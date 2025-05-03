"""Tests for the RabbitMQ MCP server."""

from unittest.mock import MagicMock, patch

import pytest

from mcp_server_rabbitmq.server import (
    enqueue,
    fanout,
    list_queues,
)


@pytest.fixture
def setup_global_vars():
    """Set up global variables for testing."""
    import mcp_server_rabbitmq.server as server
    server.rabbitmq_host = "localhost"
    server.rabbitmq_port = 5672
    server.rabbitmq_username = "guest"
    server.rabbitmq_password = "guest"
    server.rabbitmq_use_tls = False
    server.rabbitmq_api_port = 15672


class TestRabbitMQTools:
    """Test the RabbitMQ MCP tools."""

    @patch("mcp_server_rabbitmq.server.RabbitMQConnection")
    @patch("mcp_server_rabbitmq.server.handle_enqueue")
    def test_enqueue(self, mock_handle_enqueue, mock_connection, setup_global_vars):
        """Test the enqueue tool."""
        mock_connection.return_value = MagicMock()
        
        result = enqueue("test_queue", "test_message")
        
        mock_connection.assert_called_once_with(
            "localhost", 5672, "guest", "guest", False
        )
        mock_handle_enqueue.assert_called_once_with(
            mock_connection.return_value, "test_queue", "test_message"
        )
        assert "successfully" in result

    @patch("mcp_server_rabbitmq.server.RabbitMQConnection")
    @patch("mcp_server_rabbitmq.server.handle_fanout")
    def test_fanout(self, mock_handle_fanout, mock_connection, setup_global_vars):
        """Test the fanout tool."""
        mock_connection.return_value = MagicMock()
        
        result = fanout("test_exchange", "test_message")
        
        mock_connection.assert_called_once_with(
            "localhost", 5672, "guest", "guest", False
        )
        mock_handle_fanout.assert_called_once_with(
            mock_connection.return_value, "test_exchange", "test_message"
        )
        assert "successfully" in result

    @patch("mcp_server_rabbitmq.server.RabbitMQAdmin")
    @patch("mcp_server_rabbitmq.server.handle_list_queues")
    def test_list_queues(self, mock_handle_list_queues, mock_admin, setup_global_vars):
        """Test the list_queues tool."""
        mock_admin.return_value = MagicMock()
        mock_handle_list_queues.return_value = ["queue1", "queue2"]
        
        result = list_queues()
        
        mock_admin.assert_called_once_with(
            "localhost", 15672, "guest", "guest", False
        )
        mock_handle_list_queues.assert_called_once_with(mock_admin.return_value)
        assert "['queue1', 'queue2']" == result
