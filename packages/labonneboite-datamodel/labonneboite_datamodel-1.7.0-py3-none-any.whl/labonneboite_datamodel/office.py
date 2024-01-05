from sqlmodel import Field
from typing import Optional
from .base import BaseMixin
from pydantic import field_validator
from sqlalchemy import UniqueConstraint
from .validators import valid_is_naf


# validators
class OfficeCommon(BaseMixin):
    """This is the base model applied to all Office tables

    Attributes:
        id: This is the primary key for the table
        siret: This is the company SIRET number

    """

    __table_args__ = (UniqueConstraint("siret"),)

    #: docs for baz
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)

    siret: Optional[str] = Field(default=None, nullable=False)

    @field_validator("siret", mode="before")
    @classmethod
    def is_siret(cls, v):
        """Validator for `siret`

        Rules:
            - a SIRET should be made up of 14 numbers

        Raises:
            ValueError:


        """
        v = v.zfill(14)

        if not v.isdigit():
            raise ValueError("a SIRET should be made up of 14 numbers")
        return v


class Office(OfficeCommon, table=True):
    """
    Attributes:
        naf: NAF identifier to determine in which field the company works in.
        company_name: Name of the main company.
        office_name: Name of the branch company.
        streetnumber: Street number of the company. (Optional)
        street: Street name of the company. (Optional)
        postcode: Postal code of the city where the company is, this may not be unique in France. (Optional)
        citycode: INSEE code of the city where the company is, this may is unique in France. (Optional)
        email: Email of the branch company. (Optional)
        phone: Phone of the branch company. (Optional)
        website: Website of the branch / main company. (Optional)
        headcount_range: Number of employees in the branch company. (Optional)
        flag_pmsmp: To be removed (Optional)
        flag_poe_afpr: To be removed (Optional)
        flag_junior: To be removed (Optional)
        flag_senior: To be removed (Optional)
        flag_handicap: To be removed (Optional)
    """

    naf: str
    company_name: str
    office_name: str
    streetnumber: str = Field(default="", nullable=True)
    street: str = Field(default="", nullable=True)
    postcode: str = Field(default="", nullable=True)
    citycode: str = Field(default="", nullable=True)
    email: str = Field(default="", nullable=True)
    phone: str = Field(default="", nullable=True)
    website: str = Field(default="", nullable=True)

    headcount_range: str = ""

    flag_pmsmp: bool = False
    flag_poe_afpr: bool = False
    flag_junior: bool = False
    flag_senior: bool = False
    flag_handicap: bool = False

    @field_validator("naf", mode="before")
    @classmethod
    def is_naf(cls, v):
        return valid_is_naf(v)

    @field_validator("streetnumber", mode="before")
    @classmethod
    def is_streetnumber(cls, v):
        """Validator for `streetnumber`

        Rules:
            - accept string inputs
        """

        if isinstance(v, int):
            return str(v)

        return v

    @field_validator(
        "flag_pmsmp",
        "flag_poe_afpr",
        "flag_junior",
        "flag_senior",
        "flag_handicap",
        mode="before",
    )
    @classmethod
    def check_flag_poe_afpr(cls, v):
        """Validator for `flag_poe_afpr`

        Rules:
            - returns False if value is NULL or empty string

        """
        if isinstance(v, str) and v in ["NULL", ""]:
            return False
        return v

    @field_validator("headcount_range", mode="before")
    @classmethod
    def headcount_range_cleanup(cls, v):
        """Validator for `headcount_range`

        Rules:
            - the value should be a range with positive values

        """

        # the value should be a range with positive values
        values = v.split("-")

        if len(values) < 2:
            return ""

        mini = int(values[0])
        maxi = int(values[1])

        if maxi > mini:
            return f"{mini}-{maxi}"

        return ""

    @field_validator("phone", mode="before")
    @classmethod
    def phone_cleanup(cls, v):
        """Validator for `phone`

        Rules:
            - Phone number is not in the expected format: either 9 or 10 numbers

        Raises:
            ValueError: Phone number is not in the expected format: either 9 or 10 numbers
        """
        if not v:
            return ""

        if len(v) < 9:
            raise ValueError(
                "Phone number is not in the expected format: either 9 or 10 numbers"
            )
        return v.zfill(10)

    @field_validator("postcode", mode="before")
    @classmethod
    def is_postcode(cls, v):
        """Validator for `postcode`

        Rules:
            - should be made up of at least 5 numbers
            - a postcode cannot be 00000

        Raises:
            ValueError:

        """
        if not v:
            return ""

        if len(v) < 5:
            raise ValueError("a postcode should be made up of at least 5 numbers")

        if int(v) == 0:
            raise ValueError("a postcode cannot be 00000")
        return v

    @field_validator("citycode", mode="before")
    @classmethod
    def is_citycode(cls, v):
        """Validator for `citycode`

        Rules:
            - should be made up of at least 5 numbers
            - a citycode cannot be 00000

        Raises:
            ValueError:

        """
        if not v:
            return ""

        if len(v) < 5:
            raise ValueError("a citycode should be made up of 4 numbers and a letter")

        if v == "0".zfill(5):
            raise ValueError("a citycode cannot be 00000")
        return v


class OfficeScore(OfficeCommon, table=True):
    """This table stores the current score for each siret

    Attributes:
        score: Score provided by the ADS algorithm monthly
    """

    score: float = 0


class OfficeMetadata(OfficeCommon, table=True):
    """This table stores the office metadata information not part of ADS core data

    Attributes:
        subscribed: Score provided by the ADS algorithm monthly
        hide_phone:
        hide_adress:
    """

    subscribed: bool = Field(default=True)
    hide_phone: bool = Field(default=False)
    hide_location: bool = Field(default=False)


class OfficeGps(OfficeCommon, table=True):
    """
    This is only for gps information

    Attributes:
        department_number: Department number (75, 47, etc.) where the company is.
        department: Department name where the company is.
        city:
        region:
        region_number:
        latitude:
        longitude:
    """

    department_number: str
    department: str
    city: str
    region: str
    region_number: int
    latitude: float
    longitude: float
