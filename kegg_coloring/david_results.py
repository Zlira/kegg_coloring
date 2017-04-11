import pandas as pd


def read_david_res(file_path):
    return DavidRes(pd.read_csv(file_path, sep='\t'))


class DavidRes(pd.DataFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pathway_list = None

    def list_pathways(self):
        """
        Returns dataframe with two columns 'kegg_id' and 'term'
        """
        # cache the list
        if self._pathway_list is None:
            self._pathway_list = pd.DataFrame(
                self.Term.str.split(':').tolist(),
                columns=['kegg_id', 'term']
            )
        return self._pathway_list

    def gene_list_for_pathway(self, pathway_id):
        """
        Returns a list of strings - gene names of genes from the
        specified pathway.
        """
        return (
            self[self.Term.str.contains(pathway_id)].Genes
            .str.lower()
            .str.split(', ')
            .tolist()
        )[0]

    def get_pathway_id_by_name(self, pathway_name):
        """
        Given a pathway_name returns its kegg_id.
        """
        # TODO handle no/multiple matches
        return (
            self.list_pathways()
            .query(f'term == "{pathway_name}"')
            .iloc[0]['kegg_id']
        )
