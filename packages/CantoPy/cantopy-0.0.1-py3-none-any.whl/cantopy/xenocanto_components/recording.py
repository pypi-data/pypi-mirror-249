from datetime import timedelta, datetime
from typing import Dict

import pandas as pd
from pandas import Timestamp


class Recording:
    """
    Wrapper for storing a single recording returned by the Xeno Canto API.

    Attributes
    ----------
    recording_id : int
        The recording id number of the recording on xeno-canto.
    generic_name : str
        Generic name of the species.
    specific_name : str
        Specific name (epithet) of the species.
    subspecies_name : str
        Subspecies name (subspecific epithet).
    species_group : str
        Group to which the species belongs (birds, grasshoppers, bats).
    english_name : str
        English name of the species.
    recordist_name : str
        Name of the recordist.
    country : str
        Country where the recording was made.
    locality_name : str
        Name of the locality.
    latitude : float
        Latitude of the recording in decimal coordinates.
    longitude : float
        Longitude of the recording in decimal coordinates.
    sound_type : str
        Sound type of the recording (combining both predefined terms such as 'call' or 'song'
        and additional free text options).
    sex : str
        Sex of the animal.
    life_stage : str
        Life stage of the animal (adult, juvenile, etc.).
    recording_method : str
        Recording method (field recording, in the hand, etc.).
    recording_url : str
        URL specifying the details of this recording.
    audio_file_url : str
        URL to the audio file.
    license_url : str
        URL describing the license of this recording.
    quality_rating : str
        Current quality rating for the recording.
    recording_length : timedelta
        Length of the recording in a timedelta.
    recording_timestamp : datetime
        Timestamp that the recording was made.
    upload_timestamp : datetime
        Date that the recording was uploaded to xeno-canto.
    background_species : list
        An array with the identified background species in the recording.
    recordist_remarks : str
        Additional remarks by the recordist.
    animal_seen : str
        Was the recorded animal seen?
    playback_used : str
        Was playback used to lure the animal?
    temperature : str
        Temperature during recording (applicable to specific groups only).

    automatic_recording : str
        Automatic (non-supervised) recording?
    recording_device : str
        Recording device used.
    microphone_used : str
        Microphone used.
    sample_rate : int
        Sample rate.

    Notes
    -----
    Currently, the recording class does not capture the following information also returned by the
    XenoCanto API:
    - file-name : Original file name of the audio file.
    - sono : An object with the URLs to the four versions of sonograms.
    - osci : An object with the URLs to the three versions of oscillograms.
    - regnr : Registration number of the specimen (when collected).

    """

    def __init__(self, recording_data: Dict[str, str]):
        """Create a Recording object with a given recording dict returned from the XenoCanto API

        Parameters
        ----------
        recording_data : Dict[str, str]
            The dict of the recording returned by the XenoCanto API
        """
        # Extract the recording length from the given string representation
        length_in_minutes = recording_data["length"].split(":")
        recording_length = timedelta(
            minutes=int(length_in_minutes[0]), seconds=int(length_in_minutes[1])
        )

        # Extract the full timestamp from the given string representation
        recording_date = recording_data["date"]
        recording_time = recording_data["time"]
        recording_timestamp = (
            Timestamp(f"{recording_date}T{recording_time}")
            if recording_time != "?"  # If time is not set
            else Timestamp(recording_date)
        )

        # Extract the uploaded timestamp
        uploaded_timestamp = datetime.fromisoformat(recording_data["uploaded"])

        ####################################################################
        # Set the Recording object attributes
        ####################################################################

        # Id
        self.recording_id = int(recording_data["id"])

        # Animal information
        self.generic_name = recording_data["gen"]
        self.specific_name = recording_data["sp"]
        self.subspecies_name = recording_data["ssp"]
        self.species_group = recording_data["group"]
        self.english_name = recording_data["en"]
        self.sound_type = recording_data["type"]
        self.sex = recording_data["sex"]
        self.life_stage = recording_data["stage"]
        self.background_species = recording_data["also"]
        self.animal_seen = recording_data["animal-seen"]

        # Recording information
        self.recordist_name = recording_data["rec"]
        self.recording_method = recording_data["method"]
        self.license_url = recording_data["lic"]
        self.quality_rating = recording_data["q"]
        self.recording_length = recording_length
        self.recording_timestamp = recording_timestamp
        self.date = recording_data["date"]
        self.upload_timestamp = uploaded_timestamp
        self.recording_url = recording_data["url"]
        self.audio_file_url = recording_data["file"]
        self.recordist_remarks = recording_data["rmk"]
        self.playback_used = recording_data["playback-used"]
        self.automatic_recording = recording_data["auto"]
        self.recording_device = recording_data["dvc"]
        self.microphone_used = recording_data["mic"]
        self.sample_rate = int(recording_data["smp"])

        # Location information
        self.country = recording_data["cnt"]
        self.locality_name = recording_data["loc"]
        self.latitude = float(recording_data["lat"]) if recording_data["lat"] else None
        self.longitude = float(recording_data["lng"]) if recording_data["lng"] else None
        self.temperature = recording_data["temp"]

    def to_dataframe_row(self) -> pd.DataFrame:
        """Convert the Recording object to a pandas DataFrame row.

        Returns
        -------
        pd.DataFrame
            A pandas DataFrame row containing the recording information.
        """

        data = {
            "recording_id": [self.recording_id],
            "generic_name": [self.generic_name],
            "specific_name": [self.specific_name],
            "subspecies_name": [self.subspecies_name],
            "species_group": [self.species_group],
            "english_name": [self.english_name],
            "sound_type": [self.sound_type],
            "sex": [self.sex],
            "life_stage": [self.life_stage],
            "background_species": [self.background_species],
            "animal_seen": [self.animal_seen],
            "recordist_name": [self.recordist_name],
            "recording_method": [self.recording_method],
            "license_url": [self.license_url],
            "quality_rating": [self.quality_rating],
            "recording_length": [self.recording_length],
            "recording_timestamp": [self.recording_timestamp],
            "date": [self.date],
            "upload_timestamp": [self.upload_timestamp],
            "recording_url": [self.recording_url],
            "audio_file_url": [self.audio_file_url],
            "recordist_remarks": [self.recordist_remarks],
            "playback_used": [self.playback_used],
            "automatic_recording": [self.automatic_recording],
            "recording_device": [self.recording_device],
            "microphone_used": [self.microphone_used],
            "sample_rate": [self.sample_rate],
            "country": [self.country],
            "locality_name": [self.locality_name],
            "latitude": [self.latitude],
            "longitude": [self.longitude],
            "temperature": [self.temperature],
        }

        return pd.DataFrame(data)
