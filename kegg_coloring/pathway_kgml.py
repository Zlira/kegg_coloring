from xml.etree import ElementTree

from kegg_coloring.gene import Gene
from kegg_coloring.gene import GeneRectangle
from kegg_coloring.kegg_client import download_kgml


def _load_kgml_etree(kgml_file, pathway_id):
    """
    Helper function to load xml ElementTree
    """
    if kgml_file is None:
        kgml_file = download_kgml(pathway_id)

    return ElementTree.parse(kgml_file)


def parse_gene_graphics(graphics):
    """
    Givent xml element 'graphics' construct and recturn
    GeneRectangle object with the coordinates.
    """
    attrs = {'x', 'y', 'width', 'height'}
    return GeneRectangle(**{
        attr: int(graphics.attrib[attr]) for attr in attrs
    })


def parse_gene_entry(gene_entry):
    """
    Given xml element 'entry' of a type 'gene' construct and
    return Gene object with extracted info.
    """
    kegg_ids = gene_entry.attrib['name'].split()
    graphics = gene_entry.find('graphics')
    names = graphics.attrib['name'].strip('.').split(', ')
    rect = parse_gene_graphics(graphics)
    return Gene(
        kegg_ids=set(kegg_ids),
        names=set(names),
        rectangle=rect,
    )


class PathwayKgml:
    '''
    A class to work with KEGG XML (kgml) of a path.

    It can be initated with kegg one of the following:
        * kgml_file - a file name or a file object
        * pahtway_id - a string with KEGG pathway id
    KGML file has preference over pathway_id, if kgml_file is passed
    pathway_id will be ignored.
    '''
    # TODO save pathway_id as attribute (handle a case when only file
    # is passed and add some __repr__ method.

    def __init__(self, kgml_file=None, pathway_id=None):
        assert kgml_file or pathway_id, (
            "One of the arguments kgml_file or pathway_id should "
            "be provided."
        )
        self.etree = _load_kgml_etree(kgml_file, pathway_id)

    def get_image_url(self):
        """
        Given the ElementTree constructed from KEGG pathway xml
        extract and return the url of an image.
        """
        return self.etree.getroot().attrib['image']

    def parse_genes_list(self):
        """
        Given the ElementTree constructed from KEGG pathway xml
        extract all 'gene' enties and construct a list of Gene
        objects from it.
        """
        genes = (
            e for e in self.etree.findall('entry')
            if e.attrib['type'] == 'gene'
        )
        return [parse_gene_entry(g) for g in genes]

    def save(self, file_path):
        with open(file_path, 'w') as out_file:
            self.etree.write(out_file)
