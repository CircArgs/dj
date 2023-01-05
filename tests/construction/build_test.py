"""
Tests for building nodes and extracting dependencies
"""
import pytest
from sqlmodel import Session, select

from dj.construction.build import (
    ColumnDependencies,
    CompoundBuildException,
    InvalidSQLException,
    MissingColumnException,
    NodeTypeException,
    UnknownNodeException,
    amenable_name,
    extract_dependencies,
    extract_dependencies_from_query,
    extract_dependencies_from_select,
    get_dj_node,
    make_name,
)
from dj.models import Column
from dj.models.node import Node, NodeType
from dj.sql.parsing.ast import Alias, BinaryOp, BinaryOpKind
from dj.sql.parsing.ast import Column as ASTColumn
from dj.sql.parsing.ast import (
    From,
    Join,
    JoinKind,
    Name,
    Namespace,
    Query,
    Select,
    String,
    Table,
)
from dj.sql.parsing.backends.sqloxide import parse
from dj.typing import ColumnType


@pytest.mark.parametrize(
    "name,expected_amenable_name",
    [
        ("a.b.c.d", "a_DOT_b_DOT_c_DOT_d"),
        ("a.b.node-name", "a_DOT_b_DOT_node_MINUS_name"),
        ("node-[name]", "node_MINUS__LBRACK_name_RBRACK_"),
        ("a.b.node&(name)", "a_DOT_b_DOT_node_AMP__LPAREN_name_RPAREN_"),
        ("a.b.c.+d", "a_DOT_b_DOT_c_DOT__PLUS_d"),
        ("a.b.c.-d", "a_DOT_b_DOT_c_DOT__MINUS_d"),
        ("a.b.c.~~d", "a_DOT_b_DOT_c_DOT_______d"),
    ],
)
def test_amenable_name(name: str, expected_amenable_name: str):
    assert amenable_name(name) == expected_amenable_name


@pytest.mark.parametrize(
    "namespace,name,expected_make_name",
    [
        (Namespace([Name("a"), Name("b"), Name("c")]), "d", "a.b.c.d"),
        (Namespace([Name("a"), Name("b")]), "node-name", "a.b.node-name"),
        (Namespace([]), "node-[name]", "node-[name]"),
        (None, "node-[name]", "node-[name]"),
        (Namespace([Name("a"), Name("b"), Name("c")]), None, "a.b.c"),
        (
            Namespace([Name("a"), Name("b"), Name("c")]),
            "node&(name)",
            "a.b.c.node&(name)",
        ),
        (Namespace([Name("a"), Name("b"), Name("c")]), "+d", "a.b.c.+d"),
        (Namespace([Name("a"), Name("b"), Name("c")]), "-d", "a.b.c.-d"),
        (Namespace([Name("a"), Name("b"), Name("c")]), "~~d", "a.b.c.~~d"),
    ],
)
def test_make_name(namespace: str, name: str, expected_make_name: str):
    assert make_name(namespace, name) == expected_make_name


def test_invalid_sql_exception():
    assert "This is an exception message `foo`" in str(
        InvalidSQLException("This is an exception message", Name("foo")),
    )
    assert "This is an exception message `foo` from `bar`" in str(
        InvalidSQLException("This is an exception message", Name("foo"), Table("bar")),
    )


def test_missing_column_exception():
    assert "This is an exception message `foo`" in str(
        MissingColumnException("This is an exception message", ASTColumn("foo")),
    )
    assert "This is an exception message `foo` from `bar`" in str(
        MissingColumnException(
            "This is an exception message",
            ASTColumn("foo"),
            Table("bar"),
        ),
    )


def test_node_type_exception():
    assert "This is an exception message `foo`" in str(
        NodeTypeException("This is an exception message", Name("foo")),
    )
    assert "This is an exception message `foo` from `bar`" in str(
        NodeTypeException("This is an exception message", Name("foo"), Table("bar")),
    )


def test_unknown_node_exception():
    assert "This is an exception message `foo`" in str(
        UnknownNodeException("This is an exception message", Name("foo")),
    )
    assert "This is an exception message `foo` from `bar`" in str(
        UnknownNodeException("This is an exception message", Name("foo"), Table("bar")),
    )


