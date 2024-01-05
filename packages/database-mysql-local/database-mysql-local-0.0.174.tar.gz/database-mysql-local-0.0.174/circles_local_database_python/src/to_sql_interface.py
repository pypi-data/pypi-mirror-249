from abc import ABC, abstractmethod


class ToSQLInterface(ABC):
    """
    An interface for objects that represent structures to be
    inserted into a database.

    Subclasses must implement the `to_sql` method, which should return a string
    representing the SQL representation of the structure.

    Example:
    --------
    class Point(ToSQLInterface):
        def __init__(self, longitude, latitude):
            self.longitude = longitude
            self.latitude = latitude

        def to_sql(self):
            return f"POINT({self.longitude}, {self.latitude})"
    """
    @abstractmethod
    def to_sql(self) -> str:
        pass
