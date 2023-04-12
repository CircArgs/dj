# pylint: disable=too-many-lines

"""
Post requests for all example entities
"""

from dj.models import Column
from dj.sql.parsing.types import IntegerType, StringType, TimestampType
from dj.typing import QueryState

EXAMPLES = (  # type: ignore
    (
        "/catalogs/",
        {"name": "draft"},
    ),
    (
        "/catalogs/",
        {"name": "default"},
    ),
    (
        "/engines/",
        {"name": "spark", "version": "3.1.1"},
    ),
    (
        "/catalogs/default/engines/",
        [{"name": "spark", "version": "3.1.1"}],
    ),
    (
        "/catalogs/",
        {"name": "public"},
    ),
    (
        "/engines/",
        {"name": "postgres", "version": "15.2"},
    ),
    (
        "/catalogs/public/engines/",
        [{"name": "postgres", "version": "15.2"}],
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "repair_order_id": {"type": "int"},
                "municipality_id": {"type": "string"},
                "hard_hat_id": {"type": "int"},
                "order_date": {"type": "timestamp"},
                "required_date": {"type": "timestamp"},
                "dispatched_date": {"type": "timestamp"},
                "dispatcher_id": {"type": "int"},
            },
            "description": "All repair orders",
            "mode": "published",
            "name": "repair_orders",
            "catalog": "default",
            "schema_": "roads",
            "table": "repair_orders",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "repair_order_id": {"type": "int"},
                "repair_type_id": {"type": "int"},
                "price": {"type": "float"},
                "quantity": {"type": "int"},
                "discount": {"type": "float"},
            },
            "description": "Details on repair orders",
            "mode": "published",
            "name": "repair_order_details",
            "catalog": "default",
            "schema_": "roads",
            "table": "repair_order_details",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "repair_type_id": {"type": "int"},
                "repair_type_name": {"type": "string"},
                "contractor_id": {"type": "int"},
            },
            "description": "Information on types of repairs",
            "mode": "published",
            "name": "repair_type",
            "catalog": "default",
            "schema_": "roads",
            "table": "repair_type",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "contractor_id": {"type": "int"},
                "company_name": {"type": "string"},
                "contact_name": {"type": "string"},
                "contact_title": {"type": "string"},
                "address": {"type": "string"},
                "city": {"type": "string"},
                "state": {"type": "string"},
                "postal_code": {"type": "string"},
                "country": {"type": "string"},
                "phone": {"type": "string"},
            },
            "description": "Information on contractors",
            "mode": "published",
            "name": "contractors",
            "catalog": "default",
            "schema_": "roads",
            "table": "contractors",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "municipality_id": {"type": "string"},
                "municipality_type_id": {"type": "string"},
            },
            "description": "Lookup table for municipality and municipality types",
            "mode": "published",
            "name": "municipality_municipality_type",
            "catalog": "default",
            "schema_": "roads",
            "table": "municipality_municipality_type",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "municipality_type_id": {"type": "string"},
                "municipality_type_desc": {"type": "string"},
            },
            "description": "Information on municipality types",
            "mode": "published",
            "name": "municipality_type",
            "catalog": "default",
            "schema_": "roads",
            "table": "municipality_type",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "municipality_id": {"type": "string"},
                "contact_name": {"type": "string"},
                "contact_title": {"type": "string"},
                "local_region": {"type": "string"},
                "phone": {"type": "string"},
                "state_id": {"type": "int"},
            },
            "description": "Information on municipalities",
            "mode": "published",
            "name": "municipality",
            "catalog": "default",
            "schema_": "roads",
            "table": "municipality",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "dispatcher_id": {"type": "int"},
                "company_name": {"type": "string"},
                "phone": {"type": "string"},
            },
            "description": "Information on dispatchers",
            "mode": "published",
            "name": "dispatchers",
            "catalog": "default",
            "schema_": "roads",
            "table": "dispatchers",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "hard_hat_id": {"type": "int"},
                "last_name": {"type": "string"},
                "first_name": {"type": "string"},
                "title": {"type": "string"},
                "birth_date": {"type": "timestamp"},
                "hire_date": {"type": "timestamp"},
                "address": {"type": "string"},
                "city": {"type": "string"},
                "state": {"type": "string"},
                "postal_code": {"type": "string"},
                "country": {"type": "string"},
                "manager": {"type": "int"},
                "contractor_id": {"type": "int"},
            },
            "description": "Information on employees",
            "mode": "published",
            "name": "hard_hats",
            "catalog": "default",
            "schema_": "roads",
            "table": "hard_hats",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "hard_hat_id": {"type": "int"},
                "state_id": {"type": "string"},
            },
            "description": "Lookup table for employee's current state",
            "mode": "published",
            "name": "hard_hat_state",
            "catalog": "default",
            "schema_": "roads",
            "table": "hard_hat_state",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "state_id": {"type": "int"},
                "state_name": {"type": "string"},
                "state_abbr": {"type": "string"},
                "state_region": {"type": "int"},
            },
            "description": "Information on different types of repairs",
            "mode": "published",
            "name": "us_states",
            "catalog": "default",
            "schema_": "roads",
            "table": "us_states",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "us_region_id": {"type": "int"},
                "us_region_description": {"type": "string"},
            },
            "description": "Information on US regions",
            "mode": "published",
            "name": "us_region",
            "catalog": "default",
            "schema_": "roads",
            "table": "us_region",
        },
    ),
    (
        "/nodes/dimension/",
        {
            "description": "Repair order dimension",
            "query": """
                        SELECT
                        repair_order_id,
                        municipality_id,
                        hard_hat_id,
                        order_date,
                        required_date,
                        dispatched_date,
                        dispatcher_id
                        FROM repair_orders
                    """,
            "mode": "published",
            "name": "repair_order",
        },
    ),
    (
        "/nodes/dimension/",
        {
            "description": "Contractor dimension",
            "query": """
                        SELECT
                        contractor_id,
                        company_name,
                        contact_name,
                        contact_title,
                        address,
                        city,
                        state,
                        postal_code,
                        country,
                        phone
                        FROM contractors
                    """,
            "mode": "published",
            "name": "contractor",
        },
    ),
    (
        "/nodes/dimension/",
        {
            "description": "Hard hat dimension",
            "query": """
                        SELECT
                        hard_hat_id,
                        last_name,
                        first_name,
                        title,
                        birth_date,
                        hire_date,
                        address,
                        city,
                        state,
                        postal_code,
                        country,
                        manager,
                        contractor_id
                        FROM hard_hats
                    """,
            "mode": "published",
            "name": "hard_hat",
        },
    ),
    (
        "/nodes/dimension/",
        {
            "description": "Hard hat dimension",
            "query": """
                        SELECT
                        hh.hard_hat_id,
                        last_name,
                        first_name,
                        title,
                        birth_date,
                        hire_date,
                        address,
                        city,
                        state,
                        postal_code,
                        country,
                        manager,
                        contractor_id,
                        hhs.state_id AS state_id
                        FROM hard_hats hh
                        LEFT JOIN hard_hat_state hhs
                        ON hh.hard_hat_id = hhs.hard_hat_id
                        WHERE hh.state_id = 'NY'
                    """,
            "mode": "published",
            "name": "local_hard_hats",
        },
    ),
    (
        "/nodes/dimension/",
        {
            "description": "US state dimension",
            "query": """
                        SELECT
                        state_id,
                        state_name,
                        state_abbr,
                        state_region,
                        r.us_region_description AS state_region_description
                        FROM us_states s
                        LEFT JOIN us_region r
                        ON s.state_region = r.us_region_id
                    """,
            "mode": "published",
            "name": "us_state",
        },
    ),
    (
        "/nodes/dimension/",
        {
            "description": "Dispatcher dimension",
            "query": """
                        SELECT
                        dispatcher_id,
                        company_name,
                        phone
                        FROM dispatchers
                    """,
            "mode": "published",
            "name": "dispatcher",
        },
    ),
    (
        "/nodes/dimension/",
        {
            "description": "Municipality dimension",
            "query": """
                        SELECT
                        m.municipality_id,
                        contact_name,
                        contact_title,
                        local_region,
                        state_id,
                        mmt.municipality_type_id,
                        mt.municipality_type_desc
                        FROM municipality AS m
                        LEFT JOIN municipality_municipality_type AS mmt
                        ON m.municipality_id = mmt.municipality_id
                        LEFT JOIN municipality_type AS mt
                        ON mmt.municipality_type_id = mt.municipality_type_desc
                    """,
            "mode": "published",
            "name": "municipality_dim",
        },
    ),
    (
        "/nodes/metric/",
        {
            "description": "Number of repair orders",
            "query": (
                "SELECT count(repair_order_id) as num_repair_orders "
                "FROM repair_orders"
            ),
            "mode": "published",
            "name": "num_repair_orders",
        },
    ),
    (
        "/nodes/metric/",
        {
            "description": "Average repair price",
            "query": "SELECT avg(price) as avg_repair_price FROM repair_order_details",
            "mode": "published",
            "name": "avg_repair_price",
        },
    ),
    (
        "/nodes/metric/",
        {
            "description": "Total repair cost",
            "query": "SELECT sum(price) as total_repair_cost FROM repair_order_details",
            "mode": "published",
            "name": "total_repair_cost",
        },
    ),
    (
        "/nodes/metric/",
        {
            "description": "Average length of employment",
            "query": (
                "SELECT avg(NOW() - hire_date) as avg_length_of_employment "
                "FROM hard_hats"
            ),
            "mode": "published",
            "name": "avg_length_of_employment",
        },
    ),
    (
        "/nodes/metric/",
        {
            "description": "Total repair order discounts",
            "query": (
                "SELECT sum(price * discount) as total_discount "
                "FROM repair_order_details"
            ),
            "mode": "published",
            "name": "total_repair_order_discounts",
        },
    ),
    (
        "/nodes/metric/",
        {
            "description": "Total repair order discounts",
            "query": (
                "SELECT avg(price * discount) as avg_repair_order_discount "
                "FROM repair_order_details"
            ),
            "mode": "published",
            "name": "avg_repair_order_discounts",
        },
    ),
    (
        "/nodes/metric/",
        {
            "description": "Average time to dispatch a repair order",
            "query": (
                "SELECT avg(dispatched_date - order_date) as avg_time_to_dispatch "
                "FROM repair_orders"
            ),
            "mode": "published",
            "name": "avg_time_to_dispatch",
        },
    ),
    (
        (
            "/nodes/repair_order_details/columns/repair_order_id/"
            "?dimension=repair_order&dimension_column=repair_order_id"
        ),
        {},
    ),
    (
        (
            "/nodes/repair_orders/columns/municipality_id/"
            "?dimension=municipality_dim&dimension_column=municipality_id"
        ),
        {},
    ),
    (
        (
            "/nodes/repair_type/columns/contractor_id/"
            "?dimension=contractor&dimension_column=contractor_id"
        ),
        {},
    ),
    (
        (
            "/nodes/repair_orders/columns/hard_hat_id/"
            "?dimension=hard_hat&dimension_column=hard_hat_id"
        ),
        {},
    ),
    (
        (
            "/nodes/repair_orders/columns/dispatcher_id/"
            "?dimension=dispatcher&dimension_column=dispatcher_id"
        ),
        {},
    ),
    (
        (
            "/nodes/local_hard_hats/columns/state_id/"
            "?dimension=us_state&dimension_column=state_id"
        ),
        {},
    ),
    (
        (
            "/nodes/repair_order_details/columns/repair_order_id/"
            "?dimension=repair_order&dimension_column=repair_order_id"
        ),
        {},
    ),
    (
        (
            "/nodes/repair_order/columns/dispatcher_id/"
            "?dimension=dispatcher&dimension_column=dispatcher_id"
        ),
        {},
    ),
    (
        (
            "/nodes/repair_order/columns/hard_hat_id/"
            "?dimension=hard_hat&dimension_column=hard_hat_id"
        ),
        {},
    ),
    (
        (
            "/nodes/repair_order/columns/municipality_id/"
            "?dimension=municipality_dim&dimension_column=municipality_id"
        ),
        {},
    ),
    (  # foo.bar Namespaced copy of roads database example
        "/nodes/source/",
        {
            "columns": {
                "repair_order_id": {"type": "int"},
                "municipality_id": {"type": "string"},
                "hard_hat_id": {"type": "int"},
                "order_date": {"type": "timestamp"},
                "required_date": {"type": "timestamp"},
                "dispatched_date": {"type": "timestamp"},
                "dispatcher_id": {"type": "int"},
            },
            "description": "All repair orders",
            "mode": "published",
            "name": "foo.bar.repair_orders",
            "catalog": "default",
            "schema_": "roads",
            "table": "repair_orders",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "repair_order_id": {"type": "int"},
                "repair_type_id": {"type": "int"},
                "price": {"type": "float"},
                "quantity": {"type": "int"},
                "discount": {"type": "float"},
            },
            "description": "Details on repair orders",
            "mode": "published",
            "name": "foo.bar.repair_order_details",
            "catalog": "default",
            "schema_": "roads",
            "table": "repair_order_details",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "repair_type_id": {"type": "int"},
                "repair_type_name": {"type": "string"},
                "contractor_id": {"type": "int"},
            },
            "description": "Information on types of repairs",
            "mode": "published",
            "name": "foo.bar.repair_type",
            "catalog": "default",
            "schema_": "roads",
            "table": "repair_type",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "contractor_id": {"type": "int"},
                "company_name": {"type": "string"},
                "contact_name": {"type": "string"},
                "contact_title": {"type": "string"},
                "address": {"type": "string"},
                "city": {"type": "string"},
                "state": {"type": "string"},
                "postal_code": {"type": "string"},
                "country": {"type": "string"},
                "phone": {"type": "string"},
            },
            "description": "Information on contractors",
            "mode": "published",
            "name": "foo.bar.contractors",
            "catalog": "default",
            "schema_": "roads",
            "table": "contractors",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "municipality_id": {"type": "string"},
                "municipality_type_id": {"type": "string"},
            },
            "description": "Lookup table for municipality and municipality types",
            "mode": "published",
            "name": "foo.bar.municipality_municipality_type",
            "catalog": "default",
            "schema_": "roads",
            "table": "municipality_municipality_type",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "municipality_type_id": {"type": "string"},
                "municipality_type_desc": {"type": "string"},
            },
            "description": "Information on municipality types",
            "mode": "published",
            "name": "foo.bar.municipality_type",
            "catalog": "default",
            "schema_": "roads",
            "table": "municipality_type",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "municipality_id": {"type": "string"},
                "contact_name": {"type": "string"},
                "contact_title": {"type": "string"},
                "local_region": {"type": "string"},
                "phone": {"type": "string"},
                "state_id": {"type": "int"},
            },
            "description": "Information on municipalities",
            "mode": "published",
            "name": "foo.bar.municipality",
            "catalog": "default",
            "schema_": "roads",
            "table": "municipality",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "dispatcher_id": {"type": "int"},
                "company_name": {"type": "string"},
                "phone": {"type": "string"},
            },
            "description": "Information on dispatchers",
            "mode": "published",
            "name": "foo.bar.dispatchers",
            "catalog": "default",
            "schema_": "roads",
            "table": "dispatchers",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "hard_hat_id": {"type": "int"},
                "last_name": {"type": "string"},
                "first_name": {"type": "string"},
                "title": {"type": "string"},
                "birth_date": {"type": "timestamp"},
                "hire_date": {"type": "timestamp"},
                "address": {"type": "string"},
                "city": {"type": "string"},
                "state": {"type": "string"},
                "postal_code": {"type": "string"},
                "country": {"type": "string"},
                "manager": {"type": "int"},
                "contractor_id": {"type": "int"},
            },
            "description": "Information on employees",
            "mode": "published",
            "name": "foo.bar.hard_hats",
            "catalog": "default",
            "schema_": "roads",
            "table": "hard_hats",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "hard_hat_id": {"type": "int"},
                "state_id": {"type": "string"},
            },
            "description": "Lookup table for employee's current state",
            "mode": "published",
            "name": "foo.bar.hard_hat_state",
            "catalog": "default",
            "schema_": "roads",
            "table": "hard_hat_state",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "state_id": {"type": "int"},
                "state_name": {"type": "string"},
                "state_abbr": {"type": "string"},
                "state_region": {"type": "int"},
            },
            "description": "Information on different types of repairs",
            "mode": "published",
            "name": "foo.bar.us_states",
            "catalog": "default",
            "schema_": "roads",
            "table": "us_states",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "us_region_id": {"type": "int"},
                "us_region_description": {"type": "string"},
            },
            "description": "Information on US regions",
            "mode": "published",
            "name": "foo.bar.us_region",
            "catalog": "default",
            "schema_": "roads",
            "table": "us_region",
        },
    ),
    (
        "/nodes/dimension/",
        {
            "description": "Repair order dimension",
            "query": """
                        SELECT
                        repair_order_id,
                        municipality_id,
                        hard_hat_id,
                        order_date,
                        required_date,
                        dispatched_date,
                        dispatcher_id
                        FROM foo.bar.repair_orders
                    """,
            "mode": "published",
            "name": "foo.bar.repair_order",
        },
    ),
    (
        "/nodes/dimension/",
        {
            "description": "Contractor dimension",
            "query": """
                        SELECT
                        contractor_id,
                        company_name,
                        contact_name,
                        contact_title,
                        address,
                        city,
                        state,
                        postal_code,
                        country,
                        phone
                        FROM foo.bar.contractors
                    """,
            "mode": "published",
            "name": "foo.bar.contractor",
        },
    ),
    (
        "/nodes/dimension/",
        {
            "description": "Hard hat dimension",
            "query": """
                        SELECT
                        hard_hat_id,
                        last_name,
                        first_name,
                        title,
                        birth_date,
                        hire_date,
                        address,
                        city,
                        state,
                        postal_code,
                        country,
                        manager,
                        contractor_id
                        FROM foo.bar.hard_hats
                    """,
            "mode": "published",
            "name": "foo.bar.hard_hat",
        },
    ),
    (
        "/nodes/dimension/",
        {
            "description": "Hard hat dimension",
            "query": """
                        SELECT
                        hh.hard_hat_id,
                        last_name,
                        first_name,
                        title,
                        birth_date,
                        hire_date,
                        address,
                        city,
                        state,
                        postal_code,
                        country,
                        manager,
                        contractor_id,
                        hhs.state_id AS state_id
                        FROM foo.bar.hard_hats hh
                        LEFT JOIN foo.bar.hard_hat_state hhs
                        ON hh.hard_hat_id = hhs.hard_hat_id
                        WHERE hh.state_id = 'NY'
                    """,
            "mode": "published",
            "name": "foo.bar.local_hard_hats",
        },
    ),
    (
        "/nodes/dimension/",
        {
            "description": "US state dimension",
            "query": """
                        SELECT
                        state_id,
                        state_name,
                        state_abbr,
                        state_region,
                        r.us_region_description AS state_region_description
                        FROM foo.bar.us_states s
                        LEFT JOIN foo.bar.us_region r
                        ON s.state_region = r.us_region_id
                    """,
            "mode": "published",
            "name": "foo.bar.us_state",
        },
    ),
    (
        "/nodes/dimension/",
        {
            "description": "Dispatcher dimension",
            "query": """
                        SELECT
                        dispatcher_id,
                        company_name,
                        phone
                        FROM foo.bar.dispatchers
                    """,
            "mode": "published",
            "name": "foo.bar.dispatcher",
        },
    ),
    (
        "/nodes/dimension/",
        {
            "description": "Municipality dimension",
            "query": """
                        SELECT
                        m.municipality_id,
                        contact_name,
                        contact_title,
                        local_region,
                        state_id,
                        mmt.municipality_type_id,
                        mt.municipality_type_desc
                        FROM foo.bar.municipality AS m
                        LEFT JOIN foo.bar.municipality_municipality_type AS mmt
                        ON m.municipality_id = mmt.municipality_id
                        LEFT JOIN foo.bar.municipality_type AS mt
                        ON mmt.municipality_type_id = mt.municipality_type_desc
                    """,
            "mode": "published",
            "name": "foo.bar.municipality_dim",
        },
    ),
    (
        "/nodes/metric/",
        {
            "description": "Number of repair orders",
            "query": (
                "SELECT count(repair_order_id) as num_repair_orders "
                "FROM foo.bar.repair_orders"
            ),
            "mode": "published",
            "name": "foo.bar.num_repair_orders",
        },
    ),
    (
        "/nodes/metric/",
        {
            "description": "Average repair price",
            "query": "SELECT avg(price) as avg_repair_price FROM foo.bar.repair_order_details",
            "mode": "published",
            "name": "foo.bar.avg_repair_price",
        },
    ),
    (
        "/nodes/metric/",
        {
            "description": "Total repair cost",
            "query": "SELECT sum(price) as total_repair_cost FROM foo.bar.repair_order_details",
            "mode": "published",
            "name": "foo.bar.total_repair_cost",
        },
    ),
    (
        "/nodes/metric/",
        {
            "description": "Average length of employment",
            "query": (
                "SELECT avg(NOW() - hire_date) as avg_length_of_employment "
                "FROM foo.bar.hard_hats"
            ),
            "mode": "published",
            "name": "foo.bar.avg_length_of_employment",
        },
    ),
    (
        "/nodes/metric/",
        {
            "description": "Total repair order discounts",
            "query": (
                "SELECT sum(price * discount) as total_discount "
                "FROM foo.bar.repair_order_details"
            ),
            "mode": "published",
            "name": "foo.bar.total_repair_order_discounts",
        },
    ),
    (
        "/nodes/metric/",
        {
            "description": "Total repair order discounts",
            "query": (
                "SELECT avg(price * discount) as avg_repair_order_discount "
                "FROM foo.bar.repair_order_details"
            ),
            "mode": "published",
            "name": "foo.bar.avg_repair_order_discounts",
        },
    ),
    (
        "/nodes/metric/",
        {
            "description": "Average time to dispatch a repair order",
            "query": (
                "SELECT avg(dispatched_date - order_date) as avg_time_to_dispatch "
                "FROM foo.bar.repair_orders"
            ),
            "mode": "published",
            "name": "foo.bar.avg_time_to_dispatch",
        },
    ),
    (
        (
            "/nodes/foo.bar.repair_order_details/columns/repair_order_id/"
            "?dimension=foo.bar.repair_order&dimension_column=repair_order_id"
        ),
        {},
    ),
    (
        (
            "/nodes/foo.bar.repair_orders/columns/municipality_id/"
            "?dimension=foo.bar.municipality_dim&dimension_column=municipality_id"
        ),
        {},
    ),
    (
        (
            "/nodes/foo.bar.repair_type/columns/contractor_id/"
            "?dimension=foo.bar.contractor&dimension_column=contractor_id"
        ),
        {},
    ),
    (
        (
            "/nodes/foo.bar.repair_orders/columns/hard_hat_id/"
            "?dimension=foo.bar.hard_hat&dimension_column=hard_hat_id"
        ),
        {},
    ),
    (
        (
            "/nodes/foo.bar.repair_orders/columns/dispatcher_id/"
            "?dimension=foo.bar.dispatcher&dimension_column=dispatcher_id"
        ),
        {},
    ),
    (
        (
            "/nodes/foo.bar.local_hard_hats/columns/state_id/"
            "?dimension=foo.bar.us_state&dimension_column=state_id"
        ),
        {},
    ),
    (
        (
            "/nodes/foo.bar.repair_order_details/columns/repair_order_id/"
            "?dimension=foo.bar.repair_order&dimension_column=repair_order_id"
        ),
        {},
    ),
    (
        (
            "/nodes/foo.bar.repair_order/columns/dispatcher_id/"
            "?dimension=foo.bar.dispatcher&dimension_column=dispatcher_id"
        ),
        {},
    ),
    (
        (
            "/nodes/foo.bar.repair_order/columns/hard_hat_id/"
            "?dimension=foo.bar.hard_hat&dimension_column=hard_hat_id"
        ),
        {},
    ),
    (
        (
            "/nodes/foo.bar.repair_order/columns/municipality_id/"
            "?dimension=foo.bar.municipality_dim&dimension_column=municipality_id"
        ),
        {},
    ),
    (  # Accounts/Revenue examples begin
        "/nodes/source/",
        {
            "columns": {
                "id": {"type": "int"},
                "account_type_name": {"type": "string"},
                "account_type_classification": {"type": "int"},
                "preferred_payment_method": {"type": "int"},
            },
            "description": "A source table for account type data",
            "mode": "published",
            "name": "account_type_table",
            "catalog": "default",
            "schema_": "accounting",
            "table": "account_type_table",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "id": {"type": "int"},
                "payment_type_name": {"type": "string"},
                "payment_type_classification": {"type": "int"},
            },
            "description": "A source table for different types of payments",
            "mode": "published",
            "name": "payment_type_table",
            "catalog": "default",
            "schema_": "accounting",
            "table": "payment_type_table",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "payment_id": {"type": "int"},
                "payment_amount": {"type": "float"},
                "payment_type": {"type": "int"},
                "customer_id": {"type": "int"},
                "account_type": {"type": "string"},
            },
            "description": "All repair orders",
            "mode": "published",
            "name": "revenue",
            "catalog": "default",
            "schema_": "accounting",
            "table": "revenue",
        },
    ),
    (
        "/nodes/dimension/",
        {
            "description": "Payment type dimensions",
            "query": (
                "SELECT id, payment_type_name, payment_type_classification "
                "FROM payment_type_table"
            ),
            "mode": "published",
            "name": "payment_type",
        },
    ),
    (
        "/nodes/dimension/",
        {
            "description": "Account type dimension",
            "query": (
                "SELECT id, account_type_name, "
                "account_type_classification FROM "
                "account_type_table"
            ),
            "mode": "published",
            "name": "account_type",
        },
    ),
    (
        "/nodes/transform/",
        {
            "query": (
                "SELECT payment_id, payment_amount, customer_id, account_type "
                "FROM revenue WHERE payment_amount > 1000000"
            ),
            "description": "Only large revenue payments",
            "mode": "published",
            "name": "large_revenue_payments_only",
        },
    ),
    (
        "/nodes/transform/",
        {
            "query": (
                "SELECT payment_id, payment_amount, customer_id, account_type "
                "FROM revenue WHERE "
                "large_revenue_payments_and_business_only > 1000000 "
                "AND account_type='BUSINESS'"
            ),
            "description": "Only large revenue payments from business accounts",
            "mode": "published",
            "name": "large_revenue_payments_and_business_only",
        },
    ),
    (
        "/nodes/metric/",
        {
            "description": "Total number of account types",
            "query": "SELECT count(id) as num_accounts FROM account_type",
            "mode": "published",
            "name": "number_of_account_types",
        },
    ),
    (  # Basic namespace
        "/nodes/source/",
        {
            "name": "basic.source.users",
            "description": "A user table",
            "columns": {
                "id": {"type": "int"},
                "full_name": {"type": "string"},
                "age": {"type": "int"},
                "country": {"type": "string"},
                "gender": {"type": "string"},
                "preferred_language": {"type": "string"},
                "secret_number": {"type": "float"},
                "created_at": {"type": "timestamp"},
                "post_processing_timestamp": {"type": "timestamp"},
            },
            "mode": "published",
            "catalog": "public",
            "schema_": "basic",
            "table": "dim_users",
        },
    ),
    (
        "/nodes/dimension/",
        {
            "description": "User dimension",
            "query": (
                "SELECT id, full_name, age, country, gender, preferred_language, "
                "secret_number, created_at, post_processing_timestamp "
                "FROM basic.source.users"
            ),
            "mode": "published",
            "name": "basic.dimension.users",
        },
    ),
    (
        "/nodes/source/",
        {
            "name": "basic.source.comments",
            "description": "A fact table with comments",
            "columns": {
                "id": {"type": "int"},
                "user_id": {
                    "type": "int",
                    "dimension": "basic.dimension.users",
                },
                "timestamp": {"type": "timestamp"},
                "text": {"type": "string"},
                "event_timestamp": {"type": "timestamp"},
                "created_at": {"type": "timestamp"},
                "post_processing_timestamp": {"type": "timestamp"},
            },
            "mode": "published",
            "catalog": "public",
            "schema_": "basic",
            "table": "comments",
        },
    ),
    (
        "/nodes/dimension/",
        {
            "description": "Country dimension",
            "query": "SELECT country, COUNT(1) AS user_cnt "
            "FROM basic.source.users GROUP BY country",
            "mode": "published",
            "name": "basic.dimension.countries",
        },
    ),
    (
        "/nodes/transform/",
        {
            "description": "Country level agg table",
            "query": (
                "SELECT country, COUNT(DISTINCT id) AS num_users "
                "FROM basic.source.users GROUP BY 1"
            ),
            "mode": "published",
            "name": "basic.transform.country_agg",
        },
    ),
    (
        "/nodes/metric/",
        {
            "description": "Number of comments",
            "query": ("SELECT COUNT(1) AS cnt " "FROM basic.source.comments"),
            "mode": "published",
            "name": "basic.num_comments",
        },
    ),
    (
        "/nodes/metric/",
        {
            "description": "Number of users.",
            "type": "metric",
            "query": ("SELECT SUM(num_users) " "FROM basic.transform.country_agg"),
            "mode": "published",
            "name": "basic.num_users",
        },
    ),
    (  # Event examples
        "/nodes/source/",
        {
            "name": "event_source",
            "description": "Events",
            "columns": {
                "event_id": {"type": "int"},
                "event_latency": {"type": "int"},
                "device_id": {"type": "int"},
                "country": {"type": "string"},
            },
            "mode": "published",
            "catalog": "default",
            "schema_": "logs",
            "table": "log_events",
        },
    ),
    (
        "/nodes/transform/",
        {
            "name": "long_events",
            "description": "High-Latency Events",
            "query": "SELECT event_id, event_latency, device_id, country "
            "FROM event_source WHERE event_latency > 1000000",
            "mode": "published",
        },
    ),
    (
        "/nodes/dimension/",
        {
            "name": "country_dim",
            "description": "Country Dimension",
            "query": "SELECT country, COUNT(DISTINCT event_id) AS events_cnt "
            "FROM event_source GROUP BY country",
            "mode": "published",
        },
    ),
    (
        "/nodes/event_source/columns/country/?dimension=country_dim&dimension_column=country",
        {},
    ),
    (
        "/nodes/metric/",
        {
            "name": "device_ids_count",
            "description": "Number of Distinct Devices",
            "query": "SELECT COUNT(DISTINCT device_id) " "FROM event_source",
            "mode": "published",
        },
    ),
    (
        "/nodes/metric/",
        {
            "name": "long_events_distinct_countries",
            "description": "Number of Distinct Countries for Long Events",
            "query": "SELECT COUNT(DISTINCT country) " "FROM long_events",
            "mode": "published",
        },
    ),
    (  # DBT examples
        "/nodes/source/",
        {
            "columns": {
                "id": {"type": "int"},
                "first_name": {"type": "string"},
                "last_name": {"type": "string"},
            },
            "description": "Customer table",
            "mode": "published",
            "name": "dbt.source.jaffle_shop.customers",
            "catalog": "public",
            "schema_": "jaffle_shop",
            "table": "customers",
        },
    ),
    (
        "/nodes/dimension/",
        {
            "description": "User dimension",
            "query": (
                "SELECT id, first_name, last_name "
                "FROM dbt.source.jaffle_shop.customers"
            ),
            "mode": "published",
            "name": "dbt.dimension.customers",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "id": {"type": "int"},
                "user_id": {
                    "type": "int",
                    "dimension": "dbt.dimension.customers",
                },
                "order_date": {"type": "date"},
                "status": {"type": "string"},
                "_etl_loaded_at": {"type": "timestamp"},
            },
            "description": "Orders fact table",
            "mode": "published",
            "name": "dbt.source.jaffle_shop.orders",
            "catalog": "public",
            "schema_": "jaffle_shop",
            "table": "orders",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "id": {"type": "int"},
                "orderid": {"type": "int"},
                "paymentmethod": {"type": "string"},
                "status": {"type": "string"},
                "amount": {"type": "int"},
                "created": {"type": "date"},
                "_batched_at": {"type": "timestamp"},
            },
            "description": "Payments fact table.",
            "mode": "published",
            "name": "dbt.source.stripe.payments",
            "catalog": "public",
            "schema_": "stripe",
            "table": "payments",
        },
    ),
    (
        "/nodes/transform/",
        {
            "query": (
                "SELECT c.id, "
                "        c.first_name, "
                "        c.last_name, "
                "        COUNT(1) AS order_cnt "
                "FROM dbt.source.jaffle_shop.orders o "
                "JOIN dbt.source.jaffle_shop.customers c ON o.user_id = c.id "
                "GROUP BY c.id, "
                "        c.first_name, "
                "        c.last_name "
            ),
            "description": "Country level agg table",
            "mode": "published",
            "name": "dbt.transform.customer_agg",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "id": {"type": "int"},
                "item_name": {"type": "string"},
                "sold_count": {"type": "int"},
                "price_per_unit": {"type": "float"},
                "psp": {"type": "string"},
            },
            "description": "A source table for sales",
            "mode": "published",
            "name": "sales",
            "catalog": "default",
            "schema_": "revenue",
            "table": "sales",
        },
    ),
    (
        "/nodes/dimension/",
        {
            "description": "Item dimension",
            "query": ("SELECT item_name " "account_type_classification FROM " "sales"),
            "mode": "published",
            "name": "items",
        },
    ),
    (
        "/nodes/metric/",
        {
            "description": "Total units sold",
            "query": "SELECT SUM(sold_count) as num_sold FROM sales",
            "mode": "published",
            "name": "items_sold_count",
        },
    ),
    (
        "/nodes/metric/",
        {
            "description": "Total profit",
            "query": "SELECT SUM(sold_count * price_per_unit) as num_sold FROM sales",
            "mode": "published",
            "name": "total_profit",
        },
    ),
    ( # Bodega Salon
        "/nodes/source/",
        {
            "columns": {
                "call_id": {"type": "INT"},
                "call_start": {"type": "TIMESTAMP"},
                "call_end": {"type": "TIMESTAMP"},
                "rep": {"type": "STR"},
                "customer_id": {"type": "INT"},
                "notes_id": {"type": "INT"},
                "category": {"type": "STR"},
            },
            "description": "(1) Incoming customer service calls",
            "mode": "published",
            "name": "incoming_customer_service",
            "catalog": "default",
            "schema_": "public",
            "table": "incoming_customer_service",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "call_id": {"type": "INT"},
                "call_start": {"type": "TIMESTAMP"},
                "call_end": {"type": "TIMESTAMP"},
                "rep": {"type": "STR"},
                "customer_id": {"type": "INT"},
                "notes_id": {"type": "INT"},
                "category": {"type": "STR"},
            },
            "description": "(2) Outgoing customer service calls",
            "mode": "published",
            "name": "outgoing_customer_service",
            "catalog": "default",
            "schema_": "public",
            "table": "outgoing_customer_service",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "customer_d": {"type": "INT"},
                "first_name": {"type": "STR"},
                "last_name": {"type": "STR"},
            },
            "description": "(3) Customer data",
            "mode": "published",
            "name": "customer_d",
            "catalog": "default",
            "schema_": "public",
            "table": "customer_d",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "purchase_id": {"type": "INT"},
                "item_id": {"type": "INT"},
                "item_type": {"type": "STR"},
                "account_id": {"type": "INT"},
                "purchase_country": {"type": "STR"},
                "purchase_time": {"type": "TIMESTAMP"},
            },
            "description": "(4) Purchase data",
            "mode": "published",
            "name": "purchase_events",
            "catalog": "default",
            "schema_": "public",
            "table": "purchase_events",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "account_id": {"type": "INT"},
                "account_type": {"type": "STR"},
                "customer_id": {"type": "INT"},
                "home_country": {"type": "STR"},
            },
            "description": "(5) Customer accounts",
            "mode": "published",
            "name": "customer_accounts",
            "catalog": "default",
            "schema_": "public",
            "table": "customer_accounts",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "service_item_id": {"type": "INT"},
                "description": {"type": "STR"},
                "category": {"type": "STR"},
                "price": {"type": "FLOAT"},
            },
            "description": "(6) Services for purchase",
            "mode": "published",
            "name": "service_items",
            "catalog": "default",
            "schema_": "public",
            "table": "service_items",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "membership_id": {"type": "INT"},
                "item_id": {"type": "INT"},
                "discount": {"type": "fLOAT"},
            },
            "description": "(9) Item discounts for memberships",
            "mode": "published",
            "name": "membership_discounts",
            "catalog": "default",
            "schema_": "public",
            "table": "membership_discounts",
        },
    ),
    (
        "/nodes/source/",
        {
            "columns": {
                "consumable_item_id": {"type": "INT"},
                "description": {"type": "STR"},
                "category": {"type": "STR"},
                "price": {"type": "FLOAT"},
            },
            "description": "(7) Consumables for purchase",
            "mode": "published",
            "name": "consumable_items",
            "catalog": "default",
            "schema_": "public",
            "table": "consumable_items",
        },
    ),
    (
        "/nodes/transform/",
        {
            "description": "(10) Incoming and outgoing customer service calls",
            "query": """
                select call_id, 'incoming' as direction, call_start, call_end, rep, customer_id, notes_id, category from incoming_customer_service
                -- union
                -- select call_id, 'outgoing' as direction, call_start, call_end, rep, customer_id, notes_id, category from outgoing_customer_service
            """,
            "mode": "published",
            "name": "incoming_and_outgoing_calls",
            "type": "transform",
        },
    ),
    (
        "/nodes/transform/",
        {
            "description": "(11) Calls enriched with most recently purchased item",
            "query": """
                with purchase_events_with_customer_id as (
                    select
                        pe.account_id
                        ,pe.item_id
                        ,pe.purchase_country
                        ,pe.purchase_time
                        ,ca.customer_id
                    from purchase_events pe
                    left join customer_accounts ca
                    on pe.account_id = ca.account_id
                )
                select distinct
                    calls.call_id
                    ,calls.direction
                    ,calls.call_start
                    ,calls.call_end
                    ,calls.rep
                    ,calls.customer_id
                    ,calls.notes_id
                    ,calls.category
                    ,most_recent_purchase.customer_id
                    ,most_recent_purchase.item_id
                    ,most_recent_purchase.purchase_country
                from incoming_and_outgoing_calls calls
                left join customer_accounts ca
                on calls.customer_id = ca.customer_id
                left join (
                    select customer_id, item_id, purchase_country
                    from purchase_events_with_customer_id pe1
                    where purchase_time = (
                        select max(purchase_time) from purchase_events_with_customer_id pe2 where pe1.customer_id = pe2.customer_id
                    )
                ) most_recent_purchase
                on ca.customer_id = most_recent_purchase.customer_id
            """,
            "mode": "published",
            "name": "calls_with_most_recent_purchase",
            "type": "transform",
        },
    ),
    (
        "/nodes/dimension/",
        {
            "description": "(13) Customers",
            "query": """
                select customer_id, first_name, last_name from customer_d
            """,
            "mode": "published",
            "name": "customer",
        },
    ),
    (
        "/nodes/dimension/",
        {
            "description": "(14) Countries",
            "query": """
            select country_abbreviation, most_recent_item
            from (
                select purchase_country as country_abbreviation, item_id as most_recent_item
                from purchase_events pe1
                where purchase_time = (
                    select max(purchase_time) from purchase_events pe2 where pe1.purchase_country = pe2.purchase_country
                )
            ) c
            """,
            "mode": "published",
            "name": "country",
        },
    ),
    (
        "/nodes/dimension/",
        {
            "description": "(15) Items",
            "query": """
                select distinct service_item_id as item_id, 'service' as type, description, category, price
                from service_items
                -- union
                -- select distinct consumable_item_id as item_id, 'consumable' as type, description, category, price
                -- from consumable_items
            """,
            "mode": "published",
            "name": "item",
        },
    ),
    (
        "/nodes/metric/",
        {
            "description": "(16) Average length of customer service calls",
            "query": """
                select avg(call_end - call_start) as average_call_time from calls_with_most_recent_purchase
            """,
            "mode": "published",
            "name": "average_number_of_calls",
        },
    ),
    (
        "/nodes/metric/",
        {
            "description": "(17) Total length of customer service calls",
            "query": """
                select sum(call_end - call_start) as total_call_time from calls_with_most_recent_purchase
            """,
            "mode": "published",
            "name": "total_number_of_calls",
        },
    ),
    (
        "/nodes/metric/",
        {
            "description": "(18) Total number of items with member discounts",
            "query": """
                select count(distinct item_id) as num_discounted_items from membership_discounts
            """,
            "mode": "published",
            "name": "number_of_discounted_items",
        },
    ),
    (
        "/nodes/metric/",
        {
            "description": "(19) Average item discount",
            "query": """
                select avg(discount) as avg_discount from membership_discounts
            """,
            "mode": "published",
            "name": "average_item_discount",
        },
    ),
)


