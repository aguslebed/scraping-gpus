class Gpu:
    def __init__(self, name,chipset, price, url, image_url, outlet, store):
        self.name = name
        self.chipset = chipset
        self.price = price
        self.url = url
        self.image_url = image_url
        self.outlet = outlet
        self.store = store
        
    def get_obj(self):
        return {
            "name": self.name,
            "chipset": self.chipset,
            "price": self.price,
            "url": self.url,
            "image_url": self.image_url,
            "outlet": self.outlet,
            "store": self.store
        }