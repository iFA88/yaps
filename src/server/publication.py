class Publication:

    def __init__(self, topic: str, message: str):
        self.topic = topic
        self.message = message

    def __repr__(self):
        return f'{self.topic}: {self.message}'
