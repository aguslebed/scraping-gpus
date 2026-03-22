
class Prices:

    def __init__(self, gpu_id, price, date):
        self.gpu_id = gpu_id
        self.price = price
        self.date = date

    def get_obj(self):
        return {
            "gpu_id": self.gpu_id,
            "price": self.price,
            "date": self.date
        }
