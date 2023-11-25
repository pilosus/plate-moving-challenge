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


class Plate:
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Mover:
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, source: list, dest: list) -> None:
        self.source = self._transpose(source)
        self.dest = self._transpose(dest)
        self.dest_rows = len(self.dest)
        self.dest_cols = len(self.dest[0])

    @staticmethod
    def _transpose(plate: list) -> list:
        """
        Transpose the matrix (list of lists)
        """
        result = []
        for col in range(len(plate[0])):
            new_row = []
            for row in range(len(plate)):
                new_row.append(plate[row][col])
            result.append(new_row)
        return result

    def source_val_to_dest_idx(self, val: int, overflow: bool = True) -> int:
        if not overflow and val > self.dest_rows * self.dest_cols:
            raise ValueError(f"Value {val} exceeds the plate capacity")

        # divisor and remainder represent col and row respectively
        return divmod((val - 1) % self.dest_rows, self.dest_cols)

    def move(self, overflow: bool = True) -> None:
        val_to_count = defaultdict(int)
        filled = 0
        max_places = self.dest_rows * self.dest_cols

        for row in self.source:
            for val in row:
                dest_col, dest_row = divmod((val - 1) % self.dest_rows, self.dest_cols)
                dest_current_val = self.dest[dest_col][dest_row]

                print(f"Value: {val}, Dest coord {dest_col}, {dest_row}, Filled: {filled}")

                self.dest[dest_col][dest_row] = val
                if dest_current_val != val:
                    if not overflow and filled >= max_places:
                        raise ValueError(f"Value {val} exceeds the plate capacity")
                    filled += 1
                val_to_count[val] += 1

    def __str__(self) -> None:
        transposed = self._transpose(self.dest)
        padding = [" ", " ", " "]
        col_numbers = " ".join(padding + [str(i + 1) for i in range(len(transposed[0]))])
        underscore = " ".join(padding + ["_" for _ in range(len(transposed[0]))])

        result = [col_numbers, underscore]
        for idx, row in enumerate(transposed):
            letter = self.alpha[idx % len(self.alpha)]
            new_row = [letter, " | "] + row
            result.append(" ".join(map(str, new_row)))

        return "\n".join(result)
