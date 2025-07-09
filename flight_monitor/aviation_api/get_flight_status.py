import frappe
from frappe.utils import format_datetime

@frappe.whitelist()
def get_flight_status(flight_number, date):
    flight = frappe.db.get_value(
        "Flight",
        {
            "flight_number": flight_number,
            "scheduled_departure": ["like",f"{date}%"]
        },
        [
            "status",
            "gate",
            "terminal",
            "scheduled_departure",
            "estimated_departure",
            "actual_departure"
        ],
        as_dict=True
    )

    if flight:
        for key in ["scheduled_dparture", "estimated_departure", "actual_departure"]:
            if flight.get(key):
                flight[key] = format_datetime(flight[key])

    return flight