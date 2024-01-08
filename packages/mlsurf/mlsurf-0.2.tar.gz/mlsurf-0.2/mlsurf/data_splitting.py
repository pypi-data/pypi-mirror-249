from abc import ABCMeta, abstractmethod

import numpy as np
from sklearn.model_selection import train_test_split


class SplitterInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_split_idxs(self, data: dict, data_len: int, shares: list) -> list:
        """We return indexes rather than the data already split up, because it saves space by doing that.
        i.e., copying the X data could be very memory intensive, and so I'd rather leave this to invoking
        code to decide how to deal with the more memory intensive parts."""
        pass


class RandomSplitter(SplitterInterface):
    # GPT: https://chat.openai.com/c/f552546c-283d-4bdb-80d5-5babe2258c44
    def get_split_idxs(self, data: dict, data_len: int, shares: list) -> list:
        shuf_idxs = np.arange(data_len)

        # Shuffle the indices
        np.random.shuffle(shuf_idxs)

        # Calculate split indices based on shares
        splits = []
        start_idx = 0

        for i, share in enumerate(shares):
            if share is None:
                # Handle the None case for the last share
                if i != len(shares) - 1:
                    raise ValueError("None can only be used for the last share")
                end_idx = data_len
            elif isinstance(share, float):  # Share is a ratio
                num_indices = int(round(share * data_len))
                end_idx = start_idx + num_indices
            elif isinstance(share, int):  # Share is an absolute number
                end_idx = min(start_idx + share, data_len)  # Ensure it doesn't exceed data_len
            else:
                raise ValueError("Shares must be either int, float, or None")

            splits.append(shuf_idxs[start_idx:end_idx])
            start_idx = end_idx

        return splits


class StratifiedSplitter(SplitterInterface):
    def __init__(self, stratify_prefix='y'):
        self.stratify_prefix = stratify_prefix

    def get_split_idxs(self, data: dict, data_len: int, shares: list) -> list:
        # Assuming 'y' key exists in data dictionary
        y_data = data[self.stratify_prefix]

        # Shuffle indices
        shuf_idxs = np.arange(data_len)
        np.random.shuffle(shuf_idxs)

        # Initialize splits list and remaining indices
        splits = []
        remaining_indxs = shuf_idxs

        n_classes = len(np.unique(y_data))

        for i, share in enumerate(shares):
            if share is None:
                if i != len(shares) - 1:
                    raise ValueError("None can only be used for the last share")
                splits.append(remaining_indxs)
                break

            if isinstance(share, float):
                # Calculate the proportion of remaining indices to split
                num_elements = round(share * data_len)
            elif isinstance(share, int):
                # Use the absolute number but not more than the remaining elements
                num_elements = min(share, len(remaining_indxs))
            else:
                raise ValueError("Shares must be either int, float, or None")

            # FIXME: come up with better logic for the n_classes problem.
            #        To understand the issue, take away `+ n_classes` and run tests.
            if num_elements + n_classes >= len(remaining_indxs):
                if i != len(shares) - 1:
                    raise "Haven't finished dishing out shares"
                splits.append(remaining_indxs)
                break

            # Perform stratified split to get indices for this share
            temp_indxs, remaining_indxs, _, remainin_labels = train_test_split(
                remaining_indxs, y_data[remaining_indxs],
                train_size=num_elements, stratify=y_data[remaining_indxs])

            splits.append(temp_indxs)

        return splits
