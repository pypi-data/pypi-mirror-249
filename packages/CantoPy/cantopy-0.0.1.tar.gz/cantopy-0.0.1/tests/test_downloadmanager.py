from src.cantopy import DownloadManager
from src.cantopy.xenocanto_components import QueryResult, Recording
import os
from os.path import join
import pytest
import pandas as pd


@pytest.mark.parametrize(
    "example_queryresult_fixture_name, add_fake_recording",
    [
        ("example_single_page_queryresult", False),
        ("example_two_page_queryresult", False),
        ("example_single_page_queryresult", True),
        ("example_two_page_queryresult", True),
    ],
)
def test_downloadmanager_download_recordings(
    empty_data_folder_download_manager: DownloadManager,
    example_queryresult_fixture_name: str,
    add_fake_recording: bool,
    example_fake_xenocanto_recording: Recording,
    request: pytest.FixtureRequest,
):
    """Test the DownloadManager functionality for donwloading QueryResult
    in an empty folder.

    Parameters
    ----------
    empty_data_folder_download_manager : DownloadManager
        DownloadManager instance set to an empty data folder.
    example_queryresult_fixture_name : str
        Fixture name of the example QueryResult object based on the example XenoCanto API responses.
    add_fake_recording : bool
        Whether to add a fake recording to the recordings to download in order to test fail
        scenarios.
    example_fake_xenocanto_recording : Recording
        Example fake recording to add to the recordings to download in order to test fail
    request : pytest.FixtureRequest
        Request fixture to get the example QueryResult object.
    """
    example_queryresult: QueryResult = request.getfixturevalue(
        example_queryresult_fixture_name
    )

    recordings_to_download = example_queryresult.get_all_recordings()

    # Add fake recordings to the beginning and end of the recordings to download
    if add_fake_recording:
        recordings_to_download.insert(0, example_fake_xenocanto_recording)

    # Run the download functionality on a single page
    download_pass_or_fail = empty_data_folder_download_manager._download_all_recordings(  # type: ignore
        recordings_to_download
    )

    # Check if the download pass or fail dict has been generated correctly
    if example_queryresult_fixture_name == "example_single_page_queryresult":
        if add_fake_recording:
            assert len(download_pass_or_fail) == 4
            assert download_pass_or_fail["0"] == "fail"
        elif not add_fake_recording:
            assert len(download_pass_or_fail) == 3

        assert download_pass_or_fail["581412"] == "pass"
        assert download_pass_or_fail["581411"] == "pass"
        assert download_pass_or_fail["427716"] == "pass"
    elif example_queryresult_fixture_name == "example_two_page_queryresult":
        if add_fake_recording:
            assert len(download_pass_or_fail) == 7
            assert download_pass_or_fail["0"] == "fail"
        elif not add_fake_recording:
            assert len(download_pass_or_fail) == 6

        assert download_pass_or_fail["581412"] == "pass"
        assert download_pass_or_fail["581411"] == "pass"
        assert download_pass_or_fail["427716"] == "pass"
        assert download_pass_or_fail["220366"] == "pass"
        assert download_pass_or_fail["220365"] == "pass"
        assert download_pass_or_fail["196385"] == "pass"

    # Check if the files have been downloaded correctly
    if example_queryresult_fixture_name == "example_single_page_queryresult":
        # After download, we should have a new folder containing recordings in the format:
        # |- spot-winged_wood_quail
        # |---- 581412.mp3
        # |---- 581411.mp3
        # |---- 427716.mp3

        assert len(os.listdir(empty_data_folder_download_manager.data_base_path)) == 1
        assert os.listdir(empty_data_folder_download_manager.data_base_path)[0] == (
            "spot_winged_wood_quail"
        )

        bird_folder = join(
            empty_data_folder_download_manager.data_base_path, "spot_winged_wood_quail"
        )
        assert len(os.listdir(bird_folder)) == 3
        assert "581412.mp3" in os.listdir(bird_folder)
        assert "581411.mp3" in os.listdir(bird_folder)
        assert "427716.mp3" in os.listdir(bird_folder)
    if example_queryresult_fixture_name == "example_two_page_queryresult":
        # After download, we should have a new folder containing recordings in the format:
        # |- spot-winged_wood_quail
        # |---- 581412.mp3
        # |---- 581411.mp3
        # |---- 427716.mp3
        # |- little_nightjar
        # |---- 196385.mp3
        # |-----220365.mp3
        # |-----220366.mp3

        assert len(os.listdir(empty_data_folder_download_manager.data_base_path)) == 2
        assert "spot_winged_wood_quail" in os.listdir(
            empty_data_folder_download_manager.data_base_path
        )
        assert "little_nightjar" in os.listdir(
            empty_data_folder_download_manager.data_base_path
        )

        bird_folder = join(
            empty_data_folder_download_manager.data_base_path, "spot_winged_wood_quail"
        )
        assert len(os.listdir(bird_folder)) == 3
        assert "581412.mp3" in os.listdir(bird_folder)
        assert "581411.mp3" in os.listdir(bird_folder)
        assert "427716.mp3" in os.listdir(bird_folder)

        bird_folder = join(
            empty_data_folder_download_manager.data_base_path, "little_nightjar"
        )
        assert len(os.listdir(bird_folder)) == 3
        assert "220366.mp3" in os.listdir(bird_folder)
        assert "220365.mp3" in os.listdir(bird_folder)
        assert "196385.mp3" in os.listdir(bird_folder)


