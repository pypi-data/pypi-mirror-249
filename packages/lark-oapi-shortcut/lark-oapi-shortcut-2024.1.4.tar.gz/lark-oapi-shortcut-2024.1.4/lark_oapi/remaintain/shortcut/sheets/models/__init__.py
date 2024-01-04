import functools
import re
from typing import Optional

from pydantic import BaseModel

from .. import utils


@functools.total_ordering
class CellPos(BaseModel):
    x: str = ""
    y: int = 0

    @classmethod
    def from_literal(cls, s: str):
        pattern = r'([A-Z]*)(\d*)'
        matched_groups: tuple = ()
        matched = re.match(pattern, s)
        if matched:
            try:
                matched_groups = matched.groups()
            except AttributeError:
                pass
        if len(matched_groups) != 2:
            return None
        return cls(
            x=matched_groups[0],
            y=int(matched_groups[1]) if matched_groups[1] else 0,
        )

    def to_param_range(self):
        x = self.x
        y = self.y
        if y > 0:
            return f"{x}{y}"
        return x

    def __lt__(self, other):
        return (utils.column_name_to_number(self.x), self.y) < (utils.column_name_to_number(other.x), other.y)


class CellsRange(BaseModel):
    start_pos: Optional[CellPos]
    end_pos: Optional[CellPos]

    @classmethod
    def from_literal(cls, s: str):
        pattern = r'([A-Z]*)(\d*):([A-Z]*)(\d*)'
        matched_groups: tuple = ()
        matched = re.match(pattern, s)
        if matched:
            try:
                matched_groups = ("",) + matched.groups()
            except AttributeError:
                pass
        if len(matched_groups) != 5:
            return None
        return cls(
            start_pos=CellPos(
                x=matched_groups[1],
                y=int(matched_groups[2]) if matched_groups[2] else 0,
            ),
            end_pos=CellPos(
                x=matched_groups[3],
                y=int(matched_groups[4]) if matched_groups[4] else 0,
            ),
        )

    def to_param_range_pos_part(self):
        res = ""
        if self.start_pos:
            res += self.start_pos.to_param_range()
        if self.end_pos:
            res += ":"
            res += self.end_pos.to_param_range()
        return res


class SheetRange(CellsRange):
    sheet_id: str

    @classmethod
    def from_literal(cls, s: str):
        pattern = r'(.*?)!([A-Z]*)(\d*):([A-Z]*)(\d*)'
        matched_groups: tuple = ()
        matched = re.match(pattern, s)
        if matched:
            try:
                matched_groups = matched.groups()
            except AttributeError:
                pass
        if len(matched_groups) != 5:
            return None
        return cls(
            sheet_id=matched_groups[0],
            start_pos=CellPos(
                x=matched_groups[1],
                y=int(matched_groups[2]) if matched_groups[2] else 0,
            ),
            end_pos=CellPos(
                x=matched_groups[3],
                y=int(matched_groups[4]) if matched_groups[4] else 0,
            ),
        )

    def to_param_range(self) -> str:
        res = f"{self.sheet_id}"
        if self.start_pos:
            res += "!"
            res += self.start_pos.to_param_range()
        if self.end_pos:
            res += ":"
            res += self.end_pos.to_param_range()
        return res
