"""Alteryx plugin output anchor definition."""

from ..records import RecordContainer


class OutputAnchor:
    """Output anchor definition."""

    __slots__ = ["_engine_anchor_ref", "_metadata_pushed", "__record_info", "__record_container", "name", "optional", "num_connections", "push_records"]

    def __init__(
        self, name: str, optional: bool, engine_output_anchor_mgr, record_info=None
    ):
        """Initialize an output anchor."""
        self._engine_anchor_ref = engine_output_anchor_mgr.get_output_anchor(name)
        self._metadata_pushed = False
        self.__record_info = record_info
        if record_info is not None:
            self.__record_container = RecordContainer(record_info)
        else:
            self.__record_container = None

        self.name = name
        self.optional = optional
        self.num_connections = 0
        self.push_records = self._raise_metadata_error

    @property
    def record_container(self):
        """Getter for record container."""
        if self.__record_container is None:
            raise RuntimeError(
                "Output record_info must be specified before output record container can be accessed."
            )

        return self.__record_container

    @property
    def record_info(self):
        """Getter for record info."""
        return self.__record_info

    @record_info.setter
    def record_info(self, value):
        """Setter for record info."""
        if self._metadata_pushed:
            raise RuntimeError("Can't reassign record_info after it has been pushed.")

        self.__record_info = value
        self.__record_container = RecordContainer(value)

    def update_progress(self, percent: float) -> None:
        """Push the progress to downstream tools."""
        self._engine_anchor_ref.update_progress(percent)

    def push_metadata(self) -> None:
        """Push metadata to downstream tools."""
        if self.record_info is None:
            raise ValueError("record_info must be set before metadata can be pushed.")

        if not self._metadata_pushed:
            self._engine_anchor_ref.init(self.record_info)
            self._metadata_pushed = True
            self.push_records = self._push_records

    def _raise_metadata_error(self) -> None:
        """Push records out."""
        raise RuntimeError(
            "Must run push_metadata before push_records can be called."
        )

    def _push_records(self) -> None:
        for record in self.record_container:
            self._engine_anchor_ref.push_record(record.value, False)

        self.record_container.clear_records()

    def close(self) -> None:
        """Close the output anchor."""
        self._engine_anchor_ref.close()

    def push_dataframe(self, df) -> None:
        self.record_container.set_from_df(df)
        self.push_records()