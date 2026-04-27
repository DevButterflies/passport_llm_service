from typing import Optional
import re
from pydantic import BaseModel, ValidationInfo,field_validator
from datetime import datetime


# ICAO Standards: Only Latin A-Z, 0-9, and filler characters allowed in MRZ
# For visual zones, we allow spaces, hyphens, and apostrophes.
LATIN_STRICT_PATTERN = re.compile(r"^[A-Z0-9\s\-\']+$")
ISO_3166_1_ALPHA_3 = re.compile(r"^[A-Z]{3}$")  # Country codes are always 3 letters (TUN, FRA, etc.)

class PassportCardResponse(BaseModel):
    country_code: Optional[str]
    passport_number: Optional[str]
    date_of_birth: Optional[str]      # Expected: YYYY-MM-DD
    expiration_date: Optional[str]    # Expected: YYYY-MM-DD
    nationality: Optional[str]
    sex: Optional[str]                # M, F, or X (<)
    given_names: Optional[str]
    surname: Optional[str]
    personal_number: Optional[str]

    @field_validator('country_code', 'nationality')
    @classmethod
    def validate_icao_codes(cls, v: str):
        try:
            if not v or v.upper() == "UNKNOWN":
                return "UNKNOWN"
            
            v = v.upper().strip()
            # If LLM returns "TUNISIAN" or "TUNISIE", extract "TUN"
            if "TUN" in v: return "TUN"
            if "FRA" in v: return "FRA"
            if "USA" in v: return "USA"
            if "CAN" in v: return "CAN"
            
            # If it's just a long string, take the first 3
            if len(v) > 3:
                v = v[:3]
                
            if ISO_3166_1_ALPHA_3.fullmatch(v):
                return v
            return "invalid extraction"
        except Exception:
            return "invalid extraction"

    @field_validator('date_of_birth', 'expiration_date')
    @classmethod
    def validate_dates(cls, v: str, info: ValidationInfo):
        if not v or v.upper() == "UNKNOWN":
            return "UNKNOWN"
        
        v = v.strip()
        # List of formats the LLM might hallucinate
        formats_to_try = [
            "%Y-%m-%d", # Correct: 1998-02-14
            "%d-%m-%Y", # What you just got: 14-02-1998
            "%d/%m/%Y", # 14/02/1998
            "%Y/%m/%d", # 1998/02/14
            "%y%m%d"    # MRZ style: 980214
        ]

        for fmt in formats_to_try:
            try:
                dt = datetime.strptime(v, fmt)
                # If it's MRZ style (YYMMDD), handle the century
                if fmt == "%y%m%d":
                    if info.field_name == 'date_of_birth':
                        year = dt.year if dt.year <= datetime.now().year else dt.year - 100
                        return dt.replace(year=year).strftime("%Y-%m-%d")
                return dt.strftime("%Y-%m-%d")
            except (ValueError, TypeError):
                continue
        
        return "invalid extraction"

    @field_validator('personal_number')
    @classmethod
    def validate_tunisian_id(cls, v: str, info: ValidationInfo):
        try:
            if not v or v.upper() == "UNKNOWN":
                return "UNKNOWN"

            # Check if we are dealing with a Tunisian document
            country = getattr(info.data, 'country_code', "")
            if country == "TUN":
                digits_only = re.sub(r'\D', '', v)
                if len(digits_only) == 8:
                    return digits_only
                # If it's 7 digits, it might be an old CIN, pad with 0
                if len(digits_only) == 7:
                    return f"0{digits_only}"
                
            # For other cases, just alphanumeric cleaning
            cleaned = re.sub(r'[^A-Z0-9]', '', v.upper())
            return cleaned if cleaned else "invalid extraction"
        except Exception:
            return "invalid extraction"

    @field_validator('passport_number')
    @classmethod
    def validate_passport_no(cls, v: str):
        try:
            if not v or v.upper() == "UNKNOWN":
                return "UNKNOWN"
            cleaned = re.sub(r'[^A-Z0-9]', '', v.upper())
            return cleaned if cleaned else "invalid extraction"
        except Exception:
            return "invalid extraction"

    @field_validator('sex')
    @classmethod
    def validate_sex(cls, v: str):
        try:
            if not v or v.upper() == "UNKNOWN":
                return "UNKNOWN"
            v = v.upper().strip()
            if "M" in v or "H" in v: return "M"
            if "F" in v or "W" in v: return "F"
            return "X"
        except Exception:
            return "invalid extraction"


