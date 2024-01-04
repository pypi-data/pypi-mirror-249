import marcuslion as ml
import json

ref = {}


def test():
    print(__name__)
    test_list()
    # test_search()
    # test_query()
    test_download()
    # test_subscribe()
    # test_recently()


def test_list():
    print(__name__ + ".test_list()")
    df = ml.indicators.list()
    print(df)


def test_search():
    print(__name__ + ".test_search(SMA)")
    df = ml.indicators.search("SMA")
    print(df)


def test_query():
    print(__name__ + ".test_query()")
    df = ml.indicators.query('RSI')
    print("NAME: RSI")
    print(df)
    df = ml.indicators.query('64bf885d9c8a7c1253938467')
    print("UUID: 64bf885d9c8a7c1253938467")
    print(df)


def test_download():
    print(__name__ + ".test_download()")
    args = json.dumps({"period": 5})
    product = json.dumps({
        "symbol": "USDT",
        "key": "BTC/USDT",
        "provider": "xtrd",
        "market": "OKEX",
        "providerInfo": "xtrd/OKEX"
    })
    df = ml.indicators.download(
        {"id": "SMA", "product": product, "library": "TA4J", "interval": "PT1M", "args": args})
    print(df.head(10))


def test_subscribe():
    print(__name__ + ".test_subscribe()")
    df = ml.indicators.subscribe([{"id": "SMA"},
                                  {"product": "IBM"},
                                  {"interval": "PT1M"}])
    print(df)


def test_recently():
    print(__name__ + ".test_recently()")
    df = ml.indicators.recently()
    print(df)
