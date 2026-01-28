class DomainError(Exception):
    """Base class for domain-level errors."""
    pass


class StudentNotFoundError(DomainError):
    pass

class CourseListEmptyError(DomainError):
    pass


class CourseNotFoundError(DomainError):
    pass


class TimetableClashError(DomainError):
    pass


class CollegeMismatchError(DomainError):
    pass
