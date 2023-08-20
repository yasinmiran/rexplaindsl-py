class Expression:

    def __init__(self, func):
        self.func = func

    def to_regex(self) -> str:
        return self.func()

    def __call__(self):
        return self.to_regex()

    def debug(self, callback) -> 'Expression':
        callback(self.to_regex())
        return self
