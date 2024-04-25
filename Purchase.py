import uuid
from CartDAO import CartDAO
from ItemDAO import ItemDAO
from OrderDAO import OrderDAO

class Purchase:
    def __init__(self):
        self.cart_dao = CartDAO()
        self.item_dao = ItemDAO()
        self.order_dao = OrderDAO()

    def makepurchase(self, buyer_id, payment_method):
        try:
            cart_id = self.cart_dao.get_cart(buyer_id)
            cart_items = self.cart_dao.get_cart_items(cart_id)
            transaction_id = self.order(buyer_id, cart_items,payment_method)
            return transaction_id
        except Exception as e:
            print("Error occurred during purchase:", str(e))
            return ""

    def order(self, buyer_id, cart_items,payment_method):
        transaction_id = str(uuid.uuid4())
        price = 0
        for cart_item in cart_items:
            item = self.item_dao.get_item(cart_item.item_id)
            price += item.sale_price * cart_item.quantity
            if item.quantity < cart_item.quantity:
                print("Some items do not exist in store")
                return ""

        transaction_id = self.order_dao.create_order(buyer_id, "IN_PROGRESS", transaction_id)

        for cart_item in cart_items:
            if self.item_dao.update_item_quantity(cart_item.item_id, cart_item.quantity):
                self.order_dao.update_order_item(transaction_id, cart_item.quantity, cart_item.item_id)
            else:
                print("Could not update quantity")
                return ""

        status = self.process_transaction(transaction_id, price,payment_method)
        self.order_dao.update_order(status, transaction_id)
        return transaction_id

    def process_transaction(self, transaction_id, price,payment_method):
        # Mocking S
        if payment_method!="PHONEPE":
            return "SUCCESS"
        return "FAIL"
