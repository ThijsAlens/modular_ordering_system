import unittest

# -- stuff to run tests from the test directory -- #
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
print(parent_dir)
sys.path.append(parent_dir)
# ------------------------------------------------ #

class TestBackEnd(unittest.TestCase):
    # ==================================================== #
    # MODEL TESTS
    # ==================================================== #
    def test_model_creation(self):
        from back_end.model.product import Product
        from back_end.model.order import Order
        from back_end.model.item import Item
        from back_end.model.ticket import Ticket

        from back_end.enums.product_group import Product_group
        from back_end.enums.destination import Destination
        from back_end.enums.ticket_status import Ticket_status
        from back_end.enums.order_status import Order_status

        try:
            p1 = Product(product_id=1, name="test_p1", price=5.0, destination=Destination.KITCHEN, group=Product_group.FOOD, is_active=True)
        except Exception as e:
            self.fail(f"Failed to create product: {e}")
        
        try:
            i1 = Item(product=p1, comment="test_item")
        except Exception as e:
            self.fail(f"Failed to create item: {e}")

        try:
            t1 = Ticket(ticket_id=1, order_id=1, destination=Destination.KITCHEN, status=Ticket_status.PENDING, items=[i1], comment="test_ticket")
        except Exception as e:
            self.fail(f"Failed to create ticket: {e}")

        try:
            o1 = Order(order_id=1, table_reference="1", tickets=[t1], status=Order_status.ACTIVE)
        except Exception as e:
            self.fail(f"Failed to create order: {e}")

        return
    
    def test_serialization_and_deserialization(self):
        from back_end.model.product import Product
        from back_end.model.order import Order
        from back_end.model.item import Item
        from back_end.model.ticket import Ticket

        from back_end.enums.product_group import Product_group
        from back_end.enums.destination import Destination
        from back_end.enums.ticket_status import Ticket_status
        from back_end.enums.order_status import Order_status

        p1 = Product(product_id=1, name="test_p1", price=5.0, destination=Destination.KITCHEN, group=Product_group.FOOD, is_active=True)
        i1 = Item(product=p1, comment="test_item")
        t1 = Ticket(ticket_id=1, order_id=1, destination=Destination.KITCHEN, status=Ticket_status.PENDING, items=[i1], comment="test_ticket")
        o1 = Order(order_id=1, table_reference="1", tickets=[t1], status=Order_status.ACTIVE)

        serialized_order = o1.serialize()
        deserialized_order = Order.deserialize(serialized_order)

        self.assertEqual(o1.get_order_id(), deserialized_order.get_order_id())
        self.assertEqual(o1.get_table_reference(), deserialized_order.get_table_reference())
        self.assertEqual(o1.get_status(), deserialized_order.get_status())
        self.assertEqual(len(o1.get_tickets()), len(deserialized_order.get_tickets()))
        return
    
    def test_methods(self):
        from back_end.model.product import Product
        from back_end.model.order import Order
        from back_end.model.item import Item
        from back_end.model.ticket import Ticket

        from back_end.enums.product_group import Product_group
        from back_end.enums.destination import Destination
        from back_end.enums.ticket_status import Ticket_status
        from back_end.enums.order_status import Order_status

        p1 = Product(product_id=1, name="test_p1", price=5.0, destination=Destination.KITCHEN, group=Product_group.FOOD, is_active=True)
        i1 = Item(product=p1, comment="test_item")
        t1 = Ticket(ticket_id=1, order_id=1, destination=Destination.KITCHEN, status=Ticket_status.PENDING, items=[i1], comment="test_ticket")
        o1 = Order(order_id=1, table_reference="12", tickets=[t1], status=Order_status.ACTIVE)

        # Test product getters
        self.assertEqual(p1.get_product_id(), 1)
        self.assertEqual(p1.get_name(), "test_p1")
        self.assertEqual(p1.get_price(), 5.0)
        self.assertEqual(p1.get_destination(), Destination.KITCHEN)
        self.assertEqual(p1.get_group(), Product_group.FOOD)
        self.assertEqual(p1.get_is_active(), True)

        # Test product setters
        p1.deactivate()
        self.assertEqual(p1.get_is_active(), False)
        p1.activate()

        # Test item getters
        self.assertEqual(i1.get_product().get_product_id(), 1)
        self.assertEqual(i1.get_comment(), "test_item")

        # Test item setters
        i1.set_comment("updated_item_comment")
        self.assertEqual(i1.get_comment(), "updated_item_comment")

        # Test ticket getters
        self.assertEqual(t1.get_ticket_id(), 1)
        self.assertEqual(t1.get_order_id(), 1)
        self.assertEqual(t1.get_destination(), Destination.KITCHEN)
        self.assertEqual(t1.get_status(), Ticket_status.PENDING)
        self.assertEqual(len(t1.get_items()), 1)
        self.assertEqual(t1.get_items()[0].get_product().get_product_id(), 1)
        self.assertEqual(t1.get_comment(), "test_ticket")

        # Test ticket setters
        t1.set_status(Ticket_status.COMPLETED)
        self.assertEqual(t1.get_status(), Ticket_status.COMPLETED)
        t1.set_status(Ticket_status.PENDING)
        t1.set_comment("updated_comment")
        self.assertEqual(t1.get_comment(), "updated_comment")
        i2 = Item(product=p1, comment="second_item")
        t1.add_item(i2)
        self.assertEqual(len(t1.get_items()), 2)

        # Test order getters
        self.assertEqual(o1.get_order_id(), 1)
        self.assertEqual(o1.get_table_reference(), "12")
        self.assertEqual(o1.get_status(), Order_status.ACTIVE)
        self.assertEqual(len(o1.get_tickets()), 1)
        self.assertEqual(o1.get_tickets()[0].get_ticket_id(), 1)

        # Test order setters
        o1.set_status(Order_status.CANCELED)
        self.assertEqual(o1.get_status(), Order_status.CANCELED)
        o1.set_status(Order_status.ACTIVE)
        t2 = Ticket(ticket_id=2, order_id=1, destination=Destination.BAR, status=Ticket_status.PENDING, items=[], comment="second_ticket")
        o1.add_ticket(t2)
        self.assertEqual(len(o1.get_tickets()), 2)
        return
    
    # ==================================================== #
    # REST API TESTS
    # ==================================================== #
    
    def test_REST_API_order_related_endpoints(self):
        import requests
        base_url = "http://127.0.0.1:8000"

        from back_end.model.order import Order
        from back_end.enums.order_status import Order_status
        from back_end.enums.destination import Destination
        from back_end.model.ticket import Ticket

        # 1. Get order by ID (non-existing)
        response = requests.get(f"{base_url}/get_order_by_id", params={"order_id": 0})
        self.assertEqual(response.status_code, 200)
        response_body = response.json()
        self.assertEqual(response_body["error"], "Order with ID 0 not found.")

        # 2. Create new order
        response = requests.post(f"{base_url}/create_new_order", params={"table_reference": "5"})
        self.assertEqual(response.status_code, 200)
        response_body = response.json()
        try:
            response_order = Order.deserialize(response_body)
        except Exception as e:
            self.fail(f"Deserialization failed: {e}")
        self.assertEqual(response_order.get_order_id(), 0)
        self.assertEqual(response_order.get_table_reference(), "5")
        self.assertEqual(response_order.get_status(), Order_status.ACTIVE)
        self.assertEqual(len(response_order.get_tickets()), 0)

        # 3. Get order by ID (existing)
        response = requests.get(f"{base_url}/get_order_by_id", params={"order_id": 0})
        self.assertEqual(response.status_code, 200)
        response_body = response.json()
        try:
            response_order = Order.deserialize(response_body)
        except Exception as e:
            self.fail(f"Deserialization failed: {e}")
        self.assertEqual(response_order.get_order_id(), 0)
        self.assertEqual(response_order.get_table_reference(), "5")
        self.assertEqual(response_order.get_status(), Order_status.ACTIVE)
        self.assertEqual(len(response_order.get_tickets()), 0)

        # 4. Change order status (non-existing)
        response = requests.post(f"{base_url}/change_order_status", params={"order_id": 0, "new_status": Order_status.CANCELED})
        self.assertEqual(response.status_code, 200)
        response_body = response.json()
        self.assertEqual(response_body["error"], "Order with ID 0 not found.")

        # 5. Change order status (existing)
        response = requests.post(f"{base_url}/change_order_status", params={"order_id": 0, "new_status": Order_status.CANCELED})
        self.assertEqual(response.status_code, 200)
        response_body = response.json()
        self.assertEqual(response_body["message"], "Order with ID 0 status changed to Order_status.CANCELED.")

        # 6. Add ticket to order (non-existing order)
        new_ticket = Ticket(ticket_id=0, order_id=1, destination=Destination.KITCHEN, items=[])
        response = requests.post(f"{base_url}/add_ticket_to_order", params={"ticket": new_ticket.serialize()})
        self.assertEqual(response.status_code, 200)
        response_body = response.json()
        self.assertEqual(response_body["error"], "Order with ID 1 not found.")

        # 7. Add ticket to order (existing order)
        new_ticket = Ticket(ticket_id=0, order_id=0, destination=Destination.KITCHEN, items=[])
        response = requests.post(f"{base_url}/add_ticket_to_order", params={"ticket": new_ticket.serialize()})
        self.assertEqual(response.status_code, 200)
        response_body = response.json()
        self.assertEqual(response_body["message"], "Ticket with ID 0 added to order with ID 0.")
        return
    
    def test_REST_API_ticket_related_endpoints(self):
        import requests
        base_url = "http://127.0.0.1:8000"

        from back_end.enums.destination import Destination
        from back_end.model.ticket import Ticket

        # 1. Create new empty ticket
        response = requests.get(f"{base_url}/create_new_empty_ticket", params={"order_id": 0, "destination": Destination.KITCHEN})
        self.assertEqual(response.status_code, 200)
        response_body = response.json()
        try:
            new_ticket = Ticket.deserialize(response_body)
        except Exception as e:
            self.fail(f"Deserialization failed: {e}")
        self.assertEqual(new_ticket.get_ticket_id(), 0)
        self.assertEqual(new_ticket.get_order_id(), 0)
        self.assertEqual(new_ticket.get_destination(), Destination.KITCHEN)
        self.assertEqual(len(new_ticket.get_items()), 0)
        self.assertEqual(new_ticket.get_comment(), "")

        # 2. Add pending ticket
        response = requests.post(f"{base_url}/add_pending_ticket", params={"ticket": new_ticket.serialize()})
        self.assertEqual(response.status_code, 200)
        response_body = response.json()
        self.assertEqual(response_body["message"], "Ticket with ID 0 added to pending tickets.")

        # __ create an order and add some tickets to it first __ #
        order_response = requests.post(f"{base_url}/create_new_order", params={"table_reference": "10"}).json()
        t1 = Ticket.deserialize(requests.post(f"{base_url}/create_new_empty_ticket", params={"order_id": order_response["order_id"], "destination": Destination.BAR}).json())
        t2 = Ticket.deserialize(requests.post(f"{base_url}/create_new_empty_ticket", params={"order_id": order_response["order_id"], "destination": Destination.BAR}).json())
        requests.post(f"{base_url}/add_ticket_to_order", params={"ticket": t1.serialize()})
        requests.post(f"{base_url}/add_ticket_to_order", params={"ticket": t2.serialize()})

        # 3. Get all pending tickets by order ID
        response = requests.get(f"{base_url}/get_all_pending_tickets_by_order_id", params={"order_id": order_response["order_id"]})
        self.assertEqual(response.status_code, 200)
        response_body = response.json()
        self.assertTrue(isinstance(response_body, list))
        for ticket_data in response_body:
            try:
                response_ticket = Ticket.deserialize(ticket_data)
            except Exception as e:
                self.fail(f"Deserialization failed: {e}")
            self.assertEqual(response_ticket.get_order_id(), order_response["order_id"])

        # 4. Get all pending tickets by destination
        response = requests.get(f"{base_url}/get_all_pending_tickets_by_destination", params={"destination": Destination.BAR})
        self.assertEqual(response.status_code, 200)
        response_body = response.json()
        self.assertTrue(isinstance(response_body, list))
        for ticket_data in response_body:
            try:
                response_ticket = Ticket.deserialize(ticket_data)
            except Exception as e:
                self.fail(f"Deserialization failed: {e}")
            self.assertEqual(response_ticket.get_destination(), Destination.BAR)

        # 5. Get pending ticket by ID (non-existing)
        response = requests.get(f"{base_url}/get_pending_ticket_by_id", params={"ticket_id": 999})
        self.assertEqual(response.status_code, 200)
        response_body = response.json()
        self.assertEqual(response_body["error"], "Ticket with ID 999 not found in pending tickets.")

        # 6. Get pending ticket by ID (existing)
        response = requests.get(f"{base_url}/get_pending_ticket_by_id", params={"ticket_id": new_ticket.get_ticket_id()})
        self.assertEqual(response.status_code, 200)
        response_body = response.json()
        try:
            response_ticket = Ticket.deserialize(response_body)
        except Exception as e:
            self.fail(f"Deserialization failed: {e}")
        self.assertEqual(response_ticket.get_ticket_id(), new_ticket.get_ticket_id())
        self.assertEqual(response_ticket.get_order_id(), new_ticket.get_order_id())
        return



if __name__ == '__main__':
    unittest.main()