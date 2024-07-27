from dataclasses import dataclass, field


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Square:
    top_left: Point
    size: int
    top_right: Point = field(init=False)
    bottom_left: Point = field(init=False)
    bottom_right: Point = field(init=False)
    midpoint: Point = field(init=False)

    def __post_init__(self):
        assert self.size.is_integer()

        self.top_right = Point(self.top_left.x + self.size, self.top_left.y)
        self.bottom_left = Point(self.top_left.x, self.top_left.y + self.size)
        self.bottom_right = Point(
            self.top_left.x + self.size, self.top_left.y + self.size)

        assert self.top_left.x == self.bottom_left.x
        assert self.top_right.x == self.bottom_right.x
        assert self.top_left.y == self.top_right.y
        assert self.bottom_left.y == self.bottom_right.y
        assert self.bottom_right.x > self.top_left.x and self.bottom_right.y > self.top_left.y
        # assert ((self.top_left.x + self.bottom_right.x) / 2).is_integer()
        # assert ((self.top_left.y + self.bottom_right.y) / 2).is_integer()

        self.midpoint = Point(
            (self.top_left.x + self.bottom_right.x) // 2,
            (self.top_left.y + self.bottom_right.y) // 2,
        )
        self.size = self.top_right.x - self.top_left.x


@dataclass
class Diamond:
    midpoint: Point
    # the distance between the midpoint and any of the other corner points
    radius: int
    top: Point = field(init=False)
    left: Point = field(init=False)
    right: Point = field(init=False)
    bottom: Point = field(init=False)

    def __post_init__(self):
        assert self.radius.is_integer()

        self.top = Point(self.midpoint.x, self.midpoint.y - self.radius)
        self.bottom = Point(self.midpoint.x, self.midpoint.y + self.radius)
        self.left = Point(self.midpoint.x - self.radius, self.midpoint.y)
        self.right = Point(self.midpoint.x + self.radius, self.midpoint.y)

        assert self.top.x == self.bottom.x
        assert self.left.y == self.right.y
        assert self.top.y - self.bottom.y == self.left.x - self.right.x
        assert self.bottom.y > self.top.y and self.right.x > self.left.x
        assert ((self.top.y - self.bottom.y) / 2).is_integer()
        assert ((self.left.x - self.right.x) / 2).is_integer()
