from dataclasses import dataclass

import pytest

import plate


@dataclass
class MoveParam:
    source: list[list[int]]
    dest: list[list[int]]
    overfill: bool
    groupby: int
    move_type: str
    expected: list[list[int]]


@pytest.mark.parametrize(
    "move_param",
    [
        pytest.param(
            MoveParam(
                source=[[1, 2, 3], [1, 2, 3], [3, 3, 3]],
                dest=[[0, 0], [0, 0], [0, 0]],
                overfill=False,
                groupby=1,
                move_type="deterministic",
                expected=[[1, 0], [2, 0], [3, 0]],
            ),
            id="deterministic_ordered_continuous_no_overfill",
        ),
        pytest.param(
            MoveParam(
                source=[[4, 2, 3], [1, 2, 3], [3, 3, 3]],
                dest=[[0, 0], [0, 0], [0, 0]],
                overfill=False,
                groupby=1,
                move_type="deterministic",
                expected=[[1, 4], [2, 0], [3, 0]],
            ),
            id="deterministic_unordered_continuous_no_overfill",
        ),
        pytest.param(
            MoveParam(
                source=[[4, 4, 3], [1, 1, 3], [3, 3, 3]],
                dest=[[0, 0], [0, 0], [0, 0]],
                overfill=False,
                groupby=1,
                move_type="deterministic",
                expected=[[1, 4], [0, 0], [3, 0]],
            ),
            id="deterministic_unordered_noncontinuous_no_overfill",
        ),
        pytest.param(
            MoveParam(
                source=[[1, 2, 3], [1, 2, 3], [4, 5, 6]],
                dest=[[0, 0], [0, 0]],
                overfill=True,
                groupby=1,
                move_type="deterministic",
                expected=[[5, 3], [6, 4]],
            ),
            id="deterministic_ordered_continuous_overfill",
        ),
        pytest.param(
            MoveParam(
                source=[[1, 2, 3], [1, 2, 3], [3, 3, 3]],
                dest=[[0, 0], [0, 0], [0, 0]],
                overfill=False,
                groupby=1,
                move_type="sparse",
                expected=[[1, 0], [3, 0], [2, 0]],
            ),
            id="sparce_unordered_continuous_no_overfill",
        ),
        pytest.param(
            MoveParam(
                source=[[4, 4, 3], [1, 1, 3], [3, 3, 3]],
                dest=[[0, 0], [0, 0], [0, 0]],
                overfill=False,
                groupby=1,
                move_type="sparse",
                expected=[[4, 0], [1, 0], [3, 0]],
            ),
            id="sparse_unordered_noncontinuous_no_overfill",
        ),
        pytest.param(
            MoveParam(
                source=[[4, 4, 5], [1, 1, 6], [3, 3, 6], [3, 3, 7], [3, 3, 8]],
                dest=[[0, 0], [0, 0]],
                overfill=True,
                groupby=1,
                move_type="sparse",
                expected=[[6, 8], [7, 5]],
            ),
            id="sparse_unordered_noncontinuous_overfill",
        ),
        pytest.param(
            MoveParam(
                source=[[1, 1, 2, 2], [1, 1, 2, 2], [3, 3, 4, 4], [3, 3, 4, 4]],
                dest=[[0, 0], [0, 0]],
                overfill=False,
                groupby=4,
                move_type="sparse",
                expected=[[1, 2], [3, 4]],
            ),
            id="sparse_groupby_no_overfill",
        ),
        pytest.param(
            MoveParam(
                source=[
                    [1, 1, 2, 2, 5, 5],
                    [1, 1, 2, 2, 5, 5],
                    [3, 3, 4, 4, 6, 6],
                    [3, 3, 4, 4, 6, 6],
                ],
                dest=[[0, 0], [0, 0]],
                overfill=True,
                groupby=4,
                move_type="sparse",
                expected=[[5, 2], [6, 4]],
            ),
            id="sparse_groupby_overfill",
        ),
        pytest.param(
            MoveParam(
                source=[[1, 1, 2, 2], [1, 1, 2, 2], [3, 3, 4, 4], [3, 3, 4, 4]],
                dest=[[0, 0], [0, 0]],
                overfill=False,
                groupby=4,
                move_type="deterministic",
                expected=[[1, 3], [2, 4]],
            ),
            id="deterministic_groupby_no_overfill",
        ),
        pytest.param(
            MoveParam(
                source=[
                    [1, 1, 2, 2, 5, 5],
                    [1, 1, 2, 2, 5, 5],
                    [3, 3, 4, 4, 6, 6],
                    [3, 3, 4, 4, 6, 6],
                ],
                dest=[[0, 0], [0, 0]],
                overfill=True,
                groupby=4,
                move_type="deterministic",
                expected=[[5, 3], [6, 4]],
            ),
            id="deterministic_groupby_overfill",
        ),
    ],
)
def test_move_success(move_param: MoveParam):
    pl = plate.Mover(
        source=move_param.source, dest=move_param.dest, overfill=move_param.overfill
    )
    getattr(pl, f"move_{move_param.move_type}")()
    assert pl.dest == move_param.expected


def test_move_reset():
    pl = plate.Mover(source=[[1, 2], [1, 2]], dest=[[0, 0], [0, 0]])
    pl.move_deterministic()
    assert pl.dest == [[1, 0], [2, 0]]

    pl.reset()
    assert pl.dest == [[0, 0], [0, 0]]


@pytest.mark.parametrize("method_prefix", ["move_", "validate_"])
@pytest.mark.parametrize(
    "move_param, expected_match",
    [
        pytest.param(
            MoveParam(
                source=[[1, 2, 3], [1, 2, 3], [4, 5, 6]],
                dest=[[0, 0], [0, 0]],
                overfill=False,
                groupby=1,
                move_type="deterministic",
                expected=[[5, 3], [6, 4]],
            ),
            "exceeds plate max capacity of 4",
            id="deterministic_ordered_continuous_no_overfill",
        ),
        pytest.param(
            MoveParam(
                source=[[4, 4, 5], [1, 1, 6], [3, 3, 6], [3, 3, 7], [3, 3, 8]],
                dest=[[0, 0], [0, 0]],
                overfill=False,
                groupby=1,
                move_type="sparse",
                expected=[[6, 8], [7, 5]],
            ),
            "Plate capacity exceeded",
            id="sparse_unordered_noncontinuous_no_overfill",
        ),
    ],
)
def test_move_fail(method_prefix: str, move_param: MoveParam, expected_match: str):
    pl = plate.Mover(
        source=move_param.source, dest=move_param.dest, overfill=move_param.overfill
    )
    with pytest.raises(ValueError):
        getattr(pl, f"{method_prefix}{move_param.move_type}")()


def test_repr():
    pl = plate.Mover(source=[[1, 2], [1, 2]], dest=[[0, 0], [0, 0]])
    assert pl.__repr__() == "   1  2 \nA  0  0 \nB  0  0 "

    pl.move_deterministic()
    assert pl.__repr__() == "   1  2 \nA  1  0 \nB  2  0 "
