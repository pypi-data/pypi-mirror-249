from typing import Any, Dict, Generator, List
import pytest
import json
import os
from os.path import join
import pandas as pd
import shutil

from src.cantopy import DownloadManager
from src.cantopy.xenocanto_components import QueryResult, Recording, ResultPage


######################################################################
#### CONSTANTS
######################################################################
TEST_MAX_WORKERS = 8
TEST_DATA_BASE_FOLDER_PATH = (
    "/workspaces/CantoPy/resources/test_resources/test_data_folders"
)

######################################################################
#### XENOCANTO COMPONENT FIXTURES
######################################################################


@pytest.fixture(scope="session")
def example_xenocanto_query_response_page_1() -> (
    Dict[str, str | int | List[Dict[str, str]]]
):
    """An example dict of the query response of the XenoCanto API when sending a
    Query to recieve the result page with id 1.

    Returns
    -------
    Dict[str, str]
        The dictionary representation of an example query response of the XenoCanto API.
    """

    # Open the example XenoCanto query response
    with open(
        "resources/test_resources/example_xenocanto_query_response_page_1.json",
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


@pytest.fixture(scope="session")
def example_xenocanto_query_response_page_2() -> (
    Dict[str, str | int | List[Dict[str, str]]]
):
    """An example dict of the query response of the XenoCanto API when sending a
    Query to recieve the result page with id 2.

    Returns
    -------
    Dict[str, str | int | List[Dict[str, str]]]
        The dictionary representation of an example query response of the XenoCanto API.
    """

    # Open the example XenoCanto query response
    with open(
        "resources/test_resources/example_xenocanto_query_response_page_2.json",
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


@pytest.fixture(scope="session")
def example_fake_xenocanto_recording() -> Recording:
    """An example Recording object that is not actually from XenoCanto.

    Returns
    -------
    Recording
        The created fake Recording object.
    """

    # Open the example fake XenoCanto recording
    with open(
        "resources/test_resources/example_fake_xenocanto_recording.json",
        "r",
        encoding="utf-8",
    ) as file:
        return Recording(json.load(file))


@pytest.fixture(scope="session")
def example_query_metadata_page_1(
    example_xenocanto_query_response_page_1: Dict[str, str | int | List[Dict[str, str]]]
) -> Dict[str, str | int]:
    """Build a response metadata dict from the page 1 example XenoCanto API query response.

    Parameters
    ----------
    example_xenocanto_query_response_page_1 : Dict[str, str | int | List[Dict[str, str]]]
        The dictionary representation of example XenoCanto API query response.

    Returns
    -------
    Dict[str, str | int]
        Extracted response metadata from the example page 1 XenoCanto API query response.

    Raises
    ------
    ValueError
        If the type of values assigned to numRecordings, numSpecies or numPages keys in
        the query response dict is not a string.
    """

    if (
        isinstance(example_xenocanto_query_response_page_1["numRecordings"], str)
        and isinstance(example_xenocanto_query_response_page_1["numSpecies"], str)
        and isinstance(example_xenocanto_query_response_page_1["numPages"], int)
    ):
        return {
            "available_num_recordings": int(
                example_xenocanto_query_response_page_1["numRecordings"]
            ),
            "available_num_species": int(
                example_xenocanto_query_response_page_1["numSpecies"]
            ),
            "available_num_pages": example_xenocanto_query_response_page_1["numPages"],
        }
    else:
        raise ValueError(
            f"Unexpected type of values assigned to numRecordings, numSpecies or numPages keys: \
            {example_xenocanto_query_response_page_1}"
        )


@pytest.fixture(scope="session")
def example_query_metadata_page_2(
    example_xenocanto_query_response_page_2: Dict[str, str | int | List[Dict[str, str]]]
) -> Dict[str, str | int]:
    """Build a response metadata dict from the page 2 example XenoCanto API query response.

    Parameters
    ----------
    example_xenocanto_query_response_page_2 : Dict[str, str | int | List[Dict[str, str]]]
        The dictionary representation of example page 2 XenoCanto API query response.

    Returns
    -------
    Dict[str, str | int]
        Extracted response metadata from the example XenoCanto API query response.

    Raises
    ------
    ValueError
        If the type of values assigned to numRecordings, numSpecies or numPages keys in
        the query response dict is not a string.
    """
    if (
        isinstance(example_xenocanto_query_response_page_2["numRecordings"], str)
        and isinstance(example_xenocanto_query_response_page_2["numSpecies"], str)
        and isinstance(example_xenocanto_query_response_page_2["numPages"], int)
    ):
        return {
            "available_num_recordings": int(
                example_xenocanto_query_response_page_2["numRecordings"]
            ),
            "available_num_species": int(
                example_xenocanto_query_response_page_2["numSpecies"]
            ),
            "available_num_pages": example_xenocanto_query_response_page_2["numPages"],
        }
    else:
        raise ValueError(
            f"Unexpected type of values assigned to numRecordings, numSpecies or numPages keys: \
            {example_xenocanto_query_response_page_2}"
        )


@pytest.fixture(scope="session")
def example_result_page_page_1(
    example_xenocanto_query_response_page_1: Dict[str, str | int | List[Dict[str, str]]]
) -> ResultPage:
    """Build a ResultPage object from the example page 1 XenoCanto API query response.

    Parameters
    ----------
    example_xenocanto_query_response_page_1 : Dict[str, str | int | List[Dict[str, str]]]
        The dictionary representation of example page 1 XenoCanto API query response.

    Returns
    -------
    ResultPage
        The ResultPage object created from the example XenoCanto API query response.
    """
    return ResultPage(example_xenocanto_query_response_page_1)


@pytest.fixture(scope="session")
def example_result_page_page_2(
    example_xenocanto_query_response_page_2: Dict[str, str | int | List[Dict[str, str]]]
) -> ResultPage:
    """Build a ResultPage object from the example page 2 XenoCanto API query response.

    Parameters
    ----------
    example_xenocanto_query_response_page_2 : Dict[str, str | int | List[Dict[str, str]]]
        The dictionary representation of example page 2 XenoCanto API query response.

    Returns
    -------
    ResultPage
        The ResultPage object created from the example XenoCanto API query response.
    """
    return ResultPage(example_xenocanto_query_response_page_2)


@pytest.fixture(scope="session")
def example_recording_1_from_example_xenocanto_query_response_page_1(
    example_xenocanto_query_response_page_1: Dict[str, str | int | List[Dict[str, str]]]
) -> Recording:
    """Build a Recording object based on the first recording in the example page 1
    XenoCanto API query response.

    Parameters
    ----------
    example_xenocanto_query_response_page_1 : Dict[str, str | int | List[Dict[str, str]]]
        The dictionary representation of example page 1 XenoCanto API query response.

    Returns
    -------
    Recording
        The created Recording object.
    """

    # Handle the string case, which should not be possible
    if not isinstance(example_xenocanto_query_response_page_1["recordings"], list):
        raise ValueError(
            f"Unexpected type of values assigned to recordings key: \
            {example_xenocanto_query_response_page_1['recordings']}"
        )

    return Recording(example_xenocanto_query_response_page_1["recordings"][0])


@pytest.fixture(scope="session")
def example_single_page_queryresult(
    example_query_metadata_page_1: Dict[str, str | int],
    example_result_page_page_1: ResultPage,
) -> QueryResult:
    """Build a single-page QueryResult object based on the example page 1 XenoCanto API
    query response.

    Parameters
    ----------
    example_query_metadata_page_1 : Dict[str, str | int | List[Dict[str, str]]]
        The extracted metadata from the example page 1 XenoCanto API query response.
    example_result_page : ResultPage
        The ResultPage object created from the example page 1 XenoCanto API query response

    Returns
    -------
    QueryResult
        The constructed single-page QueryResult object.
    """

    return QueryResult(example_query_metadata_page_1, [example_result_page_page_1])


@pytest.fixture(scope="session")
def example_two_page_queryresult(
    example_query_metadata_page_1: Dict[str, str | int],
    example_result_page_page_1: ResultPage,
    example_result_page_page_2: ResultPage,
) -> QueryResult:
    """Build a two-page QueryResult object based on the example page 1 and 2 XenoCanto API
    query responses.

    Parameters
    ----------
    example_query_metadata_page_1 : Dict[str, int]
        The extracted metadata from the example page 1 XenoCanto API query response.
        Page 2 metadata is the same as page 1 metadata, so this is not needed.
    example_result_page_page_1 : ResultPage
        The ResultPage object created from the example page 1 XenoCanto API query response.
    example_result_page_page_2 : ResultPage
        The ResultPage object created from the example page 2 XenoCanto API query response.

    Returns
    -------
    QueryResult
        The constructed two-page QueryResult object.
    """

    # Build the resultpages
    result_pages: List[ResultPage] = []
    result_pages.append(example_result_page_page_1)
    result_pages.append(example_result_page_page_2)

    return QueryResult(example_query_metadata_page_1, result_pages)


######################################################################
#### DOWNLOADMANAGER FIXTURES
######################################################################


@pytest.fixture
def empty_download_data_base_path() -> Generator[str, Any, Any]:
    """Logic for setting up and breaking down a new empty data folder.

    Yields
    ------
    Generator[str, Any, Any]
        Return the string path to the newly created empty data folder.
    """
    # Pre-execution configuration
    empty_download_data_base_path = join(
        TEST_DATA_BASE_FOLDER_PATH, "empty_test_data_folder"
    )
    os.mkdir(empty_download_data_base_path)

    yield empty_download_data_base_path

    # After exectution cleanup
    shutil.rmtree(empty_download_data_base_path)


@pytest.fixture
def partially_filled_download_data_base_path(
    spot_winged_wood_quail_partial_test_recording_metadata: pd.DataFrame,
    little_nightjar_partial_test_recording_metadata: pd.DataFrame,
) -> Generator[str, Any, Any]:
    """Logic for setting up and breaking down a new partially-filled data folder.

    Upon creation, this folder will already contain part of the recordings returned by
    the example pages 1 and 2 XenoCanto API response. This new folder has the following structure:
    |- folder_root
    |---- spot_winged_wood_quail
    |------- 581411.mp3
    |------- spot_winged_wood_quail_recording_metadata.csv
    |---- little_nightjar
    |------- 196385.mp3
    |------- 220365.mp3
    |------- little_nightjar_recording_metadata.csv

    Parameters
    ----------
    spot_winged_wood_quail_partial_test_recording_metadata : pd.DataFrame
        The test recording metadata for the spot-winged wood quail recordings that are already
        present.
    little_nightjar_partial_test_recording_metadata : pd.DataFrame
        The test recording metadata for the little nightjar recordings that are already
        present.

    Yields
    ------
    Generator[str, Any, Any]
        Return the string path to the newly created partially-filled data folder.
    """
    # Pre-execution configuration
    partially_filled_data_base_path = join(
        TEST_DATA_BASE_FOLDER_PATH, "partially_filled_test_data_folder"
    )
    os.mkdir(partially_filled_data_base_path)

    # Partially fill the newly created folder
    os.mkdir(join(partially_filled_data_base_path, "spot_winged_wood_quail"))
    open(
        join(partially_filled_data_base_path, "spot_winged_wood_quail", "581411.mp3"),
        "x",
    )
    spot_winged_wood_quail_partial_test_recording_metadata.to_csv(
        join(
            partially_filled_data_base_path,
            "spot_winged_wood_quail",
            "spot_winged_wood_quail_recording_metadata.csv",
        ),
        index=False,
    )
    os.mkdir(join(partially_filled_data_base_path, "little_nightjar"))
    open(join(partially_filled_data_base_path, "little_nightjar", "196385.mp3"), "x")
    open(join(partially_filled_data_base_path, "little_nightjar", "220365.mp3"), "x")
    little_nightjar_partial_test_recording_metadata.to_csv(
        join(
            partially_filled_data_base_path,
            "little_nightjar",
            "little_nightjar_recording_metadata.csv",
        ),
        index=False,
    )

    yield partially_filled_data_base_path

    # After exectution cleanup
    shutil.rmtree(partially_filled_data_base_path)


@pytest.fixture
def empty_data_folder_download_manager(empty_download_data_base_path: str):
    """Build a DownloadManager instance with its download folder set to a new empty folder.

    Parameters
    ----------
    empty_download_data_base_path : str
        The path to a newly created empty download folder.

    Returns
    -------
    DownloadManager
        The created DownloadManager instance.
    """
    return DownloadManager(empty_download_data_base_path, max_workers=TEST_MAX_WORKERS)


@pytest.fixture
def partially_filled_data_folder_download_manager(
    partially_filled_download_data_base_path: str,
):
    """Build a DownloadManager instance with its download folder set a partially-filled data folder.

    Parameters
    ----------
    partially_filled_download_data_base_path : str
        The path to a newly created but partially-filled data folder.

    Returns
    -------
    DownloadManager
        The created DownloadManager instance.
    """
    return DownloadManager(
        partially_filled_download_data_base_path, max_workers=TEST_MAX_WORKERS
    )


@pytest.fixture
def fake_data_folder_download_manager():
    """Build a DownloadManager instance with its download folder set to a fake/non-existant
    download folder. This DownloadManager instance can be used when we don't need to
    test any file storage functionality of this class.

    Returns
    -------
    DownloadManager
        The created DownloadManager instance.
    """
    return DownloadManager("fake/path", max_workers=TEST_MAX_WORKERS)


@pytest.fixture
def little_nightjar_full_test_recording_metadata() -> pd.DataFrame:
    """Load the full test recording metadata for the little nightjar.

    Returns
    -------
    pd.DataFrame
        The loaded test recording metadata for the little nightjar.
    """
    return (
        pd.read_csv(  # type: ignore
            "resources/test_resources/little_nightjar_full_test_recording_metadata.csv"
        )
        .sort_values(by=["recording_id"])
        .reset_index(drop=True)
    )


@pytest.fixture
def spot_winged_wood_quail_full_test_recording_metadata() -> pd.DataFrame:
    """Load the full test recording metadata for the spot-winged wood quail.

    Returns
    -------
    pd.DataFrame
        The loaded test recording metadata for the spot-winged wood quail.
    """
    return (
        pd.read_csv(  # type: ignore
            "resources/test_resources/spot_winged_wood_quail_full_test_recording_metadata.csv"
        )
        .sort_values(by=["recording_id"])
        .reset_index(drop=True)
    )


@pytest.fixture
def combined_full_test_recording_metadata(
    little_nightjar_full_test_recording_metadata: pd.DataFrame,
    spot_winged_wood_quail_full_test_recording_metadata: pd.DataFrame,
) -> pd.DataFrame:
    """Load the full test recording metadata for the little nightjar and the spot-winged wood quail.

    Parameters
    ----------
    little_nightjar_full_test_recording_metadata : pd.DataFrame
        The loaded full test recording metadata for the little nightjar.
    spot_winged_wood_quail_full_test_recording_metadata : pd.DataFrame
        The loaded full test recording metadata for the spot-winged wood quail.

    Returns
    -------
    pd.DataFrame
        The loaded test recording metadata for the little nightjar and the spot-winged wood quail.
    """
    return (
        pd.concat(  # type: ignore
            [
                little_nightjar_full_test_recording_metadata,
                spot_winged_wood_quail_full_test_recording_metadata,
            ]
        )
        .sort_values(by=["recording_id"])
        .reset_index(drop=True)
    )


@pytest.fixture
def little_nightjar_partial_test_recording_metadata() -> pd.DataFrame:
    """Load the partial test recording metadata for the little nightjar.

    Returns
    -------
    pd.DataFrame
        The loaded test recording metadata for the little nightjar.
    """
    return (
        pd.read_csv(  # type: ignore
            "resources/test_resources/little_nightjar_partial_test_recording_metadata.csv"
        )
        .sort_values(by=["recording_id"])
        .reset_index(drop=True)
    )


@pytest.fixture
def spot_winged_wood_quail_partial_test_recording_metadata() -> pd.DataFrame:
    """Load the partial test recording metadata for the spot-winged wood quail.

    Returns
    -------
    pd.DataFrame
        The loaded test recording metadata for the spot-winged wood quail.
    """
    return (
        pd.read_csv(  # type: ignore
            "resources/test_resources/spot_winged_wood_quail_partial_test_recording_metadata.csv"
        )
        .sort_values(by=["recording_id"])
        .reset_index(drop=True)
    )


@pytest.fixture
def combined_partial_test_recording_metadata(
    little_nightjar_partial_test_recording_metadata: pd.DataFrame,
    spot_winged_wood_quail_partial_test_recording_metadata: pd.DataFrame,
) -> pd.DataFrame:
    """Load the partial test recording metadata for the little nightjar and the spot-winged wood quail.

    Parameters
    ----------
    little_nightjar_partial_test_recording_metadata : pd.DataFrame
        The loaded partial test recording metadata for the little nightjar.
    spot_winged_wood_quail_partial_test_recording_metadata : pd.DataFrame
        The loaded partial test recording metadata for the spot-winged wood quail.

    Returns
    -------
    pd.DataFrame
        The loaded test recording metadata for the little nightjar and the spot-winged wood quail.
    """
    return (
        pd.concat(  # type: ignore
            [
                little_nightjar_partial_test_recording_metadata,
                spot_winged_wood_quail_partial_test_recording_metadata,
            ]
        )
        .sort_values(by=["recording_id"])
        .reset_index(drop=True)
    )


@pytest.fixture
def little_nightjar_to_add_test_recording_metadata() -> pd.DataFrame:
    """Load the test recording metadata for the little nightjar that we want to add.

    Returns
    -------
    pd.DataFrame
        The loaded test recording metadata for the little nightjar.
    """
    return (
        pd.read_csv(  # type: ignore
            "resources/test_resources/little_nightjar_to_add_test_recording_metadata.csv"
        )
        .sort_values(by=["recording_id"])
        .reset_index(drop=True)
    )


@pytest.fixture
def spot_winged_wood_quail_to_add_test_recording_metadata() -> pd.DataFrame:
    """Load the test recording metadata for the spot-winged wood quail that we want to add.

    Returns
    -------
    pd.DataFrame
        The loaded test recording metadata for the spot-winged wood quail.
    """
    return (
        pd.read_csv(  # type: ignore
            "resources/test_resources/spot_winged_wood_quail_to_add_test_recording_metadata.csv"
        )
        .sort_values(by=["recording_id"])
        .reset_index(drop=True)
    )


@pytest.fixture
def combined_to_add_test_recording_metadata(
    little_nightjar_to_add_test_recording_metadata: pd.DataFrame,
    spot_winged_wood_quail_to_add_test_recording_metadata: pd.DataFrame,
) -> pd.DataFrame:
    """Load the test recording metadata for the little nightjar and the spot-winged wood quail that we want to add.

    Parameters
    ----------
    little_nightjar_to_add_test_recording_metadata : pd.DataFrame
        The loaded test recording metadata for the little nightjar we want to add.
    spot_winged_wood_quail_to_add_test_recording_metadata : pd.DataFrame
        The loaded test recording metadata for the spot-winged wood quail we want to add.

    Returns
    -------
    pd.DataFrame
        The loaded test recording metadata for the little nightjar and the spot-winged wood quail.
    """
    return (
        pd.concat(  # type: ignore
            [
                little_nightjar_to_add_test_recording_metadata,
                spot_winged_wood_quail_to_add_test_recording_metadata,
            ]
        )
        .sort_values(by=["recording_id"])
        .reset_index(drop=True)
    )
