"""Tests for the RabbitMQ MCP server."""

from unittest.mock import MagicMock, patch

import pytest

from mcp_server_rabbitmq.server import RabbitMQMCPServer


@pytest.fixture
def server():
    """Create a RabbitMQMCPServer instance for testing."""
    with patch("mcp_server_rabbitmq.server.FastMCP") as mock_fastmcp:
        server_instance = RabbitMQMCPServer()
        server_instance.rabbitmq_host = "localhost"
        server_instance.rabbitmq_port = 5672
        server_instance.rabbitmq_username = "guest"
        server_instance.rabbitmq_password = "guest"
        server_instance.rabbitmq_use_tls = False
        server_instance.rabbitmq_api_port = 15672
        yield server_instance


class TestRabbitMQTools:
    """Test the RabbitMQ MCP tools."""

    def test_enqueue(self, server):
        """Test the enqueue tool."""
        with patch("mcp_server_rabbitmq.server.RabbitMQConnection") as mock_connection:
            with patch("mcp_server_rabbitmq.server.handle_enqueue") as mock_handle_enqueue:
                with patch("mcp_server_rabbitmq.server.validate_rabbitmq_name"):
                    mock_connection.return_value = MagicMock()
                    mock_handle_enqueue.return_value = None
                    
                    # Extract the enqueue function from the server
                    # This is the function that was registered with @mcp.tool()
                    enqueue_func = None
                    for name, func in server.mcp.tool.mock_calls:
                        if name == "()" and func[0].__name__ == "enqueue":
                            enqueue_func = func[0]
                            break
                    
                    assert enqueue_func is not None, "Could not find enqueue function"
                    
                    # Call the function directly
                    result = enqueue_func("test_queue", "test_message")
                    
                    mock_connection.assert_called_once_with(
                        "localhost", 5672, "guest", "guest", False
                    )
                    mock_handle_enqueue.assert_called_once_with(
                        mock_connection.return_value, "test_queue", "test_message"
                    )
                    assert "successfully" in result

    def test_fanout(self, server):
        """Test the fanout tool."""
        with patch("mcp_server_rabbitmq.server.RabbitMQConnection") as mock_connection:
            with patch("mcp_server_rabbitmq.server.handle_fanout") as mock_handle_fanout:
                with patch("mcp_server_rabbitmq.server.validate_rabbitmq_name"):
                    mock_connection.return_value = MagicMock()
                    mock_handle_fanout.return_value = None
                    
                    # Extract the fanout function from the server
                    fanout_func = None
                    for name, func in server.mcp.tool.mock_calls:
                        if name == "()" and func[0].__name__ == "fanout":
                            fanout_func = func[0]
                            break
                    
                    assert fanout_func is not None, "Could not find fanout function"
                    
                    # Call the function directly
                    result = fanout_func("test_exchange", "test_message")
                    
                    mock_connection.assert_called_once_with(
                        "localhost", 5672, "guest", "guest", False
                    )
                    mock_handle_fanout.assert_called_once_with(
                        mock_connection.return_value, "test_exchange", "test_message"
                    )
                    assert "successfully" in result

    def test_list_queues(self, server):
        """Test the list_queues tool."""
        with patch("mcp_server_rabbitmq.server.RabbitMQAdmin") as mock_admin:
            with patch("mcp_server_rabbitmq.server.handle_list_queues") as mock_handle_list_queues:
                mock_admin.return_value = MagicMock()
                mock_handle_list_queues.return_value = ["queue1", "queue2"]
                
                # Extract the list_queues function from the server
                list_queues_func = None
                for name, func in server.mcp.tool.mock_calls:
                    if name == "()" and func[0].__name__ == "list_queues":
                        list_queues_func = func[0]
                        break
                
                assert list_queues_func is not None, "Could not find list_queues function"
                
                # Call the function directly
                result = list_queues_func()
                
                mock_admin.assert_called_once_with(
                    "localhost", 15672, "guest", "guest", False
                )
                mock_handle_list_queues.assert_called_once_with(mock_admin.return_value)
                assert "['queue1', 'queue2']" == result

    def test_list_exchanges(self, server):
        """Test the list_exchanges tool."""
        with patch("mcp_server_rabbitmq.server.RabbitMQAdmin") as mock_admin:
            with patch("mcp_server_rabbitmq.server.handle_list_exchanges") as mock_handle_list_exchanges:
                mock_admin.return_value = MagicMock()
                mock_handle_list_exchanges.return_value = ["exchange1", "exchange2"]
                
                # Extract the list_exchanges function from the server
                list_exchanges_func = None
                for name, func in server.mcp.tool.mock_calls:
                    if name == "()" and func[0].__name__ == "list_exchanges":
                        list_exchanges_func = func[0]
                        break
                
                assert list_exchanges_func is not None, "Could not find list_exchanges function"
                
                # Call the function directly
                result = list_exchanges_func()
                
                mock_admin.assert_called_once_with(
                    "localhost", 15672, "guest", "guest", False
                )
                mock_handle_list_exchanges.assert_called_once_with(mock_admin.return_value)
                assert "['exchange1', 'exchange2']" == result

    def test_get_queue_info(self, server):
        """Test the get_queue_info tool."""
        with patch("mcp_server_rabbitmq.server.RabbitMQAdmin") as mock_admin:
            with patch("mcp_server_rabbitmq.server.handle_get_queue_info") as mock_handle_get_queue_info:
                with patch("mcp_server_rabbitmq.server.validate_rabbitmq_name"):
                    mock_admin.return_value = MagicMock()
                    mock_handle_get_queue_info.return_value = {"name": "test_queue", "messages": 10}
                    
                    # Extract the get_queue_info function from the server
                    get_queue_info_func = None
                    for name, func in server.mcp.tool.mock_calls:
                        if name == "()" and func[0].__name__ == "get_queue_info":
                            get_queue_info_func = func[0]
                            break
                    
                    assert get_queue_info_func is not None, "Could not find get_queue_info function"
                    
                    # Call the function directly
                    result = get_queue_info_func("test_queue")
                    
                    mock_admin.assert_called_once_with(
                        "localhost", 15672, "guest", "guest", False
                    )
                    mock_handle_get_queue_info.assert_called_once_with(mock_admin.return_value, "test_queue", "/")
                    assert "{'name': 'test_queue', 'messages': 10}" == result

    def test_delete_queue(self, server):
        """Test the delete_queue tool."""
        with patch("mcp_server_rabbitmq.server.RabbitMQAdmin") as mock_admin:
            with patch("mcp_server_rabbitmq.server.handle_delete_queue") as mock_handle_delete_queue:
                with patch("mcp_server_rabbitmq.server.validate_rabbitmq_name"):
                    mock_admin.return_value = MagicMock()
                    
                    # Extract the delete_queue function from the server
                    delete_queue_func = None
                    for name, func in server.mcp.tool.mock_calls:
                        if name == "()" and func[0].__name__ == "delete_queue":
                            delete_queue_func = func[0]
                            break
                    
                    assert delete_queue_func is not None, "Could not find delete_queue function"
                    
                    # Call the function directly
                    result = delete_queue_func("test_queue")
                    
                    mock_admin.assert_called_once_with(
                        "localhost", 15672, "guest", "guest", False
                    )
                    mock_handle_delete_queue.assert_called_once_with(mock_admin.return_value, "test_queue", "/")
                    assert "successfully deleted" in result

    def test_purge_queue(self, server):
        """Test the purge_queue tool."""
        with patch("mcp_server_rabbitmq.server.RabbitMQAdmin") as mock_admin:
            with patch("mcp_server_rabbitmq.server.handle_purge_queue") as mock_handle_purge_queue:
                with patch("mcp_server_rabbitmq.server.validate_rabbitmq_name"):
                    mock_admin.return_value = MagicMock()
                    
                    # Extract the purge_queue function from the server
                    purge_queue_func = None
                    for name, func in server.mcp.tool.mock_calls:
                        if name == "()" and func[0].__name__ == "purge_queue":
                            purge_queue_func = func[0]
                            break
                    
                    assert purge_queue_func is not None, "Could not find purge_queue function"
                    
                    # Call the function directly
                    result = purge_queue_func("test_queue")
                    
                    mock_admin.assert_called_once_with(
                        "localhost", 15672, "guest", "guest", False
                    )
                    mock_handle_purge_queue.assert_called_once_with(mock_admin.return_value, "test_queue", "/")
                    assert "successfully purged" in result

    def test_delete_exchange(self, server):
        """Test the delete_exchange tool."""
        with patch("mcp_server_rabbitmq.server.RabbitMQAdmin") as mock_admin:
            with patch("mcp_server_rabbitmq.server.handle_delete_exchange") as mock_handle_delete_exchange:
                with patch("mcp_server_rabbitmq.server.validate_rabbitmq_name"):
                    mock_admin.return_value = MagicMock()
                    
                    # Extract the delete_exchange function from the server
                    delete_exchange_func = None
                    for name, func in server.mcp.tool.mock_calls:
                        if name == "()" and func[0].__name__ == "delete_exchange":
                            delete_exchange_func = func[0]
                            break
                    
                    assert delete_exchange_func is not None, "Could not find delete_exchange function"
                    
                    # Call the function directly
                    result = delete_exchange_func("test_exchange")
                    
                    mock_admin.assert_called_once_with(
                        "localhost", 15672, "guest", "guest", False
                    )
                    mock_handle_delete_exchange.assert_called_once_with(mock_admin.return_value, "test_exchange", "/")
                    assert "successfully deleted" in result

    def test_get_exchange_info(self, server):
        """Test the get_exchange_info tool."""
        with patch("mcp_server_rabbitmq.server.RabbitMQAdmin") as mock_admin:
            with patch("mcp_server_rabbitmq.server.handle_get_exchange_info") as mock_handle_get_exchange_info:
                with patch("mcp_server_rabbitmq.server.validate_rabbitmq_name"):
                    mock_admin.return_value = MagicMock()
                    mock_handle_get_exchange_info.return_value = {"name": "test_exchange", "type": "fanout"}
                    
                    # Extract the get_exchange_info function from the server
                    get_exchange_info_func = None
                    for name, func in server.mcp.tool.mock_calls:
                        if name == "()" and func[0].__name__ == "get_exchange_info":
                            get_exchange_info_func = func[0]
                            break
                    
                    assert get_exchange_info_func is not None, "Could not find get_exchange_info function"
                    
                    # Call the function directly
                    result = get_exchange_info_func("test_exchange")
                    
                    mock_admin.assert_called_once_with(
                        "localhost", 15672, "guest", "guest", False
                    )
                    mock_handle_get_exchange_info.assert_called_once_with(mock_admin.return_value, "test_exchange", "/")
                    assert "{'name': 'test_exchange', 'type': 'fanout'}" == result

    def test_validate_rabbitmq_name_called(self, server):
        """Test that validate_rabbitmq_name is called for relevant functions."""
        with patch("mcp_server_rabbitmq.server.validate_rabbitmq_name") as mock_validate:
            with patch("mcp_server_rabbitmq.server.RabbitMQConnection"):
                with patch("mcp_server_rabbitmq.server.handle_enqueue"):
                    # Extract the enqueue function from the server
                    enqueue_func = None
                    for name, func in server.mcp.tool.mock_calls:
                        if name == "()" and func[0].__name__ == "enqueue":
                            enqueue_func = func[0]
                            break
                    
                    assert enqueue_func is not None, "Could not find enqueue function"
                    
                    # Call the function directly
                    enqueue_func("test_queue", "test_message")
                    mock_validate.assert_called_with("test_queue", "Queue name")

            mock_validate.reset_mock()
            
            with patch("mcp_server_rabbitmq.server.RabbitMQConnection"):
                with patch("mcp_server_rabbitmq.server.handle_fanout"):
                    # Extract the fanout function from the server
                    fanout_func = None
                    for name, func in server.mcp.tool.mock_calls:
                        if name == "()" and func[0].__name__ == "fanout":
                            fanout_func = func[0]
                            break
                    
                    assert fanout_func is not None, "Could not find fanout function"
                    
                    # Call the function directly
                    fanout_func("test_exchange", "test_message")
                    mock_validate.assert_called_with("test_exchange", "Exchange name")