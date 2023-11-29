import copy
import math
from collections import defaultdict

SRC = [
    [1, 1, 1, 1, 5, 5, 5, 5, 9, 9, 9, 9, 1, 1, 1, 1, 5, 5, 5, 5, 9, 9, 9, 9],
    [1, 1, 1, 1, 5, 5, 5, 5, 9, 9, 9, 9, 1, 1, 1, 1, 5, 5, 5, 5, 9, 9, 9, 9],
    [1, 1, 1, 1, 5, 5, 5, 5, 9, 9, 9, 9, 1, 1, 1, 1, 5, 5, 5, 5, 9, 9, 9, 9],
    [1, 1, 1, 1, 5, 5, 5, 5, 9, 9, 9, 9, 1, 1, 1, 1, 5, 5, 5, 5, 9, 9, 9, 9],
    [2, 2, 2, 2, 6, 6, 6, 6, 10, 10, 10, 10, 2, 2, 2, 2, 6, 6, 6, 6, 10, 10, 10, 10],
    [2, 2, 2, 2, 6, 6, 6, 6, 10, 10, 10, 10, 2, 2, 2, 2, 6, 6, 6, 6, 10, 10, 10, 10],
    [2, 2, 2, 2, 6, 6, 6, 6, 10, 10, 10, 10, 2, 2, 2, 2, 6, 6, 6, 6, 10, 10, 10, 10],
    [2, 2, 2, 2, 6, 6, 6, 6, 10, 10, 10, 10, 2, 2, 2, 2, 6, 6, 6, 6, 10, 10, 10, 10],
    [3, 3, 3, 3, 7, 7, 7, 7, 11, 11, 11, 11, 3, 3, 3, 3, 7, 7, 7, 7, 11, 11, 11, 11],
    [3, 3, 3, 3, 7, 7, 7, 7, 11, 11, 11, 11, 3, 3, 3, 3, 7, 7, 7, 7, 11, 11, 11, 11],
    [3, 3, 3, 3, 7, 7, 7, 7, 11, 11, 11, 11, 3, 3, 3, 3, 7, 7, 7, 7, 11, 11, 11, 11],
    [3, 3, 3, 3, 7, 7, 7, 7, 11, 11, 11, 11, 3, 3, 3, 3, 7, 7, 7, 7, 11, 11, 11, 11],
    [4, 4, 4, 4, 8, 8, 8, 8, 12, 12, 12, 12, 4, 4, 4, 4, 8, 8, 8, 8, 12, 12, 12, 12],
    [4, 4, 4, 4, 8, 8, 8, 8, 12, 12, 12, 12, 4, 4, 4, 4, 8, 8, 8, 8, 12, 12, 12, 12],
    [4, 4, 4, 4, 8, 8, 8, 8, 12, 12, 12, 12, 4, 4, 4, 4, 8, 8, 8, 8, 12, 12, 12, 12],
    [4, 4, 4, 4, 8, 8, 8, 8, 12, 12, 12, 12, 4, 4, 4, 4, 8, 8, 8, 8, 12, 12, 12, 12],
]

DEST = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


PlateType = list[list[int]]
CoordType = tuple[int, int]