@pytest.mark.parametrize(
    "example_queryresult_fixture_name",
    [
        ("example_single_page_queryresult"),
        ("example_two_page_queryresult"),
    ],
)
def test_downloadmanager_detect_already_donwloaded_recordings(
    example_queryresult_fixture_name: str,
    partially_filled_data_folder_download_manager: DownloadManager,
    request: pytest.FixtureRequest,
):
    """Test the detection of already downloaded recordings for the DownloadManager.

    Parameters
    ----------
    example_queryresult_fixture_name : str
        Fixture name of the example QueryResult object based on the example XenoCanto API response.
    partially_filled_data_folder_download_manager : DownloadManager
        DownloadManager instance set to a partially-filled data folder.
    request : pytest.FixtureRequest
        Request fixture to get the example QueryResult object.
    """
    example_queryresult: QueryResult = request.getfixturevalue(
        example_queryresult_fixture_name
    )

    detected_already_downloaded_recordings = partially_filled_data_folder_download_manager._detect_already_downloaded_recordings(  # type: ignore
        example_queryresult.get_all_recordings()
    )

    # Check if the already downloaded recordings have been detected correctly
    if example_queryresult_fixture_name == "example_single_page_queryresult":
        assert len(detected_already_downloaded_recordings.keys()) == 3
        assert detected_already_downloaded_recordings["581412"] == "new"
        assert detected_already_downloaded_recordings["581411"] == "already_downloaded"
        assert detected_already_downloaded_recordings["427716"] == "new"
    elif example_queryresult_fixture_name == "example_two_page_queryresult":
        assert len(detected_already_downloaded_recordings.keys()) == 6
        assert detected_already_downloaded_recordings["581412"] == "new"
        assert detected_already_downloaded_recordings["581411"] == "already_downloaded"
        assert detected_already_downloaded_recordings["427716"] == "new"
        assert detected_already_downloaded_recordings["220366"] == "new"
        assert detected_already_downloaded_recordings["220365"] == "already_downloaded"
        assert detected_already_downloaded_recordings["196385"] == "already_downloaded"


