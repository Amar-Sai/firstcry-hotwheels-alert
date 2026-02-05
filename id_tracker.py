import os

def load_last_product_id(path):
    if not os.path.exists(path):
        return 0
    with open(path, "r") as f:
        try:
            return int(f.read().strip())
        except ValueError:
            return 0

def save_last_product_id(path, product_id):
    with open(path, "w") as f:
        f.write(str(product_id))
