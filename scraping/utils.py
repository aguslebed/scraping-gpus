def find_chipset(name):
    splited_name = name.split()
    for i in splited_name:
        if i == "RTX" or i == "GTX" or i == "RX":
            return i + " " + splited_name[splited_name.index(i) + 1]
        if i == "Intel":
            return i + " " + splited_name[splited_name.index(i) + 1] + " " + splited_name[splited_name.index(i) + 2]
    return None

    """Separa el objeto gpu en dos objetos, uno para precios y otro para gpus"""

def split_price(gpu):
    return {
        "price": gpu.price,
        "date": gpu.last_update,
        "store": gpu.store
    }, {
        "name": gpu.name,
        "chipset": gpu.chipset,
        "url": gpu.url,
        "image_url": gpu.image_url,
        "outlet": gpu.outlet,
        "store": gpu.store,
        "last_update": gpu.last_update
    }