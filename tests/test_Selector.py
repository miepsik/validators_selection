from Selector import Selector
from UTA import UTA
import pandas as pd
import unittest

class TestSelector(unittest.TestCase):

    def test_empty(self):
        df = pd.read_csv('validators.csv')
        df.columns = ["stash_address", "Commission (in %)", "Self Stake (in DOT)", "Total Stake (in DOT)", "Era Points", "Cluster Size", "Voters"]
        df = df.set_index("stash_address")
        model = UTA(df, negative=["Commission (in %)", "Total Stake (in DOT)"], not_monotonic=["Voters", "Cluster Size"], n_probes=250, goal_function='average', n_points=4, additional_points={"Commission (in %)": {-0.5: "left none"}})
        selector = Selector(df)
        choice = selector.select(model)
        print(choice)


if __name__ == '__main__':
    unittest.main()

