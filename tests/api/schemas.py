"""JSON Schemas describing restful-booker response contracts."""

BOOKING = {
    "type": "object",
    "required": ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"],
    "properties": {
        "firstname": {"type": "string"},
        "lastname": {"type": "string"},
        "totalprice": {"type": "number"},
        "depositpaid": {"type": "boolean"},
        "bookingdates": {
            "type": "object",
            "required": ["checkin", "checkout"],
            "properties": {
                "checkin": {"type": "string"},
                "checkout": {"type": "string"},
            },
        },
        "additionalneeds": {"type": "string"},
    },
}

CREATE_BOOKING_RESPONSE = {
    "type": "object",
    "required": ["bookingid", "booking"],
    "properties": {
        "bookingid": {"type": "integer"},
        "booking": BOOKING,
    },
}

BOOKING_IDS = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["bookingid"],
        "properties": {"bookingid": {"type": "integer"}},
    },
}
