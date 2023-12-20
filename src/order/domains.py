from enum import Enum


class OrderStatus(str, Enum):
    in_process = "В обработке"
    assembly = "Сборка"
    on_the_way = "В пути"
    received = "Получен"