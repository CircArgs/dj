"""
testing ast Nodes and their methods
"""
import pytest

from dj.sql.parsing.ast import (
    Alias,
    Boolean,
    Column,
    From,
    Name,
    Namespace,
    Number,
    Query,
    Select,
    String,
    Table,
    Wildcard,
    flatten,
)
from dj.sql.parsing.backends.exceptions import DJParseException


def test_trivial_ne(trivial_query):
    """
    test find_all on a trivial query
    """
    assert not trivial_query.compare(
        Query(
            ctes=[],
            select=Select(
                distinct=False,
                from_=From(tables=[Table(Name(name="b"))]),
                projection=[Column(Name("a"))],
            ),
        ),
    )


def test_trivial_diff(trivial_query):
    """
    test find_all on a trivial query
    """
    assert trivial_query.diff(
        Query(
            ctes=[],
            select=Select(
                distinct=False,
                from_=From(tables=[Table(Name(name="b"))]),
                projection=[Column(Name("a"))],
            ),
        ),
    ) == [
        (Name(name="a", quote_style=""), Name(name="b", quote_style="")),
        (Wildcard(), Column(name=Name(name="a", quote_style=""), namespace=None)),
    ]


def test_findall_trivial(trivial_query):
    """
    test find_all on a trivial query
    """
    assert [Table(Name("a"))] == list(trivial_query.find_all(Table))


def test_filter_trivial(trivial_query):
    """
    test filtering nodes of a trivial query
    """
    assert [Table(Name("a"))] == list(
        trivial_query.filter(lambda node: isinstance(node, Table)),
    )


def test_flatten_trivial(trivial_query):
    """
    test flattening on a trivial query
    """
    assert [
        Query(
            select=Select(
                distinct=False,
                from_=From(
                    tables=[Table(name=Name(name="a", quote_style=""))],
                    joins=[],
                ),
                group_by=[],
                having=None,
                projection=[Wildcard()],
                where=None,
                limit=None,
            ),
            ctes=[],
        ),
        Select(
            distinct=False,
            from_=From(tables=[Table(name=Name(name="a", quote_style=""))], joins=[]),
            group_by=[],
            having=None,
            projection=[Wildcard()],
            where=None,
            limit=None,
        ),
        From(tables=[Table(name=Name(name="a", quote_style=""))], joins=[]),
        Table(name=Name(name="a", quote_style="")),
        Name(name="a", quote_style=""),
        Wildcard(),
    ] == list(trivial_query.flatten())


def test_trivial_apply(trivial_query):
    """
    test the apply method for nodes on a trivial query
    """
    flat = []
    trivial_query.apply(lambda node: flat.append(node))  # pylint: disable=W0108
    assert flat == list(trivial_query.flatten())


def test_named_alias_or_name_aliased():
    """
    test a named node for returning its alias name when a child of an alias
    """
    named = Table(Name(name="a"))
    _ = Alias(
        Name(name="alias"),
        child=named,
    )
    assert named.alias_or_name() == Name("alias")


def test_named_alias_or_name_not_aliased():
    """
    test a named node for returning its name when not a child of an alias
    """
    named = Table(Name(name="a"))
    _ = From(named)
    assert named.alias_or_name() == Name("a")


@pytest.mark.parametrize("name1, name2", [("a", "b"), ("c", "d")])
def test_column_hash(name1, name2):
    """
    test column hash
    """
    assert hash(Column(Name(name1))) == hash(
        Column(Name(name1)),
    )
    assert hash(Column(Name(name1))) != hash(
        Column(Name(name2)),
    )
    assert hash(Column(Name(name1))) != hash(
        Table(Name(name1)),
    )


@pytest.mark.parametrize("name1, name2", [("a", "b"), ("c", "d")])
def test_name_hash(name1, name2):
    """
    test name hash
    """
    assert hash(Name(name1)) == hash(
        Name(name1),
    )
    assert hash(Name(name1)) != hash(Name(name2))
    assert hash(Name(name1, "'")) == hash(Name(name1, "'"))


@pytest.mark.parametrize("value1, value2", list(zip(range(5), range(5, 10))))
def test_number_hash(value1, value2):
    """
    test number hash
    """
    assert hash(Number(value1)) == hash(Number(value1))
    assert hash(Number(value1)) != hash(Number(value2))
    assert hash(Number(value1)) != hash(String(str((value1))))


@pytest.mark.parametrize("value1, value2", [(True, False), (False, True)])
def test_boolean_hash(value1, value2):
    """
    test boolean hash
    """
    assert hash(Boolean(value1)) == hash(Boolean(value1))
    assert hash(Boolean(value1)) != hash(Boolean(value2))
    assert hash(Boolean(value1)) != hash(String(str((value1))))


def test_column_table():
    """
    test column hash
    """
    column = Column(Name("x"))
    column.add_table(Table(Name("a")))
    assert column.table == Table(Name("a"))


def test_table_columns():
    """
    test adding/getting columns from table
    """
    table = Table(Name("a"))
    table.add_columns(Column(Name("x")))
    assert table.columns == [Column(Name("x"))]


def test_wildcard_table_reference():
    """
    test adding/getting table from wildcard
    """
    wildcard = Wildcard()
    wildcard.add_table(Table(Name("a")))
    wildcard = wildcard.add_table(Table(Name("b")))
    assert wildcard.table == Table(Name("a"))


def test_flatten():
    """
    Test ``flatten``
    """
    assert list(
        flatten([1, {1, 2, 3}, range(5), (8, (18, [4, iter(range(9))], [10]))]),
    ) == [1, 1, 2, 3, range(0, 5), 8, 18, 4, 0, 1, 2, 3, 4, 5, 6, 7, 8, 10]


def test_get_nearest_parent():
    """
    test getting the nearest parent of a node of a certain type
    """

    name_a = Name("a")
    name_b = Name("b")

    assert name_a.get_nearest_parent_of_type(Table) is None
    table = Table(name_a, Namespace([name_b]))
    assert name_a.get_nearest_parent_of_type(Table) is table
    assert name_b.get_nearest_parent_of_type(Table) is table


def test_empty_namespace_conversion_raises():
    """
    test if an empty namespace conversion raises
    """
    with pytest.raises(DJParseException):
        Namespace([]).to_named_type(Column)


def test_double_add_namespace():
    """
    test if an empty namespace conversion raises
    """
    col = Column(Name("x"))
    col.add_namespace(Namespace([Name("a")]))
    col.add_namespace(Namespace([Name("b")]))
    assert str(col) == "a.x"
