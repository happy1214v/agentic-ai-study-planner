class Memory:
    def __init__(self):
        self.messages = []

    def add(self, message):
        self.messages.append(message)

    def get_all(self):
        return self.messages

    def get_recent(self, limit=5):
        if limit <= 0:
            return []

        return self.messages[-limit:]

    def search(self, keyword):
        keyword = keyword.lower().strip()

        if not keyword:
            return []

        return [
            message
            for message in self.messages
            if keyword in str(message).lower()
        ]

    def clear(self):
        self.messages.clear()