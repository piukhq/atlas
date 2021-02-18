from typing import Tuple


def fatface_card_number(publisher_list: list) -> Tuple[str, str]:
    """Mapping function to extract card number from the response"""
    return "card_number", publisher_list[0]["message"].split(":")[0]


SLUG_TO_CREDENTIAL_MAP = {
    "harvey-nichols": {
        "forename": "first_name",
        "surname": "last_name",
        "customerNumber": "card_number",
        "phone": "phone_number",
    },
    "iceland-bonus-card": {
        "town_city": "city",
        "phone1": "phone_number",
        "dob": "date_of_birth"
    },
    "fatface": {
        "surname": "last_name",
        "publisher": fatface_card_number,
    },
    "wasabi-club": {
        "FirstName": "first_name",
        "LastName": "last_name",
        "Email": "email",
        "BirthDate": "date_of_birth",
        "MemberNumber": "card_number",
    },
}
