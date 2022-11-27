import random
import string
from datetime import datetime
from uuid import uuid4

from purchasing_manager.domain.models.client import Client


def generate_random_strings(length: int):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def generate_random_numbers(length: int):
    numbers = range(0, 10)
    return "".join(str(random.choice(numbers)) for i in range(length))


def generate_clients_objects(qtd: int):
    clients = []
    for i in range(qtd):
        clients.append(
            Client(
                id=str(uuid4()),
                created_dt=datetime.now(),
                updated_dt=datetime.now(),
                name=generate_random_strings(5),
                document=generate_random_numbers(11),
                phone=generate_random_numbers(11),
                email=f"{generate_random_strings(10)}@example.com",
            )
        )

    return clients
