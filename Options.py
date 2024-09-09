@staticmethod
def get_help_options():
    return ["help", "-h", "--help", "?"]


@staticmethod
def get_exit_options():
    return ["exit", "ex", "-q", "-ex"]


@staticmethod
def get_yes_options():
    return ["yes", "y", "да", "нуы", "н"]


@staticmethod
def get_no_options():
    return ["no", "n", "тщ", "т"]

@staticmethod
def get_units_options():
    return ['bytes', 'KB', 'MB', 'GB']
