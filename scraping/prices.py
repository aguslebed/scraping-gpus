
class Prices:

    def __init__(self, gpu_id, price, date, store):
        self.gpu_id = gpu_id
        self.price = price
        self.date = date
        self.store = store

    def get_obj(self):
        return {
            "gpu_id": self.gpu_id,
            "price": self.price,
            "date": self.date,
            "store": self.store
        }
