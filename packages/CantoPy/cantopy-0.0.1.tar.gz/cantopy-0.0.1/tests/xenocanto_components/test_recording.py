from src.cantopy.xenocanto_components import Recording


def test_recording_init(example_recording_1_from_example_xenocanto_query_response_page_1: Recording):
    """Test for the initialization of a Recording object.

    Parameters
    ----------
    example_recording_1_from_example_xenocanto_query_response_page_1 : Recording
        A Recording object based on the first recording in the example page 1 XenoCanto 
        API query response.
    """

    # See if all recording fields are captured
    assert example_recording_1_from_example_xenocanto_query_response_page_1.recording_id == 581412
    assert example_recording_1_from_example_xenocanto_query_response_page_1.generic_name == "Odontophorus"
    assert example_recording_1_from_example_xenocanto_query_response_page_1.specific_name == "capueira"
    assert example_recording_1_from_example_xenocanto_query_response_page_1.subspecies_name == "plumbeicollis"
    assert example_recording_1_from_example_xenocanto_query_response_page_1.species_group == "birds"
    assert example_recording_1_from_example_xenocanto_query_response_page_1.english_name == "Spot-winged Wood Quail"
    assert example_recording_1_from_example_xenocanto_query_response_page_1.recordist_name == "Ciro Albano"
    assert example_recording_1_from_example_xenocanto_query_response_page_1.country == "Brazil"
    assert example_recording_1_from_example_xenocanto_query_response_page_1.locality_name == "RPPN Serra Bonita, Camacan-BA, Bahia"
    assert example_recording_1_from_example_xenocanto_query_response_page_1.latitude == -15.3915
    assert example_recording_1_from_example_xenocanto_query_response_page_1.longitude == -39.5643
    assert example_recording_1_from_example_xenocanto_query_response_page_1.sound_type == "duet, song"
    assert example_recording_1_from_example_xenocanto_query_response_page_1.sex == "female, male"
    assert example_recording_1_from_example_xenocanto_query_response_page_1.life_stage == "adult"
    assert example_recording_1_from_example_xenocanto_query_response_page_1.recording_method == "field recording"
    assert example_recording_1_from_example_xenocanto_query_response_page_1.recording_url == "//xeno-canto.org/581412"
    assert example_recording_1_from_example_xenocanto_query_response_page_1.audio_file_url == "https://xeno-canto.org/581412/download"
    assert (
        example_recording_1_from_example_xenocanto_query_response_page_1.license_url == "//creativecommons.org/licenses/by-nc-sa/4.0/"
    )
    assert example_recording_1_from_example_xenocanto_query_response_page_1.quality_rating == "A"
    assert example_recording_1_from_example_xenocanto_query_response_page_1.recording_length.seconds == 194
    assert (
        example_recording_1_from_example_xenocanto_query_response_page_1.recording_timestamp.strftime("%Y-%m-%d %X")
        == "2020-08-02 08:00:00"
    )
    assert example_recording_1_from_example_xenocanto_query_response_page_1.upload_timestamp.strftime("%Y-%m-%d") == "2020-08-09"
    assert example_recording_1_from_example_xenocanto_query_response_page_1.background_species == ["Sclerurus scansor"]
    assert example_recording_1_from_example_xenocanto_query_response_page_1.recordist_remarks == ""
    assert example_recording_1_from_example_xenocanto_query_response_page_1.animal_seen == "yes"
    assert example_recording_1_from_example_xenocanto_query_response_page_1.playback_used == "yes"
    assert example_recording_1_from_example_xenocanto_query_response_page_1.automatic_recording == "no"
    assert example_recording_1_from_example_xenocanto_query_response_page_1.recording_device == ""
    assert example_recording_1_from_example_xenocanto_query_response_page_1.microphone_used == ""
    assert example_recording_1_from_example_xenocanto_query_response_page_1.sample_rate == 48000


def test_to_dataframe_row(example_recording_1_from_example_xenocanto_query_response_page_1: Recording):
    """Test the conversion of a Recording object to a pandas DataFrame row.

    Parameters
    ----------
    example_recording_1_from_example_xenocanto_query_response_page_1 : Recording
        A Recording object based on the first recording in the example page 1 XenoCanto 
        API query response.
    """

    # Build the recording dataframe row
    example_recording_df_row = example_recording_1_from_example_xenocanto_query_response_page_1.to_dataframe_row()

    # test if the dataframe row contains the correct information
    assert example_recording_df_row["recording_id"][0] == 581412
    assert example_recording_df_row["generic_name"][0] == "Odontophorus"
    assert example_recording_df_row["specific_name"][0] == "capueira"
    assert example_recording_df_row["subspecies_name"][0] == "plumbeicollis"
    assert example_recording_df_row["species_group"][0] == "birds"
    assert example_recording_df_row["english_name"][0] == "Spot-winged Wood Quail"
    assert example_recording_df_row["recordist_name"][0] == "Ciro Albano"
    assert example_recording_df_row["country"][0] == "Brazil"
    assert (
        example_recording_df_row["locality_name"][0]
        == "RPPN Serra Bonita, Camacan-BA, Bahia"
    )
    assert example_recording_df_row["latitude"][0] == -15.3915
    assert example_recording_df_row["longitude"][0] == -39.5643
    assert example_recording_df_row["sound_type"][0] == "duet, song"
    assert example_recording_df_row["sex"][0] == "female, male"
    assert example_recording_df_row["life_stage"][0] == "adult"
    assert example_recording_df_row["recording_method"][0] == "field recording"
    assert example_recording_df_row["recording_url"][0] == "//xeno-canto.org/581412"
    assert (
        example_recording_df_row["audio_file_url"][0]
        == "https://xeno-canto.org/581412/download"
    )
    assert (
        example_recording_df_row["license_url"][0]
        == "//creativecommons.org/licenses/by-nc-sa/4.0/"
    )
    assert example_recording_df_row["quality_rating"][0] == "A"
    assert example_recording_df_row["recording_length"][0].seconds == 194  # type: ignore
    assert example_recording_df_row["recording_timestamp"][0].strftime("%Y-%m-%d %X") == "2020-08-02 08:00:00"  # type: ignore
    assert example_recording_df_row["upload_timestamp"][0].strftime("%Y-%m-%d") == "2020-08-09"  # type: ignore
    assert example_recording_df_row["background_species"][0] == ["Sclerurus scansor"]
    assert example_recording_df_row["recordist_remarks"][0] == ""
    assert example_recording_df_row["animal_seen"][0] == "yes"
    assert example_recording_df_row["playback_used"][0] == "yes"
    assert example_recording_df_row["automatic_recording"][0] == "no"
    assert example_recording_df_row["recording_device"][0] == ""
    assert example_recording_df_row["microphone_used"][0] == ""
    assert example_recording_df_row["sample_rate"][0] == 48000