@pytest.mark.parametrize(
    "example_queryresult_fixture_name",
    [
        ("example_single_page_queryresult"),
        ("example_two_page_queryresult"),
    ],
)
def test_downloadmanager_generate_downloaeded_recording_metadata(
    example_queryresult_fixture_name: str,
    fake_data_folder_download_manager: DownloadManager,
    request: pytest.FixtureRequest,
):
    """Test the downloaded recording metadata generation procedure for the DownloadManager
    class.

    Parameters
    ----------
    example_queryresult_fixture_name : str
        Fixture name of the example QueryResult object based on the example XenoCanto API response.
        We want to generate the downloaded recording metadata information for the recordings
        contained in the QueryResult instance.
    fake_data_folder_download_manager : DownloadManager
        A DownloadManager instance set to a non-existant path, since we won't be downloading anything.
    request : pytest.FixtureRequest
        Request fixture to get the example QueryResult object.
    """

    # Create a pass fail dict containing some passed and failed recordings
    download_pass_or_fail = {}
    if example_queryresult_fixture_name == "example_single_page_queryresult":
        download_pass_or_fail["581412"] = "pass"
        download_pass_or_fail["581411"] = "fail"
        download_pass_or_fail["427716"] = "pass"
    elif example_queryresult_fixture_name == "example_two_page_queryresult":
        download_pass_or_fail["581412"] = "pass"
        download_pass_or_fail["581411"] = "fail"
        download_pass_or_fail["427716"] = "pass"
        download_pass_or_fail["220366"] = "fail"
        download_pass_or_fail["220365"] = "pass"
        download_pass_or_fail["196385"] = "pass"

    # Generate the metadata
    example_queryresult: QueryResult = request.getfixturevalue(
        example_queryresult_fixture_name
    )
    downloaded_recording_metadata = (
        fake_data_folder_download_manager._generate_downloaded_recordings_metadata( # type: ignore
            example_queryresult.get_all_recordings(),
            download_pass_or_fail,
        )
    )

    # We only want to generate the metadata for the recordings that have indeed
    if example_queryresult_fixture_name == "example_single_page_queryresult":
        assert len(downloaded_recording_metadata) == 2
        assert downloaded_recording_metadata.loc[
            downloaded_recording_metadata["recording_id"] == 581412  # type: ignore
        ].equals(example_queryresult.result_pages[0].recordings[0].to_dataframe_row())
        assert downloaded_recording_metadata.loc[
            downloaded_recording_metadata["recording_id"] == 581411
        ].empty
        assert downloaded_recording_metadata.loc[
            downloaded_recording_metadata["recording_id"] == 427716  # type: ignore
        ].equals(
            example_queryresult.result_pages[0].recordings[2].to_dataframe_row()  # type: ignore
        )
    elif example_queryresult_fixture_name == "example_two_page_queryresult":
        assert len(downloaded_recording_metadata) == 4
        assert downloaded_recording_metadata.loc[
            downloaded_recording_metadata["recording_id"] == 581412  # type: ignore
        ].equals(example_queryresult.result_pages[0].recordings[0].to_dataframe_row())
        assert downloaded_recording_metadata.loc[
            downloaded_recording_metadata["recording_id"] == 581411
        ].empty
        assert downloaded_recording_metadata.loc[
            downloaded_recording_metadata["recording_id"] == 427716  # type: ignore
        ].equals(example_queryresult.result_pages[0].recordings[2].to_dataframe_row())
        assert downloaded_recording_metadata.loc[
            downloaded_recording_metadata["recording_id"] == 220366
        ].empty
        assert downloaded_recording_metadata.loc[
            downloaded_recording_metadata["recording_id"] == 220365  # type: ignore
        ].equals(example_queryresult.result_pages[1].recordings[1].to_dataframe_row())
        assert downloaded_recording_metadata.loc[
            downloaded_recording_metadata["recording_id"] == 196385  # type: ignore
        ].equals(example_queryresult.result_pages[1].recordings[2].to_dataframe_row())


