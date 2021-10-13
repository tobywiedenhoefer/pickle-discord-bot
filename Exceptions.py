class ExceptionStrings:
    to_user = "An unexpected error occured. "
    to_console = "Unexpected exception:"
    to_user_on_message = to_user + "I'm not sure what you're sending."
    already_connected_to_vc = "Already connected to voice chat. If this is the incorrect vc, please type 'leave' and " \
                              "try again. "


class Error(Exception):
    """
    default template for custom exceptions
    """
    def __init__(self, message, message_for_user=None):
        self.message = message
        self.message_for_user = message_for_user
        super().__init__(self.message)

    def for_user(self):
        if not self.message_for_user:
            return self.message_for_user
        return self.message


class NotLongEnough(Error):
    """
    raise exception when message is not long enough.
    """
    def __init__(self,
                 message_sent,
                 channel_type="private",
                 error_message="message should be at least two characters long."):
        self.message_sent = message_sent
        self.channel_type = str(channel_type).capitalize()
        self.error_message = error_message
        self.message = f'{self.channel_type} {self.error_message}'
        super().__init__(self.message, self.__str__())

    def __str__(self):
        return f'"{self.message_sent}" should be at least two characters long.'


class NoneType(Error):
    def __init__(self, operation, variable_name, variable):
        self.message = f"Cannot {operation} when {variable_name} is '{variable}'."
        super().__init__(self.message)


class CouldNotConnectVC(Error):
    def __init__(self):
        self.message = f'Cannot connect to voice chat.'
