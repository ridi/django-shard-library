

class ConHashNode:
    def __init__(self, hash_value: int, index: int):
        self.hash_value = hash_value
        self.index = index

    def __str__(self) -> str:
        return f"{self.index}:{self.hash_value}"