@pytest.mark.parametrize(
    "metadata_to_add_fixture_name",
    [
        ("spot_winged_wood_quail_to_add_test_recording_metadata"),
        ("little_nightjar_to_add_test_recording_metadata"),
        ("combined_to_add_test_recording_metadata"),
    ],
)
def test_downloadmanager_update_animal_recordings_metadata_files(
    partially_filled_data_folder_download_manager: DownloadManager,
    metadata_to_add_fixture_name: str,
    request: pytest.FixtureRequest,
    spot_winged_wood_quail_partial_test_recording_metadata: pd.DataFrame,
    spot_winged_wood_quail_full_test_recording_metadata: pd.DataFrame,
    little_nightjar_partial_test_recording_metadata: pd.DataFrame,
    little_nightjar_full_test_recording_metadata: pd.DataFrame,
):
    to_add_test_recording_metadata: pd.DataFrame = request.getfixturevalue(
        metadata_to_add_fixture_name
    )

    partially_filled_data_folder_download_manager._update_animal_recordings_metadata_files( # type: ignore
        to_add_test_recording_metadata
    )

    if (
        metadata_to_add_fixture_name
        == "spot_winged_wood_quail_to_add_test_recording_metadata"
    ):
        assert spot_winged_wood_quail_full_test_recording_metadata.equals(  # type: ignore
            pd.read_csv(  # type: ignore
                join(
                    partially_filled_data_folder_download_manager.data_base_path,
                    "spot_winged_wood_quail",
                    "spot_winged_wood_quail_recording_metadata.csv",
                )
            )
        )
        assert little_nightjar_partial_test_recording_metadata.equals(  # type: ignore
            pd.read_csv(  # type: ignore
                join(
                    partially_filled_data_folder_download_manager.data_base_path,
                    "little_nightjar",
                    "little_nightjar_recording_metadata.csv",
                )
            )
        )
    elif (
        metadata_to_add_fixture_name == "little_nightjar_to_add_test_recording_metadata"
    ):
        test = pd.read_csv(  # type: ignore
            join(
                partially_filled_data_folder_download_manager.data_base_path,
                "spot_winged_wood_quail",
                "spot_winged_wood_quail_recording_metadata.csv",
            )
        )
        assert spot_winged_wood_quail_partial_test_recording_metadata.equals(  # type: ignore
            pd.read_csv(  # type: ignore
                join(
                    partially_filled_data_folder_download_manager.data_base_path,
                    "spot_winged_wood_quail",
                    "spot_winged_wood_quail_recording_metadata.csv",
                )
            )
        )
        assert little_nightjar_full_test_recording_metadata.equals(  # type: ignore
            pd.read_csv(  # type: ignore
                join(
                    partially_filled_data_folder_download_manager.data_base_path,
                    "little_nightjar",
                    "little_nightjar_recording_metadata.csv",
                )
            )
        )
    elif metadata_to_add_fixture_name == "combined_to_add_test_recording_metadata":
        assert spot_winged_wood_quail_full_test_recording_metadata.equals(  # type: ignore
            pd.read_csv(  # type: ignore
                join(
                    partially_filled_data_folder_download_manager.data_base_path,
                    "spot_winged_wood_quail",
                    "spot_winged_wood_quail_recording_metadata.csv",
                )
            )
        )
        assert little_nightjar_full_test_recording_metadata.equals(  # type: ignore
            pd.read_csv(  # type: ignore
                join(
                    partially_filled_data_folder_download_manager.data_base_path,
                    "little_nightjar",
                    "little_nightjar_recording_metadata.csv",
                )
            )
        )


def test_downloadmanager_generate_animal_folder_name(
    fake_data_folder_download_manager: DownloadManager,
):
    """Test the generation functionality of the animal folder name in the DownloadManager.

    Parameters
    ----------
    fake_data_folder_download_manager : DownloadManager
        DownloadManager instance set to a non-existant path, since we won't be downloading anything.
    """
    # Spaces should be replaced by "_"
    assert (
        fake_data_folder_download_manager._generate_animal_folder_name( # type: ignore
            "test with just spaces"
        )
        == "test_with_just_spaces"
    )

    # Everything should be lower case
    assert (
        fake_data_folder_download_manager._generate_animal_folder_name( # type: ignore
            "tEst CAPITAL Bird name"
        )
        == "test_capital_bird_name"
    )

    # Special chars
    assert (
        fake_data_folder_download_manager._generate_animal_folder_name( # type: ignore
            "black-winged bird"
        )
        == "black_winged_bird"
    )
