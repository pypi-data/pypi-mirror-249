import marcuslion as ml


def test():
    print(__name__)

    timeseries = ml.timeseries.list("BTC-USDT", "1m", 10)
    if timeseries is not None:
        print(timeseries.head(10))
    else:
        print("No timeseries data found")
