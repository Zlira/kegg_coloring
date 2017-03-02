from functools import partial
from warnings import warn

import numpy as np
from PIL import Image as Img

from kegg_coloring.pathway_parse import parse_genes_list


def black_or_color(color, vals):
    """
    Given to collections of RGB values: new value and
    current value, reutrn current value if it's black
    and new value otherwise.
    """
    return vals if (vals == 0).all() else color


def color_gene_section(pixs_arr, gene, color,
                       x_start=0, x_end=0.75, y_start=0, y_end=1):
    """
    Given array of pixels (pixs_arr), a Gene object, desired color
    and part of gene rectangle to color change the color of that part
    of gene rectangle to the desired color. If a pixel inside the part
    is black it stays black.
    """
    x_slice, y_slice = gene.rectangle.get_section_coord_range(
        x_start, x_end, y_start, y_end
    )

    pixs_arr[y_slice, x_slice] = np.apply_along_axis(
        partial(black_or_color, color),
        axis=-1,
        arr=pixs_arr[y_slice, x_slice]
    )
    return pixs_arr


class PathwayImg:
    """
    Represents a KEGG pathway with the associated picture
    and gene list.
    """

    def __init__(self, xml_file, img_file):
        # Later I can download img_file from xml info
        self.xml_file = xml_file
        self.img_file = img_file
        self.genes_ = None
        self.pixs_ = None

    @property
    def genes(self):
        if self.genes_ is None:
            self.genes_ = parse_genes_list(self.xml_file)
        return self.genes_

    @property
    def pixs(self):
        if self.pixs_ is None:
            with Img.open(self.img_file) as pic:
                self.pixs_ = np.array(pic.convert('RGB'))
        return self.pixs_

    def _find_gene_by_list_attr(self, attr_name, attr_val):
        """
        Given a name of Gene attribute (the attribute must be iterable
        like list on names or kegg ids) and the desired value returns
        all Genes that contain that value in the specified attribute.
        """
        found = [
            g for g in self.genes if attr_val in getattr(g, attr_name)
        ]
        if len(found) > 1:
            # it's actually OK to have several instances of gene on
            # pathway scheme, but I may need to handle this differently
            # so the warning stays for now as a reminder.
            warn('More than one gene found for {} {}'.format(
                attr_name, attr_val
            ))
        return found

    def find_gene_by_name(self, gene_name):
        return self._find_gene_by_list_attr(
            'names', gene_name
        )

    def find_gene_by_kegg_id(self, kegg_id):
        return self._find_gene_by_list_attr(
            'kegg_ids', kegg_id
        )

    def color_gene(self, gene_name, color):
        """
        Given a gene name find all genes with that name
        associated with this pathway and color a part of that
        genes' rectangle into the color.

        ToDo:
            Add the ablitiy to control size of colored part.
        """
        # TODO think about handling both names and kegg_ids
        for gene in self.find_gene_by_name(gene_name):
            self.pixs_ = color_gene_section(
                self.pixs, gene, color
            )
        return self.pixs_

    def picture(self):
        return Img.fromarray(self.pixs)

    # TODO add a method to save image into the file
