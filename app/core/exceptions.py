class ProductNotFoundException(Exception):
    def __init__(self,product_id:int):
        self.product_id=product_id

class OrderNotFoundException(Exception):
    def __init__(self,order_id:int):
        self.order_id=order_id

class InsufficientStockException(Exception):
    def __init__(self,prodcut_id:int):
        self.product_id=self.product_id