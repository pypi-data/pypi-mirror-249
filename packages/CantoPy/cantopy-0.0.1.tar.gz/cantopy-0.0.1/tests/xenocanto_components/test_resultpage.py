from src.cantopy.xenocanto_components import ResultPage

def test_resultpage_init(example_result_page_page_1: ResultPage):
    """Test for the initialisation of a ResultPage object.

    Parameters
    ----------
    example_result_page_page_1 : ResultPage
        The ResultPage object created from the example page 1 XenoCanto API query response
    """

    # Test page attribute
    assert example_result_page_page_1.page_id == 1

    # Just check if recording is also set,
    # but more detailed recording evaluation is in the Recording test section
    assert len(example_result_page_page_1.recordings) == 3
    assert example_result_page_page_1.recordings[0].recording_id == 581412
