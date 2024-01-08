import unittest
import numpy as np

from mlsurf.data_splitting import StratifiedSplitter


class TestStratifiedSplitter(unittest.TestCase):
    def setUp(self):
        self.splitter = StratifiedSplitter()

    def test_split_data_various_shares(self):
        shares_configs = [
            # NOTE: these tests are created in a way so that rounding errors don't occurr.
            # Care should be used when using the splitting function with regards to rounding errors, e.g.,
            # if you are splitting a very small dataset, then it's best to use absolute numbers if the ratios
            # don't go into the length of the data without remainders.
            (100, [0.5, 0.25, 0.25], [80, None], [80, 20]),
            (100, [0.5, 0.25, 0.25], [0.8, None], [80, 20]),
            (100, [0.5, 0.25, 0.25], [20, 8, 52, None], [20, 8, 52, 20]),
            (100, [0.5, 0.25, 0.25], [0.2, 0.08, 0.52, None], [20, 8, 52, 20]),
            (100, [0.5, 0.25, 0.25], [0.2, 8, 0.52, None], [20, 8, 52, 20]),
            (200, [0.5, 0.25, 0.25], [0.5, 0.2, 0.1], [100, 40, 20]),  # 80% of data used, 20% left out
            (400, [0.5, 0.25, 0.25], [80, 60, 40, 32, 24], [80, 60, 40, 32, 24]),  # Total of 59, 41 left out
            (400, [0.5, 0.25, 0.25], [80, 0.15, 40, 0.08, 24], [80, 60, 40, 32, 24]),
            (100, [0.2, 0.2, 0.2, 0.2, 0.2], [0.25, 0.25, 25, 25], [25, 25, 25, 25]),  # Equal splits
            (100, [0.2, 0.2, 0.2, 0.2, 0.2], [0.25, 0.25, 25, None], [25, 25, 25, 25]),  # Equal splits
            (100, [0.6, 0.2, 0.2], [10, None], [10, 90]),  # 10 in first split, rest in second
            (90, [0.6, 0.2, 0.2], [0.333333, 0.333333, 0.333333], [30, 30, 30]),
            (90, [0.6, 0.4], [0.333333, 0.333333, None], [30, 30, 30]),
            (100, [0.6, 0.4], [50, 0.5], [50, 50]),
            (100, [0.2, 0.2, 0.2, 0.2, 0.2], [5], [5])
        ]

        for data_len, y_ratios, shares, expected_split_sizes in shares_configs:
            repeated_labels = [[i] * int(data_len * y_ratios[i]) for i in range(len(y_ratios))]
            y_data = np.array([label for sublist in repeated_labels for label in sublist])
            np.random.shuffle(y_data)
            data = {'y': y_data}

            with self.subTest(shares=shares):
                indices_splits = self.splitter.get_split_idxs(data, data_len, shares)
                self.assertEqual(len(indices_splits), len(expected_split_sizes))

                # Verify the number of indices in each split
                for i, expected_size in enumerate(expected_split_sizes):
                    self.assertEqual(len(indices_splits[i]), expected_size, f"Split {i} has incorrect size")

                # Verify stratification and total split size
                self.verify_stratification(indices_splits, shares, data_len, y_data)
                total_split_size = sum(len(split) for split in indices_splits)
                self.assertLessEqual(total_split_size, data_len)

    def verify_stratification(self, indices_splits, shares, data_len, y_data):
        total_counts = np.bincount(y_data)
        for i, indices in enumerate(indices_splits):
            split_counts = np.bincount(y_data[indices], minlength=total_counts.size)
            proportion = split_counts / total_counts
            expected_proportions = []
            for _ in range(len(proportion)):
                if shares[i] is None:
                    exp_prop = 1 - sum(s / data_len if isinstance(s, int) else s for s in shares[0:i])
                elif isinstance(shares[i], int):
                    exp_prop = shares[i] / data_len
                elif isinstance(shares[i], float):
                    exp_prop = shares[i]
                else:
                    raise "shares[i] is an unexpected type"
                expected_proportions.append(exp_prop)
            try:
                np.testing.assert_array_almost_equal(proportion, expected_proportions, decimal=5,
                                                     err_msg="Stratification is not even across splits")
                #assert all(proportion == expected_proportions), "Stratification is not even across splits"
            except Exception:
                raise
