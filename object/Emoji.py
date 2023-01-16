class Emoji:
    def __init__(self, emoji):
        # print(emoji)
        self.emoji = emoji
        self.template = {"emoji": self.emoji} if isinstance(self.emoji, str) else None

    def update(self, emoji) -> dict:
        self.emoji = emoji
        self.template["emoji"] = self.emoji
        return self.template

    def make(self) -> dict:
        return self.template