COLUMN_MAPPINGS = {
    "public.basic.comments": [
        Column(name="id", type=IntegerType()),
        Column(name="user_id", type=IntegerType()),
        Column(name="timestamp", type=TimestampType()),
        Column(name="text", type=StringType()),
    ],
}

QUERY_DATA_MAPPINGS = {
    (
        "SELECT  payment_type_table.id,\n\tpayment_type_table.payment_type_classification,\n\t"
        "payment_type_table.payment_type_name \n FROM accounting.payment_type_table AS "
        "payment_type_table"
    )
    .strip()
    .replace('"', "")
    .replace("\n", "")
    .replace(" ", ""): [
        {
            "submitted_query": (
                "SELECT  payment_type_table.id,\n\tpayment_type_table."
                "payment_type_classification,\n\t"
                'payment_type_table.payment_type_name \n FROM "accounting"."payment_type_table" '
                "AS payment_type_table"
            ),
            "state": QueryState.FINISHED,
            "results": {
                "columns": [
                    {"name": "id", "type": "int"},
                    {"name": "payment_type_classification", "type": "string"},
                    {"name": "payment_type_name", "type": "string"},
                ],
                "rows": [
                    (1, "CARD", "VISA"),
                    (2, "CARD", "MASTERCARD"),
                ],
            },
            "errors": [],
        },
    ],
    'SELECT  COUNT(1) AS cnt \n FROM "basic"."comments" AS basic_DOT_source_DOT_comments'.strip()
    .replace('"', "")
    .replace("\n", "")
    .replace(" ", ""): {
        "submitted_query": (
            'SELECT  COUNT(1) AS cnt \n FROM "basic"."comments" AS basic_DOT_source_DOT_comments'
        ),
        "state": QueryState.FINISHED,
        "results": {
            "columns": [{"name": "cnt", "type": "int"}],
            "rows": [
                (1,),
            ],
        },
        "errors": [],
    },
    'SELECT  * \n FROM "accounting"."revenue"'.strip()
    .replace('"', "")
    .replace("\n", "")
    .replace(" ", ""): {
        "submitted_query": ('SELECT  * \n FROM "accounting"."revenue"'),
        "state": QueryState.FINISHED,
        "results": {
            "columns": [{"name": "profit", "type": "float"}],
            "rows": [
                (129.19,),
            ],
        },
        "errors": [],
    },
    (
        "SELECT  revenue.account_type,\n\trevenue.customer_id,\n\trevenue.payment_amount,"
        '\n\trevenue.payment_id \n FROM "accounting"."revenue" AS revenue\n \n '
        "WHERE  revenue.payment_amount > 1000000"
    )
    .strip()
    .replace('"', "")
    .replace("\n", "")
    .replace(" ", ""): {
        "submitted_query": (
            "SELECT  revenue.account_type,\n\trevenue.customer_id,\n\trevenue.payment_amount,"
            '\n\trevenue.payment_id \n FROM "accounting"."revenue" AS revenue\n \n '
            "WHERE  revenue.payment_amount > 1000000"
        ),
        "state": QueryState.FINISHED,
        "results": {
            "columns": [
                {"name": "account_type", "type": "string"},
                {"name": "customer_id", "type": "int"},
                {"name": "payment_amount", "type": "string"},
                {"name": "payment_id", "type": "int"},
            ],
            "rows": [
                ("CHECKING", 2, "22.50", 1),
                ("SAVINGS", 2, "100.50", 1),
                ("CREDIT", 1, "11.50", 1),
                ("CHECKING", 2, "2.50", 1),
            ],
        },
        "errors": [],
    },
}
