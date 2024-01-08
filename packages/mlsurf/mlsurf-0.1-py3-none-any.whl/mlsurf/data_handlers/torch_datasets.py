import numpy as np
from torch.utils.data import Dataset


class CircularList:
    def __init__(self):
        self.data = []

    def append(self, item):
        self.data.append(item)

    def __getitem__(self, index):
        if not self.data:
            raise IndexError("Indexing empty list")
        return self.data[index % len(self.data)]

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return repr(self.data)


class ContrastiveSelfSupTorchDataset(Dataset):
    """Group-oriented self-supervised dataset. This dataset class is characterised
    by retrieving two data samples (from the `x_tensor`) in the same group (`gid_tensor`)
    at a time. "gid" stands for group ID. Data samples may be in grouped for a variety of
    use cases, such as in the event of them being augmentations of one another. The
    primary use case is for contrastive (self-supervised) learning.

    There are multiple retrieval modes which alter the behaviour of how other data
    samples are selected from the same group for a particular index.
    RANDOM: this randomly selects another data sample from the same group.
    CYCLE: this ensures that all data samples are coupled with each other during
           retrieval a fair number of times. It does this by using wrapping all indexes
           for a particular group in a circular buffer, and keeps a count of how many
           times items have been retrieved from this group. Even when a wrapping
           data loader is in shuffle mode, one item will not be picked more than once
           when another item has not been retrieved yet, due to the sequential nature
           of the data loader. We can use this to our advantage by knowing that once
           the number of retrievals from this group reaches the group size, then we
           know all elements have been traversed (in this round). During this first
           round of retrievals, we simply couple each data sample in the group
           with the one that comes after it in the index list. After the first round,
           we can increment this 'skip number' so that now each data sample is coupled
           with the 2nd element after itself in the list, and so on. By using this logic
           we ensure that everything is coupled with everything as evenly as possible,
           and in O(1) space & time (from the perspective of each group; i.e., we
           only need to keep 3 numbers for each group to achieve this).
           WARNING: an issue in some circumstances could be that elements "closer" to
           one another in the list may be more similar than further apart. This can
           be resolved by ensuring that some shuffling has happened before constructing
           this dataset. And example is for sampling "sub flows" from a pcap file;
           sub flows closer together i.e., within a particular small snippet of thepcap
           file may have a tendency to be more similar than those further away in the
           pcap file."""
    RANDOM = 0
    CYCLE = 1

    def __init__(self, x_tensor, gid_tensor, retrieve_mode=RANDOM):
        # Load data and convert to tensors
        self.x_data = x_tensor
        self.gids = gid_tensor

        # Augmentation mode dictates how we pick the augmentations within aug groups
        self.retrieve_mode = retrieve_mode

        # GID dictionary for indexing
        self.gid_dict = {}
        self.update_gid_dict(self.gids)

        self.grp_counting = {}
        self.init_grp_counting()

    def update_gid_dict(self, gids, idx_add=0):
        # Update GID dictionary for grouping indices
        if self.retrieve_mode == self.CYCLE:
            list_cls = CircularList
        else:
            list_cls = list

        gid_dict = {}
        for idx, gid in enumerate(gids):
            idx += idx_add
            if gid.item() not in gid_dict:
                gid_dict[gid.item()] = list_cls()
            gid_dict[gid.item()].append(idx)
        self.gid_dict.update(gid_dict)

    def init_grp_counting(self):
        if self.retrieve_mode is self.CYCLE:
            for gid, gid_idxs in self.gid_dict.items():
                # create a new list with the elements corresponding to:
                # 1) number of elements in respective group
                # 2) skip num for the group (i.e., the element retrieved with the
                #    requested idx will be this number of elements further in the list,
                #    bearing in mind a circular buffer). This number will be incremented
                #    after all elements have been retrieved once.
                # 3) number of retrievals in this group so far. When this number reaches
                #    `len(gid_idxs)`, i.e., is equal to the first element, then it will
                #    be reset to 0, and the 2nd element will be incremented.
                self.grp_counting[gid] = [len(gid_idxs), 1, 0]

    def permute(self, permutation: tuple):
        # Permute x_data if needed
        self.x_data = self.x_data.permute(permutation)

    def __len__(self):
        # Dataset length
        return len(self.x_data)

    def random_aug(self, idx, gid):
        # Get the list of indices with the same GID
        same_gid_indices = self.gid_dict[gid]

        # better for large groups
        different_idx = idx
        while different_idx == idx:
            different_idx = np.random.choice(same_gid_indices)

        return different_idx

    def cycle_all(self, idx, gid):
        grp_counting = self.grp_counting[gid]

        # if number of traversed elements in this group exceeds the group size
        if grp_counting[2] >= grp_counting[0]:
            # reset element traversal count to 0
            grp_counting[2] = 0
            # if skip num exceeds group size
            if grp_counting[1] >= grp_counting[0]:
                # reset skip num to 1 (i.e., next element in group)
                grp_counting[1] = 1
            else:
                # else increment skip num by 1
                grp_counting[1] += 1

        # increment group traversal count by 1
        grp_counting[2] += 1

        return idx

    def __getitem__(self, idx):
        # Get GID for the current index
        gid = self.gids[idx].item()

        # determine which idx within same aug group to pick based on aug mode
        if self.retrieve_mode == self.RANDOM:
            different_idx = self.random_aug(idx, gid)
        elif self.retrieve_mode == self.CYCLE:
            different_idx = self.cycle_all(idx, gid)
        else:
            raise NotImplementedError()

        # Return the paired data
        return self.x_data[idx], self.x_data[different_idx]