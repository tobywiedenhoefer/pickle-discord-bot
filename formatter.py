class HelpFormatter:
    def __init__(self, title: str):
        self.title = title
        self.positional_args = ''
        self.optional_args = ''

    def add_tite(self, title: str):
        self.title = title

    def add_positional_args(self, pos_args: list):
        # positional args take the form:
        # [ ["{option1, option2}", "description"], ...]
        for pos_arg in pos_args:
            choices, description = pos_arg[0], pos_arg[1]
            self.positional_args += f'\t{choices}\t{description}\n'

    def add_optional_args(self, opt_args: list):
        # optional args take the form:
        # [ ["{-f, --flag}, description, default], ...]
        for opt_arg in opt_args:
            flags, description, default = opt_arg[0], opt_arg[1], opt_arg[2]
            self.positional_args += f'\t{flags}\t{description}\t{default}'

    def __str__(self):
        return f'{self.title}\n' \
               f'positional arguments:' \
               f'{self.positional_args}\n' \
               f'optional arguments:' \
               f'{self.optional_args}'