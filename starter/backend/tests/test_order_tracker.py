import pytest
from unittest.mock import Mock
from ..order_tracker import OrderTracker

# --- Fixtures for Unit Tests ---

@pytest.fixture
def mock_storage():
    """
    Provides a mock storage object for tests.
    This mock will be configured to simulate various storage behaviors.
    """
    mock = Mock()
    # By default, mock get_order to return None (no order found)
    mock.get_order.return_value = None
    # By default, mock get_all_orders to return an empty dict
    mock.get_all_orders.return_value = {}
    return mock

@pytest.fixture
def order_tracker(mock_storage):
    """
    Provides an OrderTracker instance initialized with the mock_storage.
    """
    return OrderTracker(mock_storage)

#
# --- TODO: add test functions below this line ---
#

def test_add_order_successfully(order_tracker, mock_storage):
    """Tests adding a new order with default 'pending' status."""
    order_tracker.add_order("ORD001", "Laptop", 1, "CUST001")
    
    # We expect save_order to be called once
    mock_storage.save_order.assert_called_once()

def test_add_order_stores_correct_details(order_tracker, mock_storage):
    """Tests adding a new order with default 'pending' status."""
    order_tracker.add_order("ORD002", "Mouse", 1, "CUST001")

    mock_storage.save_order.assert_called_once_with("ORD002", {                                                                                                               
      "order_id": "ORD002",                                                                                                                                                 
      "item_name": "Mouse",                                                                                                                                                 
      "quantity": 1,                                                                                                                                                        
      "customer_id": "CUST001",                                                                                                                                             
      "status": "pending"                                                                                                                                                   
    })     

@pytest.mark.parametrize("quantity", [-1,0])
def test_add_order_invalid_quantity(order_tracker, quantity):
    """Tests adding a new order with default 'pending' status."""
    with pytest.raises(ValueError, match="Invalid quantity. It should be >= 1"):
        order_tracker.add_order("ORD001", "Laptop", quantity, "CUST001")

@pytest.mark.parametrize("status", ["crazy","bananas"])
def test_add_order_invalid_status(order_tracker, status):
    """Tests adding a new order with default 'pending' status."""
    with pytest.raises(ValueError, match="Invalid status. It should be one of: pending, processing, shipped, delivered, cancelled"):
        order_tracker.add_order("ORD001", "Laptop", 1, "CUST001", status)

def test_add_order_raises_error_if_exists(order_tracker, mock_storage):
    """Tests that adding an order with a duplicate ID raises a ValueError."""
    # Simulate that the storage finds an existing order
    mock_storage.get_order.return_value = {"order_id": "ORD_EXISTING"}

    with pytest.raises(ValueError, match="Order with ID 'ORD_EXISTING' already exists."):
        order_tracker.add_order("ORD_EXISTING", "New Item", 1, "CUST001")

def test_get_order_by_id(order_tracker, mock_storage):
    #Arrange
    mock_storage.get_order.return_value = {"order_id": "ORD002", "item_name": "Headphones", "quantity": 1, "customer_id": "CUST123", "status": "pending"}
    #Act
    result = order_tracker.get_order_by_id("ORD002")
    #Assert
    assert result == {"order_id": "ORD002", "item_name": "Headphones", "quantity": 1, "customer_id": "CUST123", "status": "pending"}

def test_get_order_by_id_not_exists(order_tracker):
    result = order_tracker.get_order_by_id("ORD001")
    assert result == None

def test_get_order_by_id_empty(order_tracker):
    with pytest.raises(ValueError, match="Order with ID cannot be empty"):
        order_tracker.get_order_by_id("")

def test_update_order_status(order_tracker, mock_storage):
    #Arrange
    mock_storage.get_order.return_value = {"order_id": "ORD002", "item_name": "Headphones", "quantity": 1, "customer_id": "CUST123", "status": "pending"}
    #Act
    order_tracker.update_order_status("ORD002","shipped")
    #Assert
    mock_storage.save_order.assert_called_once_with("ORD002", {                                                                                                               
        "order_id": "ORD002",                                                                                                                                                 
        "item_name": "Headphones",                                                                                                                                            
        "quantity": 1,                                                                                                                                                        
        "customer_id": "CUST123",                                                                                                                                           
        "status": "shipped"
    })   

