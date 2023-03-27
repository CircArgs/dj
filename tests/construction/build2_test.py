"""tests for building nodes"""

import pytest
from sqlmodel import Session

from dj.construction.build2 import build_node
from dj.sql.parsing.backends.antlr4 import parse_statement


@pytest.mark.skipif("not config.getoption('newbuild')")
def test_build2_query1(session: Session):
    """
    Test building metric with dimensions
    """
    metrics = ["average_number_of_calls", "total_number_of_calls"]
    dimensions = ["direction"]
    query = build_node(
        session=session,
        metrics=metrics,
        dimensions=dimensions,
    )
    # Query1: metrics = 17, 16  dimensions = (some local dim. on 11)
    assert parse_statement(str(query)) == parse_statement("""
    select
    sum(call_end - call_start) as total_call_time,  -- 17
    avg(call_end - call_start) as average_call_time,  -- 16
    direction -- local dim. on 11
    from (  -- this is node 11
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
                from ( -- 10
                    select call_id, 'incoming' as direction, call_start, call_end, rep, customer_id, notes_id, category from incoming_customer_service
                    union
                    select call_id, 'outgoing' as direction, call_start, call_end, rep, customer_id, notes_id, category from outgoing_customer_service
                ) calls
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
    ) as calls_with_most_recent_purchase
    group by direction  -- local dim. on 11
    """)

# 17 total_number_of_calls
# 16 average_number_of_calls
@pytest.mark.skipif("not config.getoption('newbuild')")
def test_build2_query2(session: Session):
    """
    Test building metric with dimensions
    """
    metrics = ["average_number_of_calls", "total_number_of_calls"]
    dimensions = ["country"]
    query = build_node(
        session=session,
        metrics=metrics,
        dimensions=dimensions,
    )
    # Query2: metrics = 17, 16 dimensions = 14
    assert parse_statement(str(query)) == parse_statement("""
    select
    sum(call_end - call_start) as total_call_time,  -- 17
    avg(call_end - call_start) as average_call_time,  -- 16
    country.country_abbreviation -- 14
    from (  -- this is node 11
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
                from ( -- 10
                    select call_id, 'incoming' as direction, call_start, call_end, rep, customer_id, notes_id, category from incoming_customer_service
                    union
                    select call_id, 'outgoing' as direction, call_start, call_end, rep, customer_id, notes_id, category from outgoing_customer_service
                ) calls
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
    ) as calls_with_most_recent_purchase
    left join ( -- 14
          select country_abbreviation, most_recent_item
          from (
            select purchase_country as country_abbreviation, item_id as most_recent_item
            from purchase_events pe1
            where purchase_time = (
                select max(purchase_time) from purchase_events pe2 where pe1.purchase_country = pe2.purchase_country
            )
          ) c
    ) as country
    on calls_with_most_recent_purchase.purchase_country = country.country_abbreviation
    group by country.country_abbreviation -- 14
    """)

@pytest.mark.skipif("not config.getoption('newbuild')")
def test_build2_query3(session: Session):
    """
    Test building metric with dimensions
    """
    metrics = ["average_number_of_calls", "total_number_of_calls"]
    dimensions = ["item"]
    query = build_node(
        session=session,
        metrics=metrics,
        dimensions=dimensions,
    )
    # Query3: metrics = 17, 16 dimensions = 15
    # Getting to 15 requires going through 14
    assert parse_statement(str(query)) == parse_statement("""
    select
    sum(call_end - call_start) as total_call_time,  -- 17
    avg(call_end - call_start) as average_call_time,  -- 16
    item.description -- 15
    from (  -- this is node 11
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
                from ( -- 10
                    select call_id, 'incoming' as direction, call_start, call_end, rep, customer_id, notes_id, category from incoming_customer_service
                    union
                    select call_id, 'outgoing' as direction, call_start, call_end, rep, customer_id, notes_id, category from outgoing_customer_service
                ) calls
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
    ) as calls_with_most_recent_purchase
    left join ( -- 14
          select country_abbreviation, most_recent_item
          from (
            select purchase_country as country_abbreviation, item_id as most_recent_item
            from purchase_events pe1
            where purchase_time = (
                select max(purchase_time) from purchase_events pe2 where pe1.purchase_country = pe2.purchase_country
            )
          ) c
    ) as country
    on calls_with_most_recent_purchase.purchase_country = country.country_abbreviation
    left join ( -- 15
            select distinct service_item_id as item_id, 'service' as type, description, category, price
            from service_items
            union
            select distinct consumable_item_id as item_id, 'consumable' as type, description, category, price
            from consumable_items
    ) as item
    on country.most_recent_item = item.item_id -- get to 15 through 14
    group by item.description -- 15
    """)

