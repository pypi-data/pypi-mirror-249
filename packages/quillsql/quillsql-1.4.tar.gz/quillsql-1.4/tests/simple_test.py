import pytest
from quillsql import Quill
import os
from dotenv import load_dotenv

load_dotenv()


quill = Quill(
    private_key=os.environ.get("QUILL_PRIVATE_KEY"),
    database_connection_string=os.environ.get("POSTGRES_STAGING_READ"),
)


def test_config_gets_metadata():
    res = quill.query(
        org_id="2", data={"metadata": {"task": "config", "name": "spend"}}
    )

    assert res is not None
    assert "sections" in res
    assert "newQueries" in res
    assert "filters" in res
    assert res["filters"] == []
    assert "fieldToRemove" in res
    assert res["fieldToRemove"] == "customer_id"

    for query in res["newQueries"]:
        assert "columns" in query
        assert any(
            column["field"] == "spend"
            and column["label"] == "spend"
            and column["format"] == "dollar_amount"
            for column in query["columns"]
        )
        assert any(
            column["field"] == "month"
            and column["label"] == "month"
            and column["format"] == "MMM_yyyy"
            for column in query["columns"]
        )


def test_handles_empty_client_id():
    res = quill.query(
        org_id="2",
        data={
            "metadata": {
                "task": "item",
                "id": "6580d3aea2caa9000b1c1b06",
                "client_id": None,
                "filters": [],
                "query": "select * from transactions",
            }
        },
    )

    assert res["chartType"] == "line"
    assert res["clientId"] == "62cda15d7c9fcca7bc0a3689"
    assert res["name"] == "Total Spend Test"
    assert res["dashboardName"] == "spend"


def test_gets_item():
    res = quill.query(
        org_id="2",
        data={
            "metadata": {
                "task": "item",
                "id": "6580d3aea2caa9000b1c1b06",
                "client_id": "62cda15d7c9fcca7bc0a3689",
                "filters": [],
                "query": "select * from transactions",
            }
        },
    )

    assert res["chartType"] == "line"
    assert res["clientId"] == "62cda15d7c9fcca7bc0a3689"
    assert res["name"] == "Total Spend Test"
    assert res["dashboardName"] == "spend"


def test_query_for_data():
    res = quill.query(
        org_id="2",
        data={
            "metadata": {
                "task": "query",
                "id": "6580d48f457d7b000b7bee2c",
                "query": "select sum(amount) as spend, date_trunc('month', created_at) as month from transactions group by month order by max(created_at);",
            }
        },
    )

    assert "rows" in res
    assert "fields" in res


def test_creates_a_chart():
    res = quill.query(
        org_id="2",
        data={
            "metadata": {
                "task": "create",
                "dateField": {"table": "transactions", "field": "created_at"},
                "query": "select sum(amount) as spend, date_trunc('month', created_at) as month from transactions group by month order by max(created_at);",
                "name": "Total Spend Test",
                "clientId": "62cda15d7c9fcca7bc0a3689",
                "customerId": "2",
                "xAxisField": "month",
                "xAxisLabel": "month",
                "yAxisFields": [
                    {"field": "spend", "label": "spend", "format": "dollar_amount"}
                ],
                "yAxisLabel": "spend",
                "chartType": "line",
                "dashboardName": "spend",
                "xAxisFormat": "MMM_yyyy",
                "columns": [
                    {"field": "spend", "label": "spend", "format": "dollar_amount"},
                    {"field": "month", "label": "month", "format": "MMM_yyyy"},
                ],
            }
        },
    )

    assert res is not None


def test_returns_different_configs_for_different_org_ids():
    data = {
        "metadata": {
            "task": "config",
            "name": "spend",
        }
    }
    res1 = quill.query(org_id="1", data=data)
    res2 = quill.query(org_id="2", data=data)
    assert res1 != res2


def test_returns_different_items_for_different_org_ids():
    data = {
        "metadata": {
            "task": "item",
            "id": "6580d3aea2caa9000b1c1b06",
            "filters": [],
            "client_id": "62cda15d7c9fcca7bc0a3689",
            "query": "select * from transactions",
        }
    }
    res1 = quill.query(org_id="1", data=data)
    res2 = quill.query(org_id="2", data=data)
    assert res1 != res2


def test_returns_different_query_data_for_different_org_ids():
    data = {
        "metadata": {
            "task": "query",
            "id": "6580d48f457d7b000b7bee2c",
            "query": "select sum(amount) as spend, date_trunc('month', created_at) as month from transactions group by month order by max(created_at);",
        }
    }
    res1 = quill.query(org_id="1", data=data)
    res2 = quill.query(org_id="2", data=data)
    assert res1 != res2
