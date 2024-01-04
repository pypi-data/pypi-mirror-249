from src.cantopy.xenocanto_components import ResultPage
import pytest

from src.cantopy.xenocanto_components.query_result import QueryResult


@pytest.mark.parametrize(
    "example_queryresult_fixture_name, expected_num_pages",
    [
        ("example_single_page_queryresult", 1),
        ("example_two_page_queryresult", 2),
    ],
)
def test_query_result_initialization(
    example_queryresult_fixture_name: str,
    expected_num_pages: int,
    example_result_page_page_1: ResultPage,
    example_result_page_page_2: ResultPage,
    request: pytest.FixtureRequest,
):
    """Test the initialization of a QueryResult object.

    Parameters
    ----------
    example_queryresult_fixture_name : str
        Fixture name of the example QueryResult object based on the example XenoCanto API response.
    expected_num_pages : int
        Expected number of ResultPage instances in the QueryResult object.
    example_result_page_page_1 : ResultPage
        Example ResultPage object based on the example page 2 XenoCanto API response.
    example_result_page_page_2 : ResultPage
        Example ResultPage object based on the example page 2 XenoCanto API response.
    request : pytest.FixtureRequest
        Request fixture to get the example QueryResult object.
    """
    example_queryresult: QueryResult = request.getfixturevalue(
        example_queryresult_fixture_name
    )

    # Check attributes
    assert example_queryresult.available_num_recordings == 67810
    assert example_queryresult.available_num_species == 1675
    assert example_queryresult.available_num_pages == 136

    # Check stored result pages
    assert len(example_queryresult.result_pages) == expected_num_pages
    if example_queryresult_fixture_name == "example_single_page_queryresult":
        assert example_queryresult.result_pages[0] == example_result_page_page_1
    elif example_queryresult_fixture_name == "example_two_page_queryresult":
        assert example_queryresult.result_pages[0] == example_result_page_page_1
        assert example_queryresult.result_pages[1] == example_result_page_page_2


@pytest.mark.parametrize(
    "example_queryresult_fixture_name",
    [
        ("example_single_page_queryresult"),
        ("example_two_page_queryresult"),
    ],
)
def test_query_result_get_all_recordings(
    example_queryresult_fixture_name: str,
    example_result_page_page_1: ResultPage,
    example_result_page_page_2: ResultPage,
    request: pytest.FixtureRequest,
):
    """Test the QueryResult's functionality to return all the contained recordings across ResultPages.

    Parameters
    ----------
    example_queryresult_fixture_name : str
        Fixture name of the example QueryResult object based on the example XenoCanto API response.
    example_result_page_page_1 : ResultPage
        Example ResultPage object based on the example page 1 XenoCanto API response.
    example_result_page_page_2 : ResultPage
        Example ResultPage object based on the example page 2 XenoCanto API response.
    request : pytest.FixtureRequest
        Request fixture to get the example QueryResult object.
    """

    example_queryresult: QueryResult = request.getfixturevalue(
        example_queryresult_fixture_name
    )

    # Get all the recordings contained in the example_queryresult
    recordings_list = example_queryresult.get_all_recordings()

    # The correct total number of recordings that should be returned is equal to the sum of the
    # amount of recordings in each result page instance.
    num_recordings = 0
    if example_queryresult_fixture_name == "example_single_page_queryresult":
        num_recordings += len(example_result_page_page_1.recordings)
    elif example_queryresult_fixture_name == "example_two_page_queryresult":
        num_recordings += len(example_result_page_page_1.recordings)
        num_recordings += len(example_result_page_page_2.recordings)
    assert len(recordings_list) == num_recordings

    # The specific recordings should also be in the correct order
    if example_queryresult_fixture_name == "example_single_page_queryresult":
        assert recordings_list == example_result_page_page_1.recordings
    elif example_queryresult_fixture_name == "example_two_page_queryresult":
        assert (
            recordings_list[: len(example_result_page_page_1.recordings)]
            == example_result_page_page_1.recordings
        )
        assert (
            recordings_list[len(example_result_page_page_1.recordings) :]
            == example_result_page_page_2.recordings
        )
