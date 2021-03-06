"""Mock record ref class definition."""
from typing import Any, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .record_info import RecordInfo


class RecordRef:
    """Record ref mock."""

    def __init__(self, record_info: "RecordInfo") -> None:
        """Construct a record ref."""
        self.data: Dict[str, Any] = {field.name: None for field in record_info}

    def set_field(self, name: str, value: Any) -> None:
        """Set a field to a value."""
        self.data[name] = value

    def get_field(self, name: str) -> Any:
        """Get the value of a field."""
        return self.data[name]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RecordRef):
            return NotImplemented

        return self.data == other.data
