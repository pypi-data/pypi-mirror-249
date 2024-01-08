import unittest

from mlsurf.data_util import topological_sort


class TestTopologicalSort(unittest.TestCase):

    def test_sort(self):
        d1 = {'name': 1}
        d2 = {'name': 2, 'depends_on': 3}
        d3 = {'name': 3}
        d4 = {'name': 4}
        d5 = {'name': 5, 'depends_on': 2}
        d6 = {'name': 6}
        d7 = {'name': 7, 'depends_on': 3}
        d8 = {'name': 'eight', 'depends_on': 7}
        d9 = {'name': 'nine', 'depends_on': 'eight'}

        sorted_dicts = topological_sort([d8, d9, d1, d2, d3, d4, d5, d6, d7])

        # Create a mapping from name to position in the sorted list
        positions = {d['name']: i for i, d in enumerate(sorted_dicts)}

        # Check if each dictionary is after its dependency
        self.assertTrue(positions[3] < positions[2])  # d3 before d2
        self.assertTrue(positions[2] < positions[5])  # d2 before d5
        self.assertTrue(positions[3] < positions[7])  # d3 before d7
        self.assertTrue(positions[7] < positions['eight'])  # d7 before d8
        self.assertTrue(positions['eight'] < positions['nine'])  # d8 before d9


# Run the unit test
unittest.main(argv=[''], exit=False)
