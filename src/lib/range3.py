from lib.vec3 import Int3


class Range3:
    def __init__(self, start: Int3, stop: Int3):
        self.start = start
        self.stop = stop

    def __iter__(self):
        i3 = self.start.copy()
        while True:
            yield i3
            i3[2] += 1
            d = 2
            while i3[d] == self.stop[d]:
                if d == 0:
                    return
                i3[d] = self.start[d]
                d -= 1
                i3[d] += 1


def test():
    r3 = Range3(Int3(0, 0, 2), Int3(2, 1, 4))
    i3s = [Int3(0, 0, 2), Int3(0, 0, 3), Int3(1, 0, 2), Int3(1, 0, 3)]

    for actual, expected in zip(r3, i3s):
        assert (actual == expected).all()
