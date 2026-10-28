CAMPUS_POLICIES = {

    "Richfield Centurion": {
        "maximum_hours": 2
    },

    "Richfield Braamfontein": {
        "maximum_hours": 3
    },

    "Richfield Polokwane": {
        "maximum_hours": 4
    }
}


def validate_booking(campus, duration):

    policy = CAMPUS_POLICIES.get(campus)

    if duration > policy["maximum_hours"]:

        return (
            False,
            f"Maximum booking duration is "
            f"{policy['maximum_hours']} hours."
        )

    return True, "Valid Booking"