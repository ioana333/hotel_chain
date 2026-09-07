class RoomID:
    def __init__(self, value: int):
        self.value = int(value)

    def __int__(self) -> int:
        return self.value

    def __repr__(self) -> str:
        return f"RoomID({self.value})"
