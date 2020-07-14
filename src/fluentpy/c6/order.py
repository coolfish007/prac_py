from collections import namedtuple

Customer = namedtuple("Customer", "name fidelity")


class LineItem:
    def __init__(self, product, quantity, price) -> None:
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


class Order:
    def __init__(self, customer, cart, promotion=None) -> None:
        self.customer = customer
        self.cart = cart
        self.promotion = promotion

    def total(self):
        if not hasattr(self, "__total"):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)
        return self.total() - discount

    def __repr__(self):
        fmt = "<Order total:{:.2f} due: {:.2f}>"
        return fmt.format(self.total(), self.due())


def fidelity_promo(order):
    print(f"fidelity:{order.customer.fidelity}")
    return order.total() * 0.05 if order.customer.fidelity >= 1000 else 0
