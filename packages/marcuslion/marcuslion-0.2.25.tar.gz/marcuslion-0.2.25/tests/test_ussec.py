import marcuslion as ml
import json


def _print_formatted(df):
    print(json.dumps(df, indent=2))


def test():
    print(__name__)
    cik = '1750'
    # test_list()
    test_fields(cik)
    # test_query(1750)
    test_units(cik, "us-gaap.EarningsPerShareBasicAndDiluted")


def test_list(cik: str):
    print(__name__ + ".test_list()")
    df = ml.us_sec.get_fields(cik)
    print(df)


def test_fields(cik: str):
    print(__name__ + ".test_fields()")
    df = ml.us_sec.get_fields(cik)
    _print_formatted(df)


def test_query(cik):
    print(__name__ + ".test_facts()")
    df = ml.us_sec.query(cik)
    print(df)


def test_units(cik, field):
    print(__name__ + ".test_units()")
    df = ml.us_sec.get_units(cik, field)
    _print_formatted(df)
