import marcuslion as ml


def test():

    print(__name__)

    print(ml.models.list())
    print(ml.data_providers.list())

    df = ml.datasets.search("bike", "kaggle,usgov")
    print(df.tail(3))
