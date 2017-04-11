from contextlib import contextmanager
from functools import partial
from warnings import warn

import numpy as np
from PIL import Image as Img

from kegg_coloring.kegg_client import download_img
from kegg_coloring.pathway_kgml import PathwayKgml
from kegg_coloring.utils import most_common_row


def new_pix_color(bg_color, new, old):
    """
    Returns new color for background pixels and old for
    all other.
    """
    return new if (old == bg_color).all() else old


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
    section = pixs_arr[y_slice, x_slice]
    # we want to change only background color. at this point
    # the color of a background is determined as the most common one.
    bg_color = most_common_row(section.reshape((1, -1, 3))[0])

    pixs_arr[y_slice, x_slice] = np.apply_along_axis(
        partial(new_pix_color, bg_color, color),
        axis=-1,
        arr=pixs_arr[y_slice, x_slice]
    )
    return pixs_arr


class PathwayImg:
    """
    Represents a KEGG pathway with the associated picture
    and gene list.
    """

    def __init__(self, pathway_id):
        self.id = pathway_id

        self._kgml = None
        self._genes = None
        self._pixs = None
        # an image file it can be a path string, or a filelike object
        self._img = None

    @property
    def kgml(self):
        if self._kgml is None:
            self._kgml = PathwayKgml(pathway_id=self.id)
        return self._kgml

    @kgml.setter
    def kgml(self, kgml_file):
        """
        kgml property is lazy so if it's set before the first
        access it will not be downloaded from the network
        """
        self._kgml = PathwayKgml(kgml_file=kgml_file)

    @property
    def img(self):
        # at the moment file is not saved after downlaod so
        # if the stream was closed and it's need for something
        # else it will be downloaded again
        if self._img is None or (
            # Ugh! not a nice check
            not isinstance(self._img, str) and self._img.closed
        ):
            self.img = download_img(self.kgml.get_image_url())
        return self._img

    @img.setter
    def img(self, img_file):
        self._img = img_file

    @contextmanager
    def image(self):
        # TODO a bit inconsistent naming
        # TODO can and should this be reusable?
        # Pillow's Image.open can handle both files and
        # file paths
        img = Img.open(self.img)
        yield img
        img.close()

    @property
    def genes(self):
        if self._genes is None:
            self._genes = self.kgml.parse_genes_list()
        return self._genes

    @property
    def pixs(self):
        if self._pixs is None:
            with self.image() as image:
                self._pixs = np.array(image.convert('RGB'))
        return self._pixs

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
            self._pixs = color_gene_section(
                self.pixs, gene, color
            )
        return self._pixs

    def picture_from_pixs(self):
        return Img.fromarray(self.pixs)

    # TODO add a method to save image into the file
