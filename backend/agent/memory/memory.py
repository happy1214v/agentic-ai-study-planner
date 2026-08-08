class Memory:
    def __init__(self):
        self.messages = []

    def add(self, message):
        self.messages.append(message)

    def get_all(self):
        return self.messages

    def get_recent(self, limit=5):
        return self.messages[-limit:]

    def clear(self):
        self.messages.clear()


    