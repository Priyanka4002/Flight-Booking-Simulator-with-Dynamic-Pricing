import random

def generate_transaction_id():
    return f"TXN{random.randint(1000,9999)}"
