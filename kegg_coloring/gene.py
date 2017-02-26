from functools import partial


def coords_relative_to_center(center, size, fraction):
    """
    Given center of rectangle (x or y coordinate) and it's size
    (widht or height respectivly) and a fraction return coordinate
    of the edge of that fraction.

    ToDo:
        write this expanation more clearly.
    """
    centre_pos = 0.5
    return int(center + (fraction - centre_pos) * size)


class GeneRectangle:
    """
    Represents a rectangle on the image where the gene is.
    """

    def __init__(self, x, y, width, height):
        # ignore fgcolor and bgcolor for now
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_section_coord_range(self, x_start=0, x_end=0.25,
                                y_start=0, y_end=1):
        """
        Return coordinates of a section of triangle limited by fractions
        x_start, x_end, y_start, y_end. Coordinates are returned as a tuple
        of slices.
        """
        get_x_pos = partial(coords_relative_to_center, self.x, self.width)
        get_y_pos = partial(coords_relative_to_center, self.y, self.height)
        return (slice(get_x_pos(x_start), get_x_pos(x_end) + 1),
                slice(get_y_pos(y_start), get_y_pos(y_end) + 1))


class Gene:
    """
    Represents a gene in a pathway.

    Todo:
        Maybe if one gene is depicted on pathway scheme several times
        it should have only one Gene object with several rectangles.
    """
    def __init__(self, names, kegg_ids=None, rectangle=None):
        self.names = names
        self.kegg_ids = kegg_ids
        self.rectangle = rectangle

    def __repr__(self):
        return 'Gene {} at position ({}, {})'.format(
            self.names[0], *self.center_coordinates()
        )

    def center_coordinates(self):
        if self.rectangle is None:
            return None, None
        else:
            return self.rectangle.x, self.rectangle.y
