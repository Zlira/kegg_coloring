import numpy as np

from kegg_coloring.utils import round_towards_inf


class Palette:

    # colors from seaborn 'RdBu_r' palette
    colors = np.array([
        [41, 113, 177],  # The blue end
        [107, 172, 208],
        [194, 221, 235],
        [247, 246, 246],
        [250, 204, 180],
        [228, 128, 101],
        [185,  39,  50]  # The red end
    ])

    def __init__(self, vals):
        self.unit = self._get_unit_len(vals)

    def _get_unit_len(self, vals):
        """
        Return the length of scale unit based on range of vals.
        The middle color of scale is reserved for exactly 0 only.
        """
        # need to filter vals so they don't include 'inf'
        vals = vals[~np.isinf(vals)]
        furthest_val = np.abs([np.max(vals), np.min(vals)]).max()
        return float(furthest_val) / ((len(self.colors) - 1) / 2)

    def get_color(self, val):
        """
        Based on unit length computed during initialization returns a color
        (as ndarray of RGB values) for a given value.
        """
        index = (len(self.colors) // 2 +
                 round_towards_inf(float(val) / self.unit))
        return self.colors[int(index)]
