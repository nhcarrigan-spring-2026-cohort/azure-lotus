from enum import Enum


class UserRole(str, Enum):
    FAMILY = "family"
    VOLUNTEER = "volunteer"
    SENIOR = "senior"


class CheckInStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    MISSED = "missed"


class CheckInMethod(str, Enum):
    SELF = "self"
    VOLUNTEER = "volunteer"
    SYSTEM = "system"
    
class InvitationStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    EXPIRED = "expired"