def test_update_non_existent_order_status(order_tracker):
    #Arrange (Nothing since Im trying to update a non existing order)
    #Act
    order_id = "ORD007"
    with pytest.raises(ValueError, match=f"Order ID {order_id} does not exist"):
        order_tracker.update_order_status(order_id,"shipped")

def test_update_order_status_empty_id(order_tracker):
    with pytest.raises(ValueError, match="Order with ID cannot be empty"):
        order_tracker.update_order_status("","shipped")

def test_update_order_invalid_status(order_tracker):
    new_status="banana"
    statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
    with pytest.raises(ValueError, match=f"Status {new_status} is invalid."):
        order_tracker.update_order_status("ORD007",new_status)

def test_list_all_orders(order_tracker, mock_storage):
    #Arrange
    mock_storage.get_all_orders.return_value = {                                                                                                                              
        "ORD001": {"order_id": "ORD001", "item_name": "Laptop", "quantity": 1, "customer_id": "CUST001", "status": "pending"},                                              
        "ORD002": {"order_id": "ORD002", "item_name": "Mouse", "quantity": 2, "customer_id": "CUST002", "status": "shipped"}                                                  
    }
    #Act
    result = order_tracker.list_all_orders()
    #Assert
    assert result == [
        {"order_id": "ORD001", "item_name": "Laptop", "quantity": 1, "customer_id": "CUST001", "status": "pending"},
        {"order_id": "ORD002", "item_name": "Mouse", "quantity": 2, "customer_id": "CUST002", "status": "shipped"}
    ]


def test_list_all_orders_empty_storage(order_tracker):
    #Arrange
    #By default mock already returns empty dict for mock_storage.get_all_orders
    #Act
    result = order_tracker.list_all_orders()
    #Assert
    assert result == []

@pytest.mark.parametrize("status", ["pending", "processing", "shipped", "delivered", "cancelled"])
def test_list_orders_by_status(order_tracker,mock_storage,status):
    #Arrange
    mock_storage.get_all_orders.return_value = {                                                                                                                              
      "ORD001": {"order_id": "ORD001", "item_name": "Laptop", "quantity": 1, "customer_id": "CUST001", "status": "pending"},                                              
      "ORD002": {"order_id": "ORD002", "item_name": "Mouse", "quantity": 2, "customer_id": "CUST002", "status": "shipped"},                                                 
      "ORD003": {"order_id": "ORD003", "item_name": "Keyboard", "quantity": 1, "customer_id": "CUST003", "status": "pending"},                                              
      "ORD004": {"order_id": "ORD004", "item_name": "Monitor", "quantity": 1, "customer_id": "CUST001", "status": "processing"},                                            
      "ORD005": {"order_id": "ORD005", "item_name": "Webcam", "quantity": 3, "customer_id": "CUST002", "status": "delivered"},                                              
      "ORD006": {"order_id": "ORD006", "item_name": "Headphones", "quantity": 1, "customer_id": "CUST003", "status": "cancelled"}                                           
    }
    #Act
    #orders = list(mock_storage.get_all_orders.return_value.values())
    result = order_tracker.list_orders_by_status(status)
    #Assert
    assert result == [order for order in mock_storage.get_all_orders.return_value.values() if order["status"] == status] 

@pytest.mark.parametrize("status", ["pending", "processing", "shipped", "delivered", "cancelled"])
def test_list_all_orders_by_status_empty_storage(order_tracker,status):
    #Arrange
    #By default mock already returns empty dict for mock_storage.get_all_orders
    #Act
    result = order_tracker.list_orders_by_status(status)
    #Assert
    assert result == []


def test_list_all_orders_by_status_empty(order_tracker,mock_storage):
     #Arrange
    #Act
    with pytest.raises(ValueError, match=f"Status cannot be empty."):
        order_tracker.list_orders_by_status("")
    #Assert
    # Raise in lieu of assert

def test_list_all_orders_by_status_invalid(order_tracker,mock_storage):
    #Act
    status="banana"
    with pytest.raises(ValueError, match=f"Status {status} is invalid."):
        order_tracker.list_orders_by_status("banana")




















