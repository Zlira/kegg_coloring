#! /usr/bin/env python

import argparse
from csv import reader

from kegg_coloring.palette import Palette
from kegg_coloring.pathway_scheme import PathwayImg


parser = argparse.ArgumentParser()
parser.add_argument(
    '-x', '--xml_file', help='Path to KEGG pathway xml file',
)
parser.add_argument(
    '-i', '--img_file', help='Path to KEGG pathway image',
)
parser.add_argument(
    '-g', '--genes_file', help='Path to .csv files with gene list',
)
parser.add_argument(
    '-o', '--output_img', help='Path to output image',
)


def color_gene_set_by_vals(pathway, gene_set):
    palette = Palette(list(gene_set.values()))
    for gene_name, val in gene_set.items():
        color = palette.get_color(val)
        pathway.color_gene(gene_name, color)
    return pathway.picture()


def parse_genes_file(genes_file):
    with open(genes_file) as infile:
        return {
            gene: float(val) for gene, val in reader(infile)
        }


def main(xml_file, img_file, genes_file, output_img):
    pathway = PathwayImg(xml_file, img_file)
    genes = parse_genes_file(genes_file)
    output = color_gene_set_by_vals(pathway, genes)
    output.save(output_img)


if __name__ == '__main__':
    args = vars(parser.parse_args())
    main(**args)
