#!/usr/bin/env python3

class Grid2D:
    """
    2D grid with x,y int indexed internal storage
    Has .width .height size properties
    """

    def __init__(self, width, height, empty=None):
        """
        Create grid width by height.
        Initially all locations hold None.
        """
        # Pretty agro use of comprehensions!
        self.array = [[empty for _ in range(width)] for _ in range(height)]
        self.width = width
        self.height = height
        self.empty = empty

    def get(self, x, y):
        """
        Gets the value stored value at x,y.
        x,y should be in bounds.
        """
        if not self.in_bounds(x, y):
            raise ValueError("Coordinates out of bounds")

        return self.array[y][x]

    def set(self, x, y, val):
        """
        Sets a new value into the grid at x,y.
        x,y should be in bounds.
        """
        if not self.in_bounds(x, y):
            raise ValueError("Coordinates out of bounds")

        self.array[y][x] = val

    def clear(self, x, y):
        """
        Clears the value at x,y.
        x,y should be in bounds.
        """
        if not self.in_bounds(x, y):
            raise ValueError("Coordinates out of bounds")

        self.array[y][x] = self.empty
        
    def clear_all(self):
        """
        Clears all values in the grid.
        """
        for y in range(self.height):
            for x in range(self.width):
                self.array[y][x] = self.empty
        
    @staticmethod
    def create(l):
        """
        Construct Grid2D using a nested-lst literal
        e.g. this makes a 3 by 2 grid:
        Grid2D.create([[1, 2, 3], [4, 5 6]])
        >>> Grid2D.create([[1, 2, 3], [4, 5, 6]])
        [[1, 2, 3], [4, 5, 6]]
        """
        Grid2D.validate_list(l)
        height = len(l)
        width = len(l[0])
        grid = Grid2D(width, height)
        for y in range(height):
            for x in range(width):
                grid.set(x, y, l[y][x])
        return grid

    def in_bounds(self, x, y):
        """
        Returns True if the x,y is in bounds of the grid. False otherwise.
        """
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def copy(self):
        """
        Return a copy of the grid2d
        """
        grid2d = Grid2D(self.width, self.height)
        for y in range(self.height):
            for x in range(self.width):
                grid2d.set(x, y, self.get(x, y))
        return grid2d

    def __str__(self):
        return repr(self.array)

    # In particular Doctest seems to use this, so crucial to make
    # Grid work in Doctests.
    def __repr__(self):
        return repr(self.array)

    @staticmethod
    def validate_list(l):
        """
        Given a list that represents a 2-d nesting, checks that it has the
        right type and the sublists are all the same len.
        Raises exception for malformations.
        """
        if not l or type(l) != list:
            raise Exception("Expecting list but got:" + str(l))

        if len(l) >= 2:
            size = len(l[0])
            for sub in l:
                if len(sub) != size:
                    raise Exception("Sub-lists are not all the same length:" + str(l))

def grid_demo():
    """
    Demonstrate use of the Grid class.
    """
    # Create width 4 by height 2 grid, filled with None initially.
    grid = Grid2D(4, 2)

    # loop over contents in usual way,
    # setting every location to 7
    for y in range(grid.height):
        for x in range(grid.width):
            grid.set(x, y, 7)

    # access 0,0
    val = grid.get(0, 0)

    # verify that 3,1 is in bounds
    if grid.in_bounds(3, 1):
        # set 3,1
        grid.set(3, 1, 11)

    print("Width:", grid.width)
    print("Height:", grid.height)
    print(grid)
    # print uses nested-list format
    # showing row-0, then row-1
    # [[7, 7, 7, 7], [7, 7, 7, 11]]

    # Grid.build() supports the same nested-list format,
    # allowing you to construct a grid on the fly.
    grid2 = Grid2D.create([[7, 7, 7, 7], [7, 7, 7, 'X']])
    grid2.set(3, 1, 33)
    print("Width:", grid2.width)
    print("Height:", grid2.height)
    print(grid2)

    # Can make a copy if needed.
    grid3 = grid.copy()
    print("Width:", grid3.width)
    print("Height:", grid3.height)
    print(grid3)

def main():
    grid_demo()


if __name__ == "__main__":
    main()
