import unittest

# -- stuff to run tests from the test directory --
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
print(parent_dir)
sys.path.append(parent_dir)
# --------------------------------------------------

class TestBackEnd(unittest.TestCase):
    def test_creation(self):
        from back_end.model.product import Product
        from back_end.model.order import Order
        from back_end.model.item import Item
        from back_end.model.ticket import Ticket

        from back_end.enums.product_group import Product_group
        from back_end.enums.destination import Destination
        from back_end.enums.ticket_status import Ticket_status
        from back_end.enums.order_status import Order_status

        try:
            p1 = Product(id=1, name="test_p1", price=5.0, destination=Destination.KITCHEN, group=Product_group.FOOD, is_active=True)
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
            o1 = Order(order_id=1, table_number=1, tickets=[t1], status=Order_status.ACTIVE)
        except Exception as e:
            self.fail(f"Failed to create order: {e}")

        return
    
    def test_serialization(self):
        from back_end.model.product import Product
        from back_end.model.order import Order
        from back_end.model.item import Item
        from back_end.model.ticket import Ticket

        from back_end.enums.product_group import Product_group
        from back_end.enums.destination import Destination
        from back_end.enums.ticket_status import Ticket_status
        from back_end.enums.order_status import Order_status

        p1 = Product(id=1, name="test_p1", price=5.0, destination=Destination.KITCHEN, group=Product_group.FOOD, is_active=True)
        i1 = Item(product=p1, comment="test_item")
        t1 = Ticket(ticket_id=1, order_id=1, destination=Destination.KITCHEN, status=Ticket_status.PENDING, items=[i1], comment="test_ticket")
        o1 = Order(order_id=1, table_number=1, tickets=[t1], status=Order_status.ACTIVE)

        serialized_order = o1.serialize()
        deserialized_order = Order.deserialize(serialized_order)

        self.assertEqual(o1.get_id(), deserialized_order.get_id())
        self.assertEqual(o1.get_table_reference(), deserialized_order.get_table_reference())
        self.assertEqual(o1.get_status(), deserialized_order.get_status())
        self.assertEqual(len(o1.get_tickets()), len(deserialized_order.get_tickets()))
        return


if __name__ == '__main__':
    unittest.main()