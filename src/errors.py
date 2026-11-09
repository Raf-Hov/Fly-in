"""Custom exceptions of the project."""


class ParseError(Exception):
    """Invalid map file: carries the line number and the cause."""

    def __init__(self, line_num: int, reason: str) -> None:
        """Build the message; line 0 means 'not tied to a line'."""
        self.line_num = line_num
        self.reason = reason
        prefix = f"Line {line_num}: " if line_num > 0 else ""
        super().__init__(f"{prefix}{reason}")
