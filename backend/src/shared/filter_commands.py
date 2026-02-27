

import datetime
from datetime import date


class CheckinFilterCommand():
    """Command object for filtering check-ins."""
    def __init__(self, offset: int = 0, limit: int = 10, from_date: date = None, to_date: date = None):
        self.offset = offset
        self.limit = limit
        self.from_date = from_date
        self.to_date = to_date
        

def validate_checkin_filter_command(command: CheckinFilterCommand):
    """Validate the filter command."""
    if command.offset < 0:
        return False
    if command.limit <= 0:
        return False
    if command.from_date and not isinstance(command.from_date, date):
        return False
    if command.to_date and not isinstance(command.to_date, date):
        return False
    if command.from_date and command.to_date and command.from_date > command.to_date:
        return False
    return True