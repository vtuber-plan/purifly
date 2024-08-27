class UnwrapException(Exception):
    msg: str

    def __init__(self, msg: str):
        super().__init__(self)
        self.msg = msg

    def __str__(self):
        return f'OptionError: {self.msg}'