def test_compound_build_exception():
    CompoundBuildException().reset()
    CompoundBuildException().set_raise(False)
    with CompoundBuildException().catch:
        raise InvalidSQLException("This SQL is invalid.", node=Name("foo"))

    assert len(CompoundBuildException().errors) == 1
    assert isinstance(CompoundBuildException().errors[0], InvalidSQLException)

    CompoundBuildException().clear()
    assert CompoundBuildException().errors == []
    assert CompoundBuildException()._raise == False

    CompoundBuildException().reset()
    assert CompoundBuildException()._raise == False


class TestExtractingDependencies:
    """A class for testing extracting dependencies from DJ queries"""

    @pytest.fixture
    def session(self, session: Session) -> Session:
        """
        Add some source nodes and transform nodes to facilitate testing of extracting dependencies
        """
        purchases = Node(
            name="purchases",
            type=NodeType.SOURCE,
            columns=[
                Column(name="transaction_id", type=ColumnType.INT),
                Column(name="transaction_time", type=ColumnType.DATETIME),
                Column(name="transaction_amount", type=ColumnType.FLOAT),
                Column(name="customer_id", type=ColumnType.INT),
            ],
        )
        customer_events = Node(
            name="customer_events",
            type=NodeType.SOURCE,
            columns=[
                Column(name="event_id", type=ColumnType.INT),
                Column(name="event_time", type=ColumnType.DATETIME),
                Column(name="event_type", type=ColumnType.STR),
                Column(name="customer_id", type=ColumnType.INT),
                Column(name="message", type=ColumnType.STR),
            ],
        )
        returns = Node(
            name="returns",
            type=NodeType.SOURCE,
            columns=[
                Column(name="transaction_id", type=ColumnType.INT),
                Column(name="transaction_time", type=ColumnType.DATETIME),
                Column(name="purchase_transaction_id", type=ColumnType.INT),
            ],
        )

        eligible_purchases = Node(
            name="eligible_purchases",
            query="""
                    SELECT transaction_id, transaction_time, transaction_amount, customer_id
                    FROM purchases
                    WHERE transaction_amount > 100.0
                """,
            type=NodeType.TRANSFORM,
            columns=[
                Column(name="transaction_id", type=ColumnType.INT),
                Column(name="transaction_time", type=ColumnType.DATETIME),
                Column(name="transaction_amount", type=ColumnType.FLOAT),
                Column(name="customer_id", type=ColumnType.INT),
            ],
        )

        returned_transactions = Node(
            name="returned_transactions",
            query="""
                    SELECT transaction_id, transaction_time, transaction_amount, customer_id
                    FROM purchases p
                    LEFT JOIN returns r
                    ON p.transaction_id = r.purchase_transaction_id
                    WHERE r.purchase_transaction_id is not null
                """,
            type=NodeType.TRANSFORM,
            columns=[
                Column(name="transaction_id", type=ColumnType.INT),
                Column(name="transaction_time", type=ColumnType.DATETIME),
                Column(name="transaction_amount", type=ColumnType.FLOAT),
                Column(name="customer_id", type=ColumnType.INT),
            ],
        )

        event_type = Node(
            name="event_type",
            type=NodeType.DIMENSION,
            query="SELECT DISTINCT event_type FROM customer_events",
            columns=[
                Column(name="event_type", type=ColumnType.STR),
            ],
        )
        session.add(purchases)
        session.add(customer_events)
        session.add(returns)
        session.add(eligible_purchases)
        session.add(returned_transactions)
        session.add(event_type)
        session.commit()
        return session

    def test_simple_select_from_single_transform(self, session: Session):
        """
        Test a simple select from a transform
        """
        query = parse(
            "select transaction_id, transaction_amount from purchases",
            "hive",
        )
        query_dependencies = extract_dependencies_from_query(session, query)
        dependencies = query_dependencies.select

        assert len(list(dependencies.all_tables)) == 1
        assert len(list(dependencies.all_node_dependencies)) == 1
        assert dependencies.columns == ColumnDependencies(
            projection=[
                (
                    ASTColumn(
                        name=Name(name="transaction_id", quote_style=""),
                        namespace=None,
                    ),
                    Table(
                        name=Name(name="purchases", quote_style=""),
                        namespace=None,
                    ),
                ),
                (
                    ASTColumn(
                        name=Name(name="transaction_amount", quote_style=""),
                        namespace=None,
                    ),
                    Table(
                        name=Name(name="purchases", quote_style=""),
                        namespace=None,
                    ),
                ),
            ],
            group_by=[],
            filters=[],
        )

        assert list(dependencies.columns.all_columns) == [
            (
                ASTColumn(
                    name=Name(name="transaction_id", quote_style=""),
                    namespace=None,
                ),
                Table(name=Name(name="purchases", quote_style=""), namespace=None),
            ),
            (
                ASTColumn(
                    name=Name(name="transaction_amount", quote_style=""),
                    namespace=None,
                ),
                Table(name=Name(name="purchases", quote_style=""), namespace=None),
            ),
        ]

        assert len(dependencies.tables) == 1
        assert dependencies.tables[0][0].name == Name(
            name="purchases",
            quote_style="",
        )
        assert dependencies.tables[0][1].name == "purchases"
        assert dependencies.tables[0][1].columns == [
            Column(
                id=1,
                dimension_id=None,
                type=ColumnType.INT,
                name="transaction_id",
                dimension_column=None,
            ),
            Column(
                id=2,
                dimension_id=None,
                type=ColumnType.DATETIME,
                name="transaction_time",
                dimension_column=None,
            ),
            Column(
                id=3,
                dimension_id=None,
                type=ColumnType.FLOAT,
                name="transaction_amount",
                dimension_column=None,
            ),
            Column(
                id=4,
                dimension_id=None,
                type=ColumnType.INT,
                name="customer_id",
                dimension_column=None,
            ),
        ]

    def test_select_from_single_transform_with_a_cte(self, session: Session):
        """
        Test a select from a transform with a cte
        """
        query = parse(
            "with p AS (select transaction_id, transaction_amount from purchases) "
            "select transaction_id, transaction_amount from p",
            "hive",
        )
        query_dependencies = extract_dependencies_from_query(session, query)
        dependencies = query_dependencies.select

        assert len(list(dependencies.all_tables)) == 1
        assert len(list(dependencies.all_node_dependencies)) == 1
        assert dependencies.columns == ColumnDependencies(
            projection=[
                (
                    ASTColumn(
                        name=Name(name="transaction_id", quote_style=""),
                        namespace=None,
                    ),
                    Table(
                        name=Name(name="purchases", quote_style=""),
                        namespace=None,
                    ),
                ),
                (
                    ASTColumn(
                        name=Name(name="transaction_amount", quote_style=""),
                        namespace=None,
                    ),
                    Table(
                        name=Name(name="purchases", quote_style=""),
                        namespace=None,
                    ),
                ),
            ],
            group_by=[],
            filters=[],
        )

        assert list(dependencies.columns.all_columns) == [
            (
                ASTColumn(
                    name=Name(name="transaction_id", quote_style=""),
                    namespace=None,
                ),
                Table(name=Name(name="purchases", quote_style=""), namespace=None),
            ),
            (
                ASTColumn(
                    name=Name(name="transaction_amount", quote_style=""),
                    namespace=None,
                ),
                Table(name=Name(name="purchases", quote_style=""), namespace=None),
            ),
        ]

        assert len(dependencies.tables) == 1
        assert dependencies.tables[0][0].name == Name(
            name="purchases",
            quote_style="",
        )
        assert dependencies.tables[0][1].name == "purchases"
        assert dependencies.tables[0][1].columns == [
            Column(
                id=1,
                dimension_id=None,
                type=ColumnType.INT,
                name="transaction_id",
                dimension_column=None,
            ),
            Column(
                id=2,
                dimension_id=None,
                type=ColumnType.DATETIME,
                name="transaction_time",
                dimension_column=None,
            ),
            Column(
                id=3,
                dimension_id=None,
                type=ColumnType.FLOAT,
                name="transaction_amount",
                dimension_column=None,
            ),
            Column(
                id=4,
                dimension_id=None,
                type=ColumnType.INT,
                name="customer_id",
                dimension_column=None,
            ),
        ]

    def test_simple_agg_from_single_transform(self, session: Session):
        """
        Test an aggregation of a column in a transform
        """
        query = parse("SELECT sum(transaction_amount) FROM eligible_purchases", "hive")
        query_dependencies = extract_dependencies_from_query(session, query)
        dependencies = query_dependencies.select

        assert dependencies.columns == ColumnDependencies(
            projection=[
                (
                    ASTColumn(
                        name=Name(name="transaction_amount", quote_style=""),
                        namespace=None,
                    ),
                    Table(
                        name=Name(name="eligible_purchases", quote_style=""),
                        namespace=None,
                    ),
                ),
            ],
            group_by=[],
            filters=[],
        )

        assert len(dependencies.tables) == 1
        assert dependencies.tables[0][0].name == Name(
            name="eligible_purchases",
            quote_style="",
        )
        assert dependencies.tables[0][1].name == "eligible_purchases"
        assert dependencies.tables[0][1].columns == [
            Column(
                id=13,
                dimension_id=None,
                type=ColumnType.INT,
                name="transaction_id",
                dimension_column=None,
            ),
            Column(
                id=14,
                dimension_id=None,
                type=ColumnType.DATETIME,
                name="transaction_time",
                dimension_column=None,
            ),
            Column(
                id=15,
                dimension_id=None,
                type=ColumnType.FLOAT,
                name="transaction_amount",
                dimension_column=None,
            ),
            Column(
                id=16,
                dimension_id=None,
                type=ColumnType.INT,
                name="customer_id",
                dimension_column=None,
            ),
        ]

    def test_group_by(self, session: Session):
        """
        Test an aggregation with a group by
        """
        query = parse(
            "SELECT sum(transaction_amount) FROM eligible_purchases GROUP BY customer_id",
            "hive",
        )
        query_dependencies = extract_dependencies_from_query(session, query)
        dependencies = query_dependencies.select

        assert dependencies.columns == ColumnDependencies(
            projection=[
                (
                    ASTColumn(
                        name=Name(name="transaction_amount", quote_style=""),
                        namespace=None,
                    ),
                    Table(
                        name=Name(name="eligible_purchases", quote_style=""),
                        namespace=None,
                    ),
                ),
            ],
            group_by=[
                (
                    ASTColumn(
                        name=Name(name="customer_id", quote_style=""),
                        namespace=None,
                    ),
                    Table(
                        name=Name(name="eligible_purchases", quote_style=""),
                        namespace=None,
                    ),
                ),
            ],
            filters=[],
        )

        assert len(dependencies.tables) == 1
        assert dependencies.tables[0][0].name == Name(
            name="eligible_purchases",
            quote_style="",
        )
        assert dependencies.tables[0][1].name == "eligible_purchases"
        assert dependencies.tables[0][1].columns == [
            Column(
                id=13,
                dimension_id=None,
                type=ColumnType.INT,
                name="transaction_id",
                dimension_column=None,
            ),
            Column(
                id=14,
                dimension_id=None,
                type=ColumnType.DATETIME,
                name="transaction_time",
                dimension_column=None,
            ),
            Column(
                id=15,
                dimension_id=None,
                type=ColumnType.FLOAT,
                name="transaction_amount",
                dimension_column=None,
            ),
            Column(
                id=16,
                dimension_id=None,
                type=ColumnType.INT,
                name="customer_id",
                dimension_column=None,
            ),
        ]

    def test_joining_table_to_itself(self, session: Session):
        """
        Test extracting dependencies from joining a table to itself
        """
        query = parse(
            """
        SELECT r2.transaction_id as matched_id
        FROM returns r1
        LEFT JOIN returns r2
        ON r1.purchase_id = r2.transaction_id
        WHERE r2.transaction_id is not null
        """,
            "hive",
        )
        query_dependencies = extract_dependencies_from_query(session, query)
        dependencies = query_dependencies.select

        assert dependencies.columns == ColumnDependencies(
            projection=[
                (
                    ASTColumn(
                        name=Name(name="transaction_id", quote_style=""),
                        namespace=Namespace(names=[Name(name="r2", quote_style="")]),
                    ),
                    Table(name=Name(name="returns", quote_style=""), namespace=None),
                ),
            ],
            group_by=[],
            filters=[
                (
                    ASTColumn(
                        name=Name(name="transaction_id", quote_style=""),
                        namespace=Namespace(names=[Name(name="r2", quote_style="")]),
                    ),
                    Table(name=Name(name="returns", quote_style=""), namespace=None),
                ),
            ],
        )

        assert len(dependencies.tables) == 2
        assert dependencies.tables[0][0].name == Name(
            name="returns",
            quote_style="",
        )
        assert dependencies.tables[0][1].name == "returns"
        assert dependencies.tables[0][1].columns == [
            Column(
                id=10,
                dimension_id=None,
                type=ColumnType.INT,
                name="transaction_id",
                dimension_column=None,
            ),
            Column(
                id=11,
                dimension_id=None,
                type=ColumnType.DATETIME,
                name="transaction_time",
                dimension_column=None,
            ),
            Column(
                id=12,
                dimension_id=None,
                type=ColumnType.INT,
                name="purchase_transaction_id",
                dimension_column=None,
            ),
        ]

        assert dependencies.tables[1][0].name == Name(
            name="returns",
            quote_style="",
        )
        assert dependencies.tables[1][1].name == "returns"
        assert dependencies.tables[1][1].columns == [
            Column(
                id=10,
                dimension_id=None,
                type=ColumnType.INT,
                name="transaction_id",
                dimension_column=None,
            ),
            Column(
                id=11,
                dimension_id=None,
                type=ColumnType.DATETIME,
                name="transaction_time",
                dimension_column=None,
            ),
            Column(
                id=12,
                dimension_id=None,
                type=ColumnType.INT,
                name="purchase_transaction_id",
                dimension_column=None,
            ),
        ]

    def test_expression_in_select(self, session: Session):
        """
        Test extracting dependencies when an expression is used in the select clause
        """
        query = parse(
            """
        SELECT transaction_id, (transaction_amount * 0.10) as reimbursement
        FROM purchases
        """,
            "hive",
        )

        query_dependencies = extract_dependencies_from_query(session, query)
        dependencies = query_dependencies.select

        assert dependencies.columns == ColumnDependencies(
            projection=[
                (
                    ASTColumn(
                        name=Name(name="transaction_id", quote_style=""),
                        namespace=None,
                    ),
                    Table(name=Name(name="purchases", quote_style=""), namespace=None),
                ),
                (
                    ASTColumn(
                        name=Name(name="transaction_amount", quote_style=""),
                        namespace=None,
                    ),
                    Table(
                        name=Name(name="purchases", quote_style=""),
                        namespace=None,
                    ),
                ),
            ],
            group_by=[],
            filters=[],
        )

        assert len(dependencies.tables) == 1
        assert dependencies.tables[0][0].name == Name(
            name="purchases",
            quote_style="",
        )
        assert dependencies.tables[0][1].name == "purchases"
        assert dependencies.tables[0][1].columns == [
            Column(
                id=1,
                dimension_id=None,
                type=ColumnType.INT,
                name="transaction_id",
                dimension_column=None,
            ),
            Column(
                id=2,
                dimension_id=None,
                type=ColumnType.DATETIME,
                name="transaction_time",
                dimension_column=None,
            ),
            Column(
                id=3,
                dimension_id=None,
                type=ColumnType.FLOAT,
                name="transaction_amount",
                dimension_column=None,
            ),
            Column(
                id=4,
                dimension_id=None,
                type=ColumnType.INT,
                name="customer_id",
                dimension_column=None,
            ),
        ]

    def test_joining_to_a_dimension(self, session: Session):
        """
        Test extracting dependencies when joining to a dimension
        """
        query = parse(
            """
            SELECT event_id, event_time, message
            FROM customer_events ce
            LEFT JOIN event_type et
            ON ce.event_type = et.id
            """,
            "hive",
        )

        # TODO: Currently fails because dimension nodes are not included in dependency extraction
        query_dependencies = extract_dependencies_from_query(session, query)
        dependencies = query_dependencies.select

    def test_ambiguous_column_name(self, session: Session):
        """
        Test extracting dependencies when column name is ambiguous
        """
        query = parse(
            """
            SELECT transaction_id
            FROM returns r
            LEFT JOIN purchases p
            ON r.purchase_transaction_id = p.transaction_id
            """,
            "hive",
        )

        with pytest.raises(InvalidSQLException) as exc_info:
            extract_dependencies_from_query(session, query)

        assert (
            "`transaction_id` appears in multiple references and so must be namespaced."
        ) in str(exc_info.value)

    def test_implicit_inner_join(self, session: Session):
        """
        Test extracting dependencies from an implicit inner join
        """
        query = parse(
            """
            SELECT purchases.transaction_id
            FROM returns, purchases
            WHERE returns.purchase_transaction_id = purchases.transaction_id
            """,
            "hive",
        )

        query_dependencies = extract_dependencies_from_query(session, query)
        dependencies = query_dependencies.select

        assert dependencies.columns == ColumnDependencies(
            projection=[
                (
                    ASTColumn(
                        name=Name(name="transaction_id", quote_style=""),
                        namespace=Namespace(
                            names=[Name(name="purchases", quote_style="")],
                        ),
                    ),
                    Table(name=Name(name="purchases", quote_style=""), namespace=None),
                ),
            ],
            group_by=[],
            filters=[
                (
                    ASTColumn(
                        name=Name(name="purchase_transaction_id", quote_style=""),
                        namespace=Namespace(
                            names=[Name(name="returns", quote_style="")],
                        ),
                    ),
                    Table(name=Name(name="returns", quote_style=""), namespace=None),
                ),
                (
                    ASTColumn(
                        name=Name(name="transaction_id", quote_style=""),
                        namespace=Namespace(
                            names=[Name(name="purchases", quote_style="")],
                        ),
                    ),
                    Table(name=Name(name="purchases", quote_style=""), namespace=None),
                ),
            ],
        )

        assert len(dependencies.tables) == 2
        assert dependencies.tables[0][0].name == Name(
            name="returns",
            quote_style="",
        )
        assert dependencies.tables[0][1].name == "returns"
        assert dependencies.tables[0][1].columns == [
            Column(
                id=10,
                dimension_id=None,
                type=ColumnType.INT,
                name="transaction_id",
                dimension_column=None,
            ),
            Column(
                id=11,
                dimension_id=None,
                type=ColumnType.DATETIME,
                name="transaction_time",
                dimension_column=None,
            ),
            Column(
                id=12,
                dimension_id=None,
                type=ColumnType.INT,
                name="purchase_transaction_id",
                dimension_column=None,
            ),
        ]

        assert dependencies.tables[1][0].name == Name(
            name="purchases",
            quote_style="",
        )
        assert dependencies.tables[1][1].name == "purchases"
        assert dependencies.tables[1][1].columns == [
            Column(
                id=1,
                dimension_id=None,
                type=ColumnType.INT,
                name="transaction_id",
                dimension_column=None,
            ),
            Column(
                id=2,
                dimension_id=None,
                type=ColumnType.DATETIME,
                name="transaction_time",
                dimension_column=None,
            ),
            Column(
                id=3,
                dimension_id=None,
                type=ColumnType.FLOAT,
                name="transaction_amount",
                dimension_column=None,
            ),
            Column(
                id=4,
                dimension_id=None,
                type=ColumnType.INT,
                name="customer_id",
                dimension_column=None,
            ),
        ]

    def test_deeply_nested_subqueries(self, session: Session):
        """
        Test extracting dependencies with deeply nested subqueries
        """
        query = parse(
            """
            SELECT
            min(event_time) as first_event_time,
            max(event_time) as last_event_time
            FROM (
              SELECT event_time
              FROM (
                SELECT event_id, event_time, message
                FROM customer_events ce
                LEFT JOIN purchases et
                ON ce.event_id = et.transaction_id
                WHERE ce.event_type = 'TRANSACTION'
              )
            )
            """,
            "hive",
        )

        query_dependencies = extract_dependencies_from_query(session, query)
        dependencies = query_dependencies.select

        assert len(list(dependencies.all_tables)) == 1
        assert dependencies.columns == ColumnDependencies(
            projection=[
                (
                    ASTColumn(
                        name=Name(name="event_time", quote_style=""),
                        namespace=None,
                    ),
                    Query(
                        select=Select(
                            from_=From(
                                tables=[
                                    Query(
                                        select=Select(
                                            from_=From(
                                                tables=[
                                                    Alias(
                                                        name=Name(
                                                            name="ce",
                                                            quote_style="",
                                                        ),
                                                        namespace=None,
                                                        child=Table(
                                                            name=Name(
                                                                name="customer_events",
                                                                quote_style="",
                                                            ),
                                                            namespace=None,
                                                        ),
                                                    ),
                                                ],
                                                joins=[
                                                    Join(
                                                        kind=JoinKind.LeftOuter,
                                                        table=Alias(
                                                            name=Name(
                                                                name="et",
                                                                quote_style="",
                                                            ),
                                                            namespace=None,
                                                            child=Table(
                                                                name=Name(
                                                                    name="purchases",
                                                                    quote_style="",
                                                                ),
                                                                namespace=None,
                                                            ),
                                                        ),
                                                        on=BinaryOp(
                                                            left=ASTColumn(
                                                                name=Name(
                                                                    name="event_id",
                                                                    quote_style="",
                                                                ),
                                                                namespace=Namespace(
                                                                    names=[
                                                                        Name(
                                                                            name="ce",
                                                                            quote_style="",
                                                                        ),
                                                                    ],
                                                                ),
                                                            ),
                                                            op=BinaryOpKind.Eq,
                                                            right=ASTColumn(
                                                                name=Name(
                                                                    name="transaction_id",
                                                                    quote_style="",
                                                                ),
                                                                namespace=Namespace(
                                                                    names=[
                                                                        Name(
                                                                            name="et",
                                                                            quote_style="",
                                                                        ),
                                                                    ],
                                                                ),
                                                            ),
                                                        ),
                                                    ),
                                                ],
                                            ),
                                            group_by=[],
                                            having=None,
                                            projection=[
                                                ASTColumn(
                                                    name=Name(
                                                        name="event_id",
                                                        quote_style="",
                                                    ),
                                                    namespace=None,
                                                ),
                                                ASTColumn(
                                                    name=Name(
                                                        name="event_time",
                                                        quote_style="",
                                                    ),
                                                    namespace=None,
                                                ),
                                                ASTColumn(
                                                    name=Name(
                                                        name="message",
                                                        quote_style="",
                                                    ),
                                                    namespace=None,
                                                ),
                                            ],
                                            where=BinaryOp(
                                                left=ASTColumn(
                                                    name=Name(
                                                        name="event_type",
                                                        quote_style="",
                                                    ),
                                                    namespace=Namespace(
                                                        names=[
                                                            Name(
                                                                name="ce",
                                                                quote_style="",
                                                            ),
                                                        ],
                                                    ),
                                                ),
                                                op=BinaryOpKind.Eq,
                                                right=String(value="TRANSACTION"),
                                            ),
                                            limit=None,
                                            distinct=False,
                                        ),
                                        ctes=[],
                                    ),
                                ],
                                joins=[],
                            ),
                            group_by=[],
                            having=None,
                            projection=[
                                ASTColumn(
                                    name=Name(name="event_time", quote_style=""),
                                    namespace=None,
                                ),
                            ],
                            where=None,
                            limit=None,
                            distinct=False,
                        ),
                        ctes=[],
                    ),
                ),
                (
                    ASTColumn(
                        name=Name(name="event_time", quote_style=""),
                        namespace=None,
                    ),
                    Query(
                        select=Select(
                            from_=From(
                                tables=[
                                    Query(
                                        select=Select(
                                            from_=From(
                                                tables=[
                                                    Alias(
                                                        name=Name(
                                                            name="ce",
                                                            quote_style="",
                                                        ),
                                                        namespace=None,
                                                        child=Table(
                                                            name=Name(
                                                                name="customer_events",
                                                                quote_style="",
                                                            ),
                                                            namespace=None,
                                                        ),
                                                    ),
                                                ],
                                                joins=[
                                                    Join(
                                                        kind=JoinKind.LeftOuter,
                                                        table=Alias(
                                                            name=Name(
                                                                name="et",
                                                                quote_style="",
                                                            ),
                                                            namespace=None,
                                                            child=Table(
                                                                name=Name(
                                                                    name="purchases",
                                                                    quote_style="",
                                                                ),
                                                                namespace=None,
                                                            ),
                                                        ),
                                                        on=BinaryOp(
                                                            left=ASTColumn(
                                                                name=Name(
                                                                    name="event_id",
                                                                    quote_style="",
                                                                ),
                                                                namespace=Namespace(
                                                                    names=[
                                                                        Name(
                                                                            name="ce",
                                                                            quote_style="",
                                                                        ),
                                                                    ],
                                                                ),
                                                            ),
                                                            op=BinaryOpKind.Eq,
                                                            right=ASTColumn(
                                                                name=Name(
                                                                    name="transaction_id",
                                                                    quote_style="",
                                                                ),
                                                                namespace=Namespace(
                                                                    names=[
                                                                        Name(
                                                                            name="et",
                                                                            quote_style="",
                                                                        ),
                                                                    ],
                                                                ),
                                                            ),
                                                        ),
                                                    ),
                                                ],
                                            ),
                                            group_by=[],
                                            having=None,
                                            projection=[
                                                ASTColumn(
                                                    name=Name(
                                                        name="event_id",
                                                        quote_style="",
                                                    ),
                                                    namespace=None,
                                                ),
                                                ASTColumn(
                                                    name=Name(
                                                        name="event_time",
                                                        quote_style="",
                                                    ),
                                                    namespace=None,
                                                ),
                                                ASTColumn(
                                                    name=Name(
                                                        name="message",
                                                        quote_style="",
                                                    ),
                                                    namespace=None,
                                                ),
                                            ],
                                            where=BinaryOp(
                                                left=ASTColumn(
                                                    name=Name(
                                                        name="event_type",
                                                        quote_style="",
                                                    ),
                                                    namespace=Namespace(
                                                        names=[
                                                            Name(
                                                                name="ce",
                                                                quote_style="",
                                                            ),
                                                        ],
                                                    ),
                                                ),
                                                op=BinaryOpKind.Eq,
                                                right=String(value="TRANSACTION"),
                                            ),
                                            limit=None,
                                            distinct=False,
                                        ),
                                        ctes=[],
                                    ),
                                ],
                                joins=[],
                            ),
                            group_by=[],
                            having=None,
                            projection=[
                                ASTColumn(
                                    name=Name(name="event_time", quote_style=""),
                                    namespace=None,
                                ),
                            ],
                            where=None,
                            limit=None,
                            distinct=False,
                        ),
                        ctes=[],
                    ),
                ),
            ],
            group_by=[],
            filters=[],
        )

    def test_extract_dependencies_from_node(self, session: Session):
        """
        Test compound build exception when extracting dependencies
        """
        eligible_purchases = session.exec(
            select(Node).where(Node.name == "eligible_purchases"),
        ).one()
        node_dependencies = extract_dependencies(
            session=session,
            node=eligible_purchases,
        )

        purchases = session.exec(select(Node).where(Node.name == "purchases")).one()

        assert len(node_dependencies) == 2
        assert node_dependencies[0] == {purchases}
        assert node_dependencies[1] == set()

    def test_extract_dependencies_from_node_with_exceptions(self, session: Session):
        """
        Test compound build exception when extracting dependencies
        """
        returned_transactions = session.exec(
            select(Node).where(Node.name == "returned_transactions"),
        ).one()
        with pytest.raises(CompoundBuildException) as exc_info:
            extract_dependencies(session=session, node=returned_transactions)

        assert "Found 2 issues:" in str(exc_info.value)
        assert (
            "MissingColumnException: `transaction_id` appears in multiple references and so must be namespaced."
            in str(exc_info.value)
        )
        assert (
            "MissingColumnException: `transaction_time` appears in multiple references and so must be namespaced."
            in str(exc_info.value)
        )

    def test_extract_dependencies_from_node_with_unraised_exceptions(
        self,
        session: Session,
    ):
        """
        Test compound build exception when extracting dependencies and not raising on exceptions
        """
        returned_transactions = session.exec(
            select(Node).where(Node.name == "returned_transactions"),
        ).one()
        node_dependencies = extract_dependencies(
            session=session,
            node=returned_transactions,
            raise_=False,
        )

        purchases = session.exec(select(Node).where(Node.name == "purchases")).one()

        assert len(node_dependencies) == 2

        n = node_dependencies[0].pop()
        assert n.name == "purchases"
        assert node_dependencies[1] == set()

    def test_extract_dependencies_from_node_with_no_query(self, session: Session):
        """
        Test compound build exception when extracting dependencies
        """

        with pytest.raises(Exception) as exc_info:
            extract_dependencies(
                session=session,
                node=Node(
                    name="queryless_node",
                    type=NodeType.TRANSFORM,
                ),
            )

        assert "Node has no query" in str(exc_info.value)


def test_get_dj_node_raise_unknown_node_exception(session: Session):
    """
    Test raising an unknown node exception when calling get_dj_node
    """
    CompoundBuildException().reset()
    with pytest.raises(UnknownNodeException) as exc_info:
        get_dj_node(session, "foobar")

    assert "No  node `foobar` exists." in str(exc_info.value)

    with pytest.raises(UnknownNodeException) as exc_info:
        get_dj_node(session, "foobar", kinds={NodeType.METRIC, NodeType.DIMENSION})

    assert "NodeType.DIMENSION" in str(exc_info.value)
    assert "NodeType.METRIC" in str(exc_info.value)
    assert "NodeType.SOURCE" not in str(exc_info.value)
    assert "NodeType.TRANSFORM" not in str(exc_info.value)