@pytest.mark.skipif("not config.getoption('newbuild')")
def test_build2_query4(session: Session):
    """
    Test building metric with dimensions
    """
    metrics = ["average_number_of_calls", "total_number_of_calls"]
    dimensions = ["country", "item"]
    query = build_node(
        session=session,
        metrics=metrics,
        dimensions=dimensions,
    )
    # Query4: metrics = 17, 16 dimensions = 14, 15
    assert parse_statement(str(query)) == parse_statement("""
    select
    sum(call_end - call_start) as total_call_time,  -- 17
    avg(call_end - call_start) as average_call_time,  -- 16
    country.country_abbreviation, -- 14
    item.description -- 15
    from (  -- this is node 11
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
                from ( -- 10
                    select call_id, 'incoming' as direction, call_start, call_end, rep, customer_id, notes_id, category from incoming_customer_service
                    union
                    select call_id, 'outgoing' as direction, call_start, call_end, rep, customer_id, notes_id, category from outgoing_customer_service
                ) calls
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
    ) as calls_with_most_recent_purchase
    left join ( -- 14
          select country_abbreviation, most_recent_item
          from (
            select purchase_country as country_abbreviation, item_id as most_recent_item
            from purchase_events pe1
            where purchase_time = (
                select max(purchase_time) from purchase_events pe2 where pe1.purchase_country = pe2.purchase_country
            )
          ) c
    ) as country
    on calls_with_most_recent_purchase.purchase_country = country.country_abbreviation
    left join ( -- 15
            select distinct service_item_id as item_id, 'service' as type, description, category, price
            from service_items
            union
            select distinct consumable_item_id as item_id, 'consumable' as type, description, category, price
            from consumable_items
    ) as item
    on country.most_recent_item = item.item_id -- get to 15 through 14
    group by country.country_abbreviation, item.description -- 14 and 15
    """)

@pytest.mark.skipif("not config.getoption('newbuild')")
def test_build2_query5(session: Session):
    """
    Test building metric with dimensions
    """
    metrics = ["average_number_of_calls", "total_number_of_calls", "number_of_discounted_items"]
    dimensions = ["item"]
    query = build_node(
        session=session,
        metrics=metrics,
        dimensions=dimensions,
    )
    # Query5: metrics = 16, 17, 18 dimensions = 15
    assert parse_statement(str(query)) == parse_statement("""
    select
    sum(call_end - call_start) as total_call_time,  -- 17
    avg(call_end - call_start) as average_call_time,  -- 16
    country.country_abbreviation, -- 14
    item.description, -- 15
    num_discounted_items -- 18
    from (  -- this is node 11
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
                from ( -- 10
                    select call_id, 'incoming' as direction, call_start, call_end, rep, customer_id, notes_id, category from incoming_customer_service
                    union
                    select call_id, 'outgoing' as direction, call_start, call_end, rep, customer_id, notes_id, category from outgoing_customer_service
                ) calls
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
    ) as calls_with_most_recent_purchase
    left join ( -- 14
          select country_abbreviation, most_recent_item
          from (
            select purchase_country as country_abbreviation, item_id as most_recent_item
            from purchase_events pe1
            where purchase_time = (
                select max(purchase_time) from purchase_events pe2 where pe1.purchase_country = pe2.purchase_country
            )
          ) c
    ) as country
    on calls_with_most_recent_purchase.purchase_country = country.country_abbreviation
    left join ( -- 15
            select distinct service_item_id as item_id, 'service' as type, description, category, price
            from service_items
            union
            select distinct consumable_item_id as item_id, 'consumable' as type, description, category, price
            from consumable_items
    ) as item
    on country.most_recent_item = item.item_id -- get to 15 through 14
    left join ( -- 18
        select count(distinct membership_discounts.item_id) as num_discounted_items, items.description, items.item_id
        from membership_discounts
        left join (
            select distinct service_item_id as item_id, 'service' as type, description, category, price
                    from service_items
                    union
                    select distinct consumable_item_id as item_id, 'consumable' as type, description, category, price
                    from consumable_items
        ) as items
        on membership_discounts.item_id = items.item_id
        group by items.item_id, items.description
    ) as number_of_discounted_items
    on item.item_id = number_of_discounted_items.item_id
    group by country.country_abbreviation, item.description, num_discounted_items -- 14 and 15
    """)
