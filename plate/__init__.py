import copy
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
        self, source: PlateType, dest: PlateType, overfill: bool = False
    ) -> None:
        self.source = source
        self.dest = dest
        self.original_dest = copy.deepcopy(dest)
        self.overfill = overfill
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
    def _calc_deterministic_coord(value: int, max_capacity: int, rows: int):
        return divmod((value - 1) % max_capacity, rows)

    @staticmethod
    def _get_plate_size(plate: PlateType) -> tuple[int, int, int]:
        """
        Return a tuple of (cols, rows, max capacity) of the given plate.
        Assume the plate has rows of the same size
        """
        cols = len(plate[0])
        rows = len(plate)
        return cols, rows, cols * rows

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

        for col_idx in range(source_cols):
            for row_idx in range(source_rows):
                sample_value = self.source[row_idx][col_idx]
                self._check_capacity(val=sample_value, max_capacity=dest_max_capacity)
                # Swap col/row indices so that we move samples column by column
                dest_row_idx, dest_col_idx = self._calc_deterministic_coord(
                    value=sample_value, max_capacity=dest_max_capacity, rows=dest_rows
                )

                self.sample_counters[sample_value] += 1
                self.dest[dest_col_idx][dest_row_idx] = sample_value

    def _get_sparse_coord(
        self,
        prev_coord: CoordType | None,
        plate_cols: int,
        plate_rows: int,
    ) -> tuple[int, int]:
        """
        Given the previous coordinates and the plate size, return next unfilled coordinates
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

    def move_sparse(self):
        """
        Move source plate's samples to the destination plate column by column.
        Same group samples are grouped.
        Pros: destination plate is filled sparsefully, no matter the sample numbering.
        Cons: we cannot predict destination cells by sample group number
        without prior knowledge of the source plate
        """
        source_cols, source_rows, _ = self._get_plate_size(self.source)
        dest_cols, dest_rows, dest_max_capacity = self._get_plate_size(self.dest)

        prev_coord = None
        val_to_coord: dict[int, CoordType] = {}

        for col_idx in range(source_cols):
            for row_idx in range(source_rows):
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

                self.sample_counters[sample_value] += 1

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