class Mover:
    alpha = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(
        self,
        source: PlateType,
        dest: PlateType,
        overfill: bool = False,
        groupby: int = 1,
    ) -> None:
        """
        Initialise Plate mover

        :param source: source plate with samples
        :param dest:  destination plate to move samples to
        :param overfill: flag showing if samples of a different group can be mixed
                         in case capacities of the destination plate are exceeded.
        :param groupby: number of samples that form a single group number/colour
        """
        self.source = source
        self.dest = copy.deepcopy(dest)
        self.original_dest = copy.deepcopy(dest)
        self.overfill = overfill
        self.groupby = groupby
        self.step = int(math.sqrt(groupby))
        assert self.step**2 == self.groupby
        self.sample_counters: dict[int, int] = defaultdict(int)

    def reset(self):
        """
        Reset results of moving samples
        """
        self.dest = copy.deepcopy(self.original_dest)
        self.sample_counters = defaultdict(int)

    def _check_capacity(self, val: int, max_capacity: int):
        """
        If source plate contains more sample groups than destination
        and flag for overflow is off, raise an exception.
        Otherwise, when moving samples they will overfill existing groups.
        """
        if (val > max_capacity) and not self.overfill:
            raise ValueError(
                f"Value {val} exceeds plate max capacity of {max_capacity}"
            )

    @staticmethod
    def _calc_deterministic_coord(
        value: int, max_capacity: int, rows: int
    ) -> CoordType:
        """
        Return col, row indices representing coordinates to put the sample value
        """
        col, row = divmod((value - 1) % max_capacity, rows)
        return col, row

    @staticmethod
    def _get_plate_size(plate: PlateType) -> tuple[int, int, int]:
        """
        Return a tuple of (cols, rows, max capacity) of the given plate.
        Assume the plate has rows of the same size
        """
        cols = len(plate[0])
        rows = len(plate)
        return cols, rows, cols * rows

    def validate_deterministic(self) -> None:
        """
        Raise exception if destination plate won't fit all the samples.
        Used for `move_deterministic` approach.
        """
        _, _, max_capacity = self._get_plate_size(self.dest)
        for row in self.source:
            for val in row:
                self._check_capacity(val, max_capacity)

    def move_deterministic(self):
        """
        Move samples from the source plate to destination plate column by column.
        Sample's group number determines cell position on the destination plate.
        Pros: destination cell is determined by the group number,
        may be useful depending on the "consumer" of the destination plate.
        Cons: if group numbers aren't continuous range and/or not starting from 1,
        there may be too many unfilled cells
        """
        source_cols, source_rows, _ = self._get_plate_size(self.source)
        dest_cols, dest_rows, dest_max_capacity = self._get_plate_size(self.dest)

        for col_idx in range(0, source_cols, self.step):
            for row_idx in range(0, source_rows, self.step):
                sample_value = self.source[row_idx][col_idx]
                self._check_capacity(val=sample_value, max_capacity=dest_max_capacity)
                dest_col_idx, dest_row_idx = self._calc_deterministic_coord(
                    value=sample_value, max_capacity=dest_max_capacity, rows=dest_rows
                )
                self.sample_counters[sample_value] += self.groupby
                self.dest[dest_row_idx][dest_col_idx] = sample_value

    def _get_sparse_coord(
        self,
        prev_coord: CoordType | None,
        plate_cols: int,
        plate_rows: int,
    ) -> CoordType:
        """
        Given the previous coordinates and the plate size, return next unfilled coordinates (col, row)
        """
        if not prev_coord:
            return 0, 0

        col, row = prev_coord
        col_overflow, new_row = divmod((row + 1), plate_rows)
        plate_overflow, new_col = divmod((col + col_overflow), plate_cols)

        if plate_overflow and not self.overfill:
            raise ValueError("Plate capacity exceeded")
        else:
            return new_col, new_row

    def validate_sparse(self) -> None:
        """
        Raise exception if destination plate won't fit all the samples.
        Used for `move_sparse` approach.
        """
        _, _, dest_max_capacity = self._get_plate_size(self.dest)
        uniq_vals = set()
        for row in self.source:
            for val in row:
                uniq_vals.add(val)
        if len(uniq_vals) > dest_max_capacity:
            raise ValueError("Plate capacity exceeded")

    def move_sparse(self):
        """
        Move source plate's samples to the destination plate column by column.
        Same group samples are grouped.
        Pros: destination plate is filled sparsely, no matter the sample numbering.
        Cons: we cannot predict destination cells by sample group number
        without prior knowledge of the source plate
        """
        source_cols, source_rows, _ = self._get_plate_size(self.source)
        dest_cols, dest_rows, dest_max_capacity = self._get_plate_size(self.dest)

        prev_coord = None
        val_to_coord: dict[int, CoordType] = {}

        for col_idx in range(0, source_cols, self.step):
            for row_idx in range(0, source_rows, self.step):
                sample_value = self.source[row_idx][col_idx]
                existing_coords = val_to_coord.get(sample_value)

                if not existing_coords:
                    dest_col_idx, dest_row_idx = self._get_sparse_coord(
                        prev_coord=prev_coord,
                        plate_cols=dest_cols,
                        plate_rows=dest_rows,
                    )
                    val_to_coord[sample_value] = dest_col_idx, dest_row_idx
                    prev_coord = dest_col_idx, dest_row_idx
                    self.dest[dest_row_idx][dest_col_idx] = sample_value

                self.sample_counters[sample_value] += self.groupby

    def __repr__(self):
        """
        Return a representation string for the destination plate
        """

        def _fmt(s):
            return "%-2s" % s

        header = [str(i + 1) for i in range(len(self.dest[0]))]
        rows = [header] + self.dest
        result = []
        for idx, row in enumerate(rows):
            letter = self.alpha[idx % len(self.alpha)]
            new_row = [letter] + row
            result.append(" ".join(map(_fmt, new_row)))
        return "\n".join(result)
