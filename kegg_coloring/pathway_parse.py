from xml.etree import ElementTree

from kegg_coloring.gene import Gene
from kegg_coloring.gene import GeneRectangle


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


def parse_genes_list(xml_file_name):
    """
    Given the path to KEGG pathway xml file extract all 'gene'
    enties and construct a list of Gene objects from it.
    """
    tree = ElementTree.parse(xml_file_name)
    genes = (e for e in tree.findall('entry') if e.attrib['type'] == 'gene')
    return [parse_gene_entry(g) for g in genes]
