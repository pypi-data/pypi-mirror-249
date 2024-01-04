import marcuslion as ml
import pandas as pd


def test():
    print(__name__)

    miscellaneous = ml.datasets.download("kaggle", "jessicali9530/animal-crossing-new-horizons-nookplaza-dataset",
                                         "miscellaneous.csv")

    print(pd.read_csv(miscellaneous).head())


def test_list(self, ref):
    return ml.datasets.list()


def test_search(self, search):
    return ml.datasets.search()

