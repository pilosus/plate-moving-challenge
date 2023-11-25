from collections import defaultdict

SRC = [[1, 1, 1, 1,  5, 5, 5, 5,  9, 9, 9, 9,  1, 1, 1, 1,  5, 5, 5, 5,  9, 9, 9, 9],
       [1, 1, 1, 1,  5, 5, 5, 5,  9, 9, 9, 9,  1, 1, 1, 1,  5, 5, 5, 5,  9, 9, 9, 9],
       [1, 1, 1, 1,  5, 5, 5, 5,  9, 9, 9, 9,  1, 1, 1, 1,  5, 5, 5, 5,  9, 9, 9, 9],
       [1, 1, 1, 1,  5, 5, 5, 5,  9, 9, 9, 9,  1, 1, 1, 1,  5, 5, 5, 5,  9, 9, 9, 9],

       [2, 2, 2, 2,  6, 6, 6, 6,  10,10,10,10,  2, 2, 2, 2,  6, 6, 6, 6,  10,10,10,10],
       [2, 2, 2, 2,  6, 6, 6, 6,  10,10,10,10,  2, 2, 2, 2,  6, 6, 6, 6,  10,10,10,10],
       [2, 2, 2, 2,  6, 6, 6, 6,  10,10,10,10,  2, 2, 2, 2,  6, 6, 6, 6,  10,10,10,10],
       [2, 2, 2, 2,  6, 6, 6, 6,  10,10,10,10,  2, 2, 2, 2,  6, 6, 6, 6,  10,10,10,10],

       [3, 3, 3, 3,  7, 7, 7, 7,  11,11,11,11,  3, 3, 3, 3,  7, 7, 7, 7,  11,11,11,11],
       [3, 3, 3, 3,  7, 7, 7, 7,  11,11,11,11,  3, 3, 3, 3,  7, 7, 7, 7,  11,11,11,11],
       [3, 3, 3, 3,  7, 7, 7, 7,  11,11,11,11,  3, 3, 3, 3,  7, 7, 7, 7,  11,11,11,11],
       [3, 3, 3, 3,  7, 7, 7, 7,  11,11,11,11,  3, 3, 3, 3,  7, 7, 7, 7,  11,11,11,11],

       [4, 4, 4, 4,  8, 8, 8, 8,  12,12,12,12,  4, 4, 4, 4,  8, 8, 8, 8,  12,12,12,12],
       [4, 4, 4, 4,  8, 8, 8, 8,  12,12,12,12,  4, 4, 4, 4,  8, 8, 8, 8,  12,12,12,12],
       [4, 4, 4, 4,  8, 8, 8, 8,  12,12,12,12,  4, 4, 4, 4,  8, 8, 8, 8,  12,12,12,12],
       [4, 4, 4, 4,  8, 8, 8, 8,  12,12,12,12,  4, 4, 4, 4,  8, 8, 8, 8,  12,12,12,12]]

DEST = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


class Mover:
    alpha = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, source: list, dest: list, overfill: bool = False) -> None:
        self.source = source
        self.dest = dest
        self.moved = dest
        self.overfill = overfill
        self.sample_counters = defaultdict(int)

    def reset(self):
        """Reset results of moving samples"""
        self.moved = self.dest[:]
        self.sample_counters = defaultdict(int)

    def _check_capacity(self, val: int, max_capacity: int):
        """
        If source plate contains more sample groups than destination
        and flag for overflow is off, raise an exception.
        Otherwise, when moving samples they will overfill existing groups.
        """
        if (val > max_capacity) and not self.overfill:
            raise ValueError(f"Value {val} exceeds plat max capacity of {max_capacity}")

    @staticmethod
    def _calc_dest_coords(value: int, max_capacity: int, rows: int):
        """
        Return column index and row index based on the value.
        Assume values start from 1, but coordinates (col idx, row idx) from 0.
        NB! The algorithm won't produce sparce filling in case sample values don't form
        a continuous range, e.g. when some values are missing: 1,2,5,6,7,8,12...
        """
        return divmod((value - 1) % max_capacity, rows)

    def move(self):
        """
        Move samples from the source plate to destination plate.
        Assume iteration over plates in top-to-down/left-to-right manner (column by column).
        Assume no predefined patterns for the source plate's samples.
        """
        source_cols = len(self.source[0])
        source_rows = len(self.source)

        dest_cols = len(self.dest[0])
        dest_rows = len(self.dest)
        dest_max_capacity = dest_rows * dest_cols

        for col_idx in range(source_cols):
            for row_idx in range(source_rows):
                sample_value = self.source[row_idx][col_idx]

                self._check_capacity(val=sample_value, max_capacity=dest_max_capacity)
                dest_row_idx, dest_col_idx = self._calc_dest_coords(value=sample_value,
                                                                    max_capacity=dest_max_capacity,
                                                                    rows=dest_rows)

                self.sample_counters[sample_value] += 1
                self.dest[dest_col_idx][dest_row_idx] = sample_value

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
