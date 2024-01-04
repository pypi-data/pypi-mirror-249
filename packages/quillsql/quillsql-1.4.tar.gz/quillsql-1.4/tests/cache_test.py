import os
import unittest
from unittest.mock import MagicMock, patch
from quillsql import Quill
from dotenv import load_dotenv

load_dotenv()


class MockRedisClient:
    def __init__(self):
        self.data = {}

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value, _type, _expiry):
        self.data[key] = value


class TestQuillSDK(unittest.IsolatedAsyncioTestCase):
    @patch("quillsql.redis", create=True)
    def test_fuzz_test_cache_config(self, mock_redis):
        mock_redis.createClient.return_value = MockRedisClient()

        Quill(
            private_key=os.environ.get("QUILL_PRIVATE_KEY"),
            database_connection_string=os.environ.get("POSTGRES_STAGING_READ"),
            cache={
                "username": "redis",
                "password": "redis",
                "host": "localhost",
                "port": "5000",
                "cacheType": "redis",
                "ttl": 60 * 60,
            },
        )
        
        Quill(
            private_key=os.environ.get("QUILL_PRIVATE_KEY"),
            database_connection_string=os.environ.get("POSTGRES_STAGING_READ"),
            cache={
                "host": "localhost",
                "port": "5000",
            },
        )
        
        Quill(
            private_key=os.environ.get("QUILL_PRIVATE_KEY"),
            database_connection_string=os.environ.get("POSTGRES_STAGING_READ"),
            cache={
                "username": "redis",
                "password": "redis",
                "host": "localhost",
                "port": "5000",
                "ttl": 60 * 60,
            },
        )

    @patch("quillsql.redis", create=True)
    def test_config_gets_metadata(self, mock_redis):
        mock_redis.createClient.return_value = MockRedisClient()

        quill = Quill(
            private_key=os.environ.get("QUILL_PRIVATE_KEY"),
            database_connection_string=os.environ.get("POSTGRES_STAGING_READ"),
            cache={
                "username": "redis",
                "password": "redis",
                "host": "localhost",
                "port": "5000",
                "cacheType": "redis",
                "ttl": 60 * 60,
            },
        )

        res = quill.query(
            org_id="2", data={"metadata": {"task": "config", "name": "spend"}}
        )

        self.assertIsNotNone(res)
        self.assertIn("sections", res)
        self.assertIn("newQueries", res)
        self.assertIn("filters", res)
        self.assertIn("fieldToRemove", res)

        for query in res["newQueries"]:
            self.assertIsInstance(query, dict)
            self.assertIn("columns", query)

            for column in query["columns"]:
                self.assertIsInstance(column, dict)
                self.assertIn("field", column)
                self.assertIn("format", column)
                self.assertIn("label", column)

    @patch("quillsql.redis", create=True)
    def test_handles_empty_client_id(self, mock_redis):
        mock_redis.createClient.return_value = MockRedisClient()

        quill = Quill(
            private_key=os.environ.get("QUILL_PRIVATE_KEY"),
            database_connection_string=os.environ.get("POSTGRES_STAGING_READ"),
            cache={
                "username": "redis",
                "password": "redis",
                "host": "localhost",
                "port": "5000",
                "cacheType": "redis",
                "ttl": 60 * 60,
            },
        )

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

    @patch("quillsql.redis", create=True)
    def test_gets_item(self, mock_redis):
        mock_redis.createClient.return_value = MockRedisClient()

        quill = Quill(
            private_key=os.environ.get("QUILL_PRIVATE_KEY"),
            database_connection_string=os.environ.get("POSTGRES_STAGING_READ"),
            cache={
                "username": "redis",
                "password": "redis",
                "host": "localhost",
                "port": "5000",
                "cacheType": "redis",
                "ttl": 60 * 60,
            },
        )

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

    @patch("quillsql.redis", create=True)
    def test_query_for_data(self, mock_redis):
        mock_redis.createClient.return_value = MockRedisClient()

        quill = Quill(
            private_key=os.environ.get("QUILL_PRIVATE_KEY"),
            database_connection_string=os.environ.get("POSTGRES_STAGING_READ"),
            cache={
                "username": "redis",
                "password": "redis",
                "host": "localhost",
                "port": "5000",
                "cacheType": "redis",
                "ttl": 60 * 60,
            },
        )

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

    @patch("quillsql.redis", create=True)
    def test_creates_a_chart(self, mock_redis):
        mock_redis.createClient.return_value = MockRedisClient()

        quill = Quill(
            private_key=os.environ.get("QUILL_PRIVATE_KEY"),
            database_connection_string=os.environ.get("POSTGRES_STAGING_READ"),
            cache={
                "username": "redis",
                "password": "redis",
                "host": "localhost",
                "port": "5000",
                "cacheType": "redis",
                "ttl": 60 * 60,
            },
        )
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

    @patch("quillsql.redis", create=True)
    def test_returns_different_configs_for_different_org_ids(self, mock_redis):
        mock_redis.createClient.return_value = MockRedisClient()

        quill = Quill(
            private_key=os.environ.get("QUILL_PRIVATE_KEY"),
            database_connection_string=os.environ.get("POSTGRES_STAGING_READ"),
            cache={
                "username": "redis",
                "password": "redis",
                "host": "localhost",
                "port": "5000",
                "cacheType": "redis",
                "ttl": 60 * 60,
            },
        )
        data = {
            "metadata": {
                "task": "config",
                "name": "spend",
            }
        }
        res1 = quill.query(org_id="1", data=data)
        res2 = quill.query(org_id="2", data=data)
        assert res1 != res2

    @patch("quillsql.redis", create=True)
    def test_returns_different_items_for_different_org_ids(self, mock_redis):
        mock_redis.createClient.return_value = MockRedisClient()

        quill = Quill(
            private_key=os.environ.get("QUILL_PRIVATE_KEY"),
            database_connection_string=os.environ.get("POSTGRES_STAGING_READ"),
            cache={
                "username": "redis",
                "password": "redis",
                "host": "localhost",
                "port": "5000",
                "cacheType": "redis",
                "ttl": 60 * 60,
            },
        )
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

    @patch("quillsql.redis", create=True)
    def test_returns_different_query_data_for_different_org_ids(self, mock_redis):
        mock_redis.createClient.return_value = MockRedisClient()

        quill = Quill(
            private_key=os.environ.get("QUILL_PRIVATE_KEY"),
            database_connection_string=os.environ.get("POSTGRES_STAGING_READ"),
            cache={
                "username": "redis",
                "password": "redis",
                "host": "localhost",
                "port": "5000",
                "cacheType": "redis",
                "ttl": 60 * 60,
            },
        )
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


if __name__ == "__main__":
    unittest.main()
