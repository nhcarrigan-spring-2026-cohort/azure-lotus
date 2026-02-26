

import datetime


class CheckinFilterCommand():
    """ Command object for filtering check-ins. """
    def __init__(self, offset: int = 0, limit: int = 10, from_date: str = None, to_date: str = None):
        self.offset = offset
        self.limit = limit
        self.from_date = from_date
        self.to_date = to_date
        

def validate_checkin_filter_command(command: CheckinFilterCommand):
    """ Validate the filter command. """
    def validate_date(date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    if command.offset < 0:
        return False
    if command.limit <= 0:
        return False
    if command.from_date and not validate_date(command.from_date):
        return False
    if command.to_date and not validate_date(command.to_date):
        return False
    if command.from_date and command.to_date and command.from_date > command.to_date:
        return False
    return True