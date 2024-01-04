import pandas as pd
import marcuslion as ml


def test():
    print(__name__)

    print(ml.providers.list())
    print(ml.data_providers.list())

    df = ml.datasets.search("bike", "kaggle,usgov")
    print(df.tail(3))
