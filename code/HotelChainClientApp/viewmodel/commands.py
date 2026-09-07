class Command:
    """Command comportamental folosit de interfața grafică pentru acțiunile butoanelor."""
    def __init__(self, action, can_execute=lambda: True):
        self.action = action
        self.can_execute = can_execute

    def execute(self):
        if self.can_execute():
            return self.action()
        return None
