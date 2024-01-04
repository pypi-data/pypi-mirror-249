import marcuslion as ml
from tests import test_indicators, test_providers, test_models, test_datasets, test_support, test_timeseries, \
    test_projects, test_documents, test_dataframes, test_ussec

if __name__ == '__main__':
    try:
        help(ml)

        # test_dataframes.test()
        # test_datasets.test()
        # test_documents.test()

        test_indicators.test()
        #
        # test_models.test()
        # test_projects.test()
        # test_providers.test()
        #
        # test_support.test()
        # test_timeseries.test()

        # test_ussec.test()

    except Exception as e:
        print("Exception ", e.with_traceback(e.__traceback__))

