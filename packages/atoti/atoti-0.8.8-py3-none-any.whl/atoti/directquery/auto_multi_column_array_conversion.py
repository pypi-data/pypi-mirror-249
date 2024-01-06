from dataclasses import dataclass

from atoti_core import keyword_only_dataclass


@keyword_only_dataclass
@dataclass(frozen=True)
class AutoMultiColumnArrayConversion:
    """Automatically convert all external tables with array values stored with one element per column to tables with arrays.

    See Also:
        :class:`~atoti.MultiColumnArrayConversion`
    """

    separator: str = ""
    """
    The characters separating the array column name and the element index.
    """

    threshold: int = 50
    """
    The minimum number of columns with the same prefix required to trigger the automatic conversion.
    """
