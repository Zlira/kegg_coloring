import pandas as pd

from kegg_coloring.palette import Palette


class CuffdiffOutput(pd.DataFrame):
    # TODO read about views and copies of dataframes. Current
    # aproach with coping everything may not be the most
    # memory efficient way to do this.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._palette = None

    def select_significant_by_samples(self, sample_1, sample_2):
        # TODO this method does too much. Slipt it into at least
        # three - for filering by samples, for selecting
        # significant difference and for filtering out multiple
        # and absent genes.
        return self.__class__(self.query(
            f'sample_1 == "{sample_1}" & '
            f'sample_2 == "{sample_2}" & '
            'status == "OK" & '
            'significant == "yes" & '
            'gene != "-" & '
            '~gene.str.contains(",")'
        ))

    def select_gene_subset_by_name(self, genes):
        return self.__class__(
            self[self.gene.str.lower().isin(genes)]
        )

    def gene_expression_dict_by_name(self, genes):
        # WARN for this to work all genes must be unique
        genes_df = self.select_gene_subset_by_name(genes)
        return {
            row.gene: row['log2(fold_change)'] for
            i, row in genes_df.iterrows()
        }

    def scaled_palette(self):
        if self._palette is None:
            self._palette = Palette(self['log2(fold_change)'])
        return self._palette
