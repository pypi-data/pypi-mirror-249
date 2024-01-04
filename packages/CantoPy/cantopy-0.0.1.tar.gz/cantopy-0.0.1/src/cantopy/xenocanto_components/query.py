# Additional information on the Xeno Canto API can be found at:
# https://www.xeno-canto.org/explore/api


class Query:
    """Wrapper for a query that is passed to the Xeno Canto API

    Attributes
    ----------
    name : str
        The name to of the species, can be either the English name, the scientific name, or the scientific name of the family.
    grp : str
        The group of the recording.
    gen : str
        The genus name of the species.
    ssp : str
        The subspecies.
    rec : str
        The id of the person who uploaded the recording.
    cnt : str
        The country of the recording.
    loc : str
        The location of the recording.
    rmk : str
        Additional remarks for the recording.
    seen : str
        If the animal was seen.
    playback : str
        The playback used attribute to set.
    lat : str
        The latitude of the recording.
    lon : str
        The longitude of the recording.
    box : str
        The coordinate box which should contain the recording location.
    also : str
        The also attribute is used to search for background species in a recording.
    song_type : str
        The type of song in the recording.
    othertype : str
        The other type attribute is used when the type field does not contain the desired sound type.
    sex : str
        The sex of the species.
    stage : str
        The life stage attribute to set, valid values are: "adult", "juvenile", "nestling", "nymph", and "subadult".
        This field always uses a 'matches' operator.
    method : str
        The recording method of the recording.
    nr : str
        The catalog number of recording to search for a specific recording.
    file_license : str
        The recording license.
    q : str
        The quality of the recording.
    length : str
        The length of the recording
    area : str
        The general world area of the recording.
    since : str
        Search for recordings UPLOADED after a certain date.
    year : str
        Search for recordings RECORDED in a certain year.
    month : str
        Search for recordings RECORDED in a certain month.
    smp : str
        The sample rate of the recording.
    """

    def __init__(
        self,
        name: str,
        grp: str = "None",
        gen: str = "None",
        ssp: str = "None",
        rec: str = "None",
        cnt: str = "None",
        loc: str = "None",
        rmk: str = "None",
        seen: str = "None",
        playback: str = "None",
        lat: str = "None",
        lon: str = "None",
        box: str = "None",
        also: str = "None",
        song_type: str = "None",
        othertype: str = "None",
        sex: str = "None",
        stage: str = "None",
        method: str = "None",
        nr: str = "None",
        file_license: str = "None",
        q: str = "None",
        length: str = "None",
        area: str = "None",
        since: str = "None",
        year: str = "None",
        month: str = "None",
        smp: str = "None",
    ):
        """Init the query object for passing to the Xeno Canto API.

        Parameters
        ----------
        name : str
            the name to set, can be either the English name, the scientific name, or the scientific name of the family
        grp : str, optional
            the group to set, valid values are: 'birds', 'grashoppers', or 'bats'.
            This can also be set using their respective ids: '1', '2', and '3'. Recordings may include multiple groups,
            use 'soundscape' or '0' to include all groups.
        gen : str, optional
            the genus name to set, field uses a 'starts with' rather than 'contains' query and accepts a 'matches' operator
        ssp : str, optional
            the subspecies to set, field uses a 'starts with' rather than 'contains' query and accepts a 'matches' operator
        rec : str, optional
            the recordist to set, field accepts a 'matches' operator
        cnt : str, optional
            the country to set, field uses a 'starts with' query and accepts a 'matches' operator
        loc : str, optional
            the location to set, field accepts a 'matches' operator
        rmk : str, optional
            the remarks to set, field accepts a 'matches' operator
        seen : str, optional
            the animal seen attribute to set
        playback : str, optional
            the playback used attribute to set
        lat : str, optional
            the latitude to set, used in conjunction with the lon field to search within one degree of a location.
            This field also accepts '<' and '>' operators
        lon : str, optional
            the longitude to set, used in conjunction with the lat field to search within one degree of a location.
            This field also accepts '<' and '>' operators
        box : str, optional
            the coordinate box to set, this box is formatted as follows: LAT_MIN,LON_MIN,LAT_MAX,LON_MAX.
            This field also accepts '<' and '>' operators
        also : str, optional
            the also attribute to set, the also attribute is used to search for background species in a recording
        song_type : str, optional
            the type attribute to set, valid values for this tag are: "aberrant", "alarm call", "begging call", "call",
            "calling song", "courtship song", "dawn song", "distress call", "disturbance song", "drumming", "duet",
            "echolocation", "female song", "flight call", "flight song", "imitation", "nocturnal flight call",
            "rivalry song", "searching song", "social call", "song", "subsong". This field always uses a 'matches' operator
        othertype : str, optional
            the other type attribute to set, this field is used when the type field does not contain the desired sound type
            e.g. "wing flapping"
        sex : str, optional
            the sex attribute to set, valid values are: "male" and "female". This field always uses a 'matches' operator
        stage : str, optional
            the life stage attribute to set, valid values are: "adult", "juvenile", "nestling", "nymph", and "subadult".
            This field always uses a 'matches' operator
        method : str, optional
            the recording method attribute to set, valid values are: "emerging from roost", "field recording",
            "fluorescent light tag", "hand-release", "in enclosure", "in net", "in the hand", "roosting", "roped",
            "studio recording". This field always uses a 'matches' operator
        nr : str, optional
            the catalog number of recordings attribute to set, this field is used to search for a specific recording.
            It can also be used to search for a range of recordings e.g. 1-10
        file_license : str, optional
            the recording license attribute to set, valid values are: "BY" (Attribution), "NC" (NonCommercial), "SA"
            (ShareAlike), "ND" (NoDerivatives), "CC0" (Public Domain/copyright-free) and "PD" (no restrictions (=BY-NC-SA)).
            Conditions can be combined e.g. "BY-NC-SA". This field always uses a 'matches' operator
        q : str, optional
            the quality attribute to set, valid values range from "A" (best) to "E" (worst). This field accepts "<" and ">" operators
        length : str, optional
            the recording length attribute to set, this field accepts "<", ">" and "=" operators
        area : str, optional
            the area attribute to set, valid values are: "africa", "america", "asia", "australia", "europe"
        since : str, optional
            the since attribute to set, this field is used to search for recordings UPLOADED after a certain date,
            date format is YYYY-MM-DD
        year : str, optional
            the year attribute to set, this field is used to search for recordings RECORDED in a certain year,
            date format is YYYY, this field accepts "<" and ">" operators
        month : str, optional
            the month attribute to set, this field is used to search for recordings RECORDED in a certain month,
            date format is MM, this field accepts "<" and ">" operators
        smp : str, optional
            the sample rate attribute to set, this field accepts "<" and ">" operators
        """

        self.name = name
        self.grp = grp
        self.gen = gen
        self.ssp = ssp
        self.rec = rec
        self.cnt = cnt
        self.loc = loc
        self.rmk = rmk
        self.seen = seen
        self.playback = playback
        self.lat = lat
        self.lon = lon
        self.box = box
        self.also = also
        self.song_type = song_type
        self.othertype = othertype
        self.sex = sex
        self.stage = stage
        self.method = method
        self.nr = nr
        self.file_license = file_license
        self.q = q
        self.length = length
        self.area = area
        self.since = since
        self.year = year
        self.month = month
        self.smp = smp

    def to_string(self) -> str:
        """Generate a string representation of the Query object for passing to the Xeno Canto API

        Returns
        -------
        str
            The string representation of the Query object
        """

        attributes = [
            f"{self.name}",  # name does not have a tag in the API
            f'grp:"{self.grp}"',
            f'gen:"{self.gen}"',
            f'ssp:"{self.ssp}"',
            f'rec:"{self.rec}"',
            f'cnt:"{self.cnt}"',
            f'loc:"{self.loc}"',
            f'rmk:"{self.rmk}"',
            f'seen:"{self.seen}"',
            f'playback:"{self.playback}"',
            f'lat:"{self.lat}"',
            f'lon:"{self.lon}"',
            f'box:"{self.box}"',
            f'also:"{self.also}"',
            f'type:"{self.song_type}"',
            f'othertype:"{self.othertype}"',
            f'sex:"{self.sex}"',
            f'stage:"{self.stage}"',
            f'method:"{self.method}"',
            f'nr:"{self.nr}"',
            f'license:"{self.file_license}"',
            f'q:"{self.q}"',
            f'length:"{self.length}"',
            f'area:"{self.area}"',
            f'since:"{self.since}"',
            f'year:"{self.year}"',
            f'month:"{self.month}"',
            f'smp:"{self.smp}"',
        ]

        # Remove the None values
        attributes = [attribute for attribute in attributes if "None" not in attribute]

        return "+".join(filter(None, attributes))
