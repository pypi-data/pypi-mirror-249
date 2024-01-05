from typing import Mapping, Sequence, Union

import shapely
from shapely import unary_union

from .geometry_types import is_multi
from .morphology import closing

__all__ = ["overlap_groups"]


def overlap_groups(
    to_be_grouped: Union[Sequence, Mapping], must_be_unique: bool = False
) -> Sequence[Mapping]:
    if not isinstance(to_be_grouped, Mapping):
        to_be_grouped = dict(zip((i for i in range(len(to_be_grouped))), to_be_grouped))

    if must_be_unique:
        assert not any(is_multi(p) for p in to_be_grouped.values()), to_be_grouped

    s = list(unary_union(v) for v in to_be_grouped.values())

    union = closing(unary_union(s)).buffer(0)
    groups = []
    already_grouped = []

    if not is_multi(union):
        groups.append(to_be_grouped)
    else:
        for union_part in union.geoms:
            intersectors = {}
            for k, v in to_be_grouped.items():
                if shapely.intersects(v, union_part):
                    if must_be_unique:
                        assert k not in already_grouped, f"{k, already_grouped, v}"
                    intersectors[k] = v
                    already_grouped.append(k)
            groups.append(intersectors)

    return groups


if __name__ == "__main__":

    def demo():
        from shapely.geometry import box
        from pprint import pprint

        data = [
            box(1, 1, 3, 3),
            box(2, 2, 3, 3),
            box(4, 4, 6, 6),
            box(4, 4, 5, 5),
            box(5, 5, 6, 6),
            box(7, 7, 8, 8),
            box(1, 1, 2, 2),
            box(4, 4, 6, 6),
        ]

        pprint(overlap_groups(data))

        data = [
            box(1, 1, 3, 3),
            unary_union([box(2, 2, 3, 3), box(4, 4, 5, 5)]),
            box(4, 4, 6, 6),
            box(4, 4, 5, 5),
        ]

        pprint(overlap_groups(data))

        # pprint(overlap_groups(data, must_be_unique=True)) # FAILS!

    demo()
