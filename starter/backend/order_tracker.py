# This module contains the OrderTracker class, which encapsulates the core
# business logic for managing orders.

class OrderTracker:
    """
    Manages customer orders, providing functionalities to add, update,
    and retrieve order information.
    """
    def __init__(self, storage):
        required_methods = ['save_order', 'get_order', 'get_all_orders']
        for method in required_methods:
            if not hasattr(storage, method) or not callable(getattr(storage, method)):
                raise TypeError(f"Storage object must implement a callable '{method}' method.")
        self.storage = storage

    def add_order(self, order_id: str, item_name: str, quantity: int, customer_id: str, status: str = "pending"):
        statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
        order_data = {                                                                                                                                                            
            "order_id": order_id,
            "item_name": item_name,                                                                                                                                               
            "quantity": quantity,                                                                                                                                               
            "customer_id": customer_id,
            "status": status                        
        }     
        if quantity < 1:
            raise ValueError(f"Invalid quantity. It should be >= 1")
        if status not in statuses:
            raise ValueError(f"Invalid status. It should be one of: pending, processing, shipped, delivered, cancelled")
        if self.storage.get_order(order_id):
            raise ValueError(f"Order with ID '{order_id}' already exists.")
        self.storage.save_order(order_id, order_data)

    def get_order_by_id(self, order_id: str):
        if order_id == "":
            raise ValueError(f"Order with ID cannot be empty")
        return self.storage.get_order(order_id)

    def update_order_status(self, order_id: str, new_status: str):
        statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
        if order_id == "":
            raise ValueError("Order with ID cannot be empty")
        if new_status not in statuses:
            raise ValueError(f"Status {new_status} is invalid. Valid statuses: {statuses}")
        order_data = self.get_order_by_id(order_id)
        if order_data is None:
            raise ValueError(f"Order ID {order_id} does not exist")
        order_data["status"] = new_status
        self.storage.save_order(order_id, order_data)

    def list_all_orders(self):
        return list(self.storage.get_all_orders().values())
        

    def list_orders_by_status(self, status: str):
        statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
        if status == "":
            raise ValueError("Status cannot be empty.")
        if status not in statuses:
            raise ValueError(f"Status {status} is invalid.")
        return [order for order in self.storage.get_all_orders().values() if order["status"] == status]

