class HelpFormatter:
    _max_chars = 72

    def __init__(self, tokens: list, parsed_commands: list, title="try the following commands:",):
        self.title = title
        self.tokens = tokens
        if len(parsed_commands) >= 1 and parsed_commands[-1] == 'help':
            self.parsed_commands = parsed_commands[:-1]
        elif len(parsed_commands) >= 1:
            self.parsed_commands = parsed_commands
        else:
            self.parsed_commands = []

    def __str__(self):
        cmd = " ".join(self.parsed_commands)
        _str = f'{self.title}\n\t{cmd} ['

        token_count = len(self.tokens)
        for i in range(token_count):
            token = f' {self.tokens[i]} '
            if i == token_count - 1:
                token += ']'
            else:
                token += '|'

            current_line = _str.split('\n')[-1]
            if len(current_line + token) < HelpFormatter._max_chars:
                _str += token
            else:
                _str += f'\n\t {"".join([" " for _ in cmd])}{token}'
        return _str

