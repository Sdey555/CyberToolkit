class Core_Exception(Exception):
    pass

class InvalidOption(Core_Exception):
    def __init__(self):
        super().__init__(
            "You have enterd invalid option! Please try again."
        )