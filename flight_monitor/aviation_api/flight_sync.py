import requests
import frappe
import json
# from frappe.utils import get_datetime, get_datetime_str
from datetime import datetime
from frappe.model.meta import get_meta

def ensure_arline_exists(payload: dict) -> None:
    """
    This function takes list of airline names and feeds to airline doctype if the airline does not exist.
    """
    airlines = frappe.get_all("Airline", pluck="airline")
    existing_airlines = set(airlines)

    airline_names_in_payload = {
        flight.get("airline",{}).get("name")
        for flight in payload.get("data", [])
        if flight.get("airline",{}).get("name")
    }

    for airline in airline_names_in_payload - existing_airlines:
        frappe.get_doc({
            "doctype":"Airline",
            "airline": airline
        }).insert(ignore_permissions=True, ignore_if_duplicate= True)

    frappe.db.commit()

def parse_iso_to_naive(iso_str):
    """
    This function converts ISO datetime (with +00:00 suffix) into a naive datetime object 
    """
    if not iso_str:
        return
    
    dt = datetime.fromisoformat(iso_str)
    return dt.replace(tzinfo=None)

def ensure_status_option(status_value: str):
    """
    Add new status option to Flight.status select field if not present.
    """
    meta = get_meta("Flight")
    df = next((f for f in meta.fields if f.fieldname == "status"), None)
    if not df or not df.options:
        return
    opts = [o.strip() for o in df.options.splitlines() if o.strip()]
    if status_value not in opts:
        opts.append(status_value)
        df.options = "\n".join(opts)
        frappe.get_doc(meta.as_dict()).save()
        frappe.clear_cache(doctype="Flight")


def sync_flight_statuses(): # payload: dict
    """
    Fetchs live flight data from external API and upserts records into the flight doctype.
    """
    # get settings
    settings_doc = frappe.get_single("Flight Settings")
    creds = settings_doc.get_credentials()
    # # print(creds)
    api_key = creds.get("api_key")

    if not api_key:
        frappe.log_error("sync flight statuses", "Missing Flight API Key in Flight Settings")
        # frappe.throw("Missing Flight API Key in Flight Settings")
        return
    
    # # use API URL from doc or switch to aviation stack as default
    base_url = creds.get("api_base_url") or "https://api.aviationstack.com/v1"
    endpoint = f"{base_url}/flights?access_key={api_key}"
    
    # try fetching data
    try:
        response = requests.get(endpoint, timeout=30)
        response.raise_for_status()
        data = response.json()
        # data = response.json()
        # data = json.dumps(data, indent= 4)
        # data = payload.get("data", [])
        frappe.log_error("Aviation Stack Payload", f"{data}")
    except Exception as e:
        frappe.log_error("sync_flight_statuses", f"Flight API request failed: {e}")
        return
    
    # ensure all the airlines are in place
    ensure_arline_exists(data)
    
    # upsert each flight record
    for flight in data.get("data",[]):
        try:
            iata = flight.get("flight",{}).get("iata")
            airline_name = flight.get("airline", {}).get("name")
            
            if not iata:
                continue
            
            # Normalize and ensure status option
            raw_status = flight.get("flight_status", "").lower()
            status_map = {
                "scheduled": "Scheduled",
                "boarding": "Boarding",
                "en route": "En Route",
                "landed": "Landed",
                "delayed": "Delayed",
                "cancelled": "Cancelled"
            }
            status_value = status_map.get(raw_status, raw_status.title())
            ensure_status_option(status_value)

            
            # preparing doc 
            doc_dict = {
                "doctype": "Flight",
                "flight_number": iata,
                "airline": frappe.db.get_value("Airline",{"airline": airline_name}),
                "origin": flight.get("departure",{}).get("iata"),
                "destination": flight.get("arrival",{}).get("iata"),
                "gate": flight.get("departure",{}).get("gate"),
                "destination": flight.get("arrival",{}).get("airport"),
                "origin": flight.get("departure",{}).get("airport"),
                "terminal": flight.get("departure",{}).get("terminal"),
                "delay_duration": flight.get("departure",{}).get("delay"),
                "status": status_value,
                "scheduled_departure": parse_iso_to_naive(flight.get("departure", {}).get("scheduled")),
                "estimated_departure": parse_iso_to_naive(flight.get("departure", {}).get("estimated")),
                "actual_departure": parse_iso_to_naive(flight.get("departure", {}).get("actual")),
                "scheduled_arrival": parse_iso_to_naive(flight.get("arrival", {}).get("scheduled")),
                "estimated_arrival": parse_iso_to_naive(flight.get("arrival", {}).get("estimated")),
                "actual_arrival": parse_iso_to_naive(flight.get("arrival", {}).get("actual")),
                "delay_duration": flight.get("departure", {}).get("delay"),
                "latitude": flight.get("departure", {}).get("terminal") or None,
                "longitude": flight.get("arrival", {}).get("terminal") or None,
            }
            
            # upsert logic
            if frappe.db.exists("Flight", {"flight_number":iata}):
                doc = frappe.get_doc("Flight", iata)
                doc.update(doc_dict)
                doc.save(ignore_permissions=True)
            else:
                doc = frappe.get_doc(doc_dict)
                doc.insert(ignore_permissions= True)
        except Exception as e:
            frappe.log_error("Sync flight statuses", f"Error: {e}")
            
    frappe.db.commit()

# payload = {"data":[{"flight_date":"2025-07-09","flight_status":"landed","departure":{"airport":"Sydney Kingsford Smith Airport","timezone":"Australia/Sydney","iata":"SYD","icao":"YSSY","terminal":"2","gate":"45","delay":15,"scheduled":"2025-07-09T10:30:00+00:00","estimated":"2025-07-09T10:30:00+00:00","actual":"2025-07-09T10:44:00+00:00","estimated_runway":"2025-07-09T10:44:00+00:00","actual_runway":"2025-07-09T10:44:00+00:00"},"arrival":{"airport":"Melbourne - Tullamarine Airport","timezone":"Australia/Melbourne","iata":"MEL","icao":"YMML","terminal":"3","gate":"3","baggage":null,"scheduled":"2025-07-09T12:05:00+00:00","delay":null,"estimated":"2025-07-09T12:00:00+00:00","actual":"2025-07-09T12:01:00+00:00","estimated_runway":"2025-07-09T12:01:00+00:00","actual_runway":"2025-07-09T12:01:00+00:00"},"airline":{"name":"Hawaiian Airlines","iata":"HA","icao":"HAL"},"flight":{"number":"4094","iata":"HA4094","icao":"HAL4094","codeshared":{"airline_name":"virgin australia","airline_iata":"va","airline_icao":"voz","flight_number":"832","flight_iata":"va832","flight_icao":"voz832"}},"aircraft":null,"live":null},{"flight_date":"2025-07-09","flight_status":"scheduled","departure":{"airport":"Tokunoshima","timezone":"Asia/Tokyo","iata":"TKN","icao":"RJKN","terminal":null,"gate":"1","delay":null,"scheduled":"2025-07-09T19:00:00+00:00","estimated":"2025-07-09T19:00:00+00:00","actual":null,"estimated_runway":null,"actual_runway":null},"arrival":{"airport":"Kagoshima","timezone":"Asia/Tokyo","iata":"KOJ","icao":"RJFK","terminal":"D","gate":null,"baggage":null,"scheduled":"2025-07-09T20:15:00+00:00","delay":null,"estimated":null,"actual":null,"estimated_runway":null,"actual_runway":null},"airline":{"name":"Japan Airlines","iata":"JL","icao":"JAL"},"flight":{"number":"3798","iata":"JL3798","icao":"JAL3798","codeshared":null},"aircraft":null,"live":null},{"flight_date":"2025-07-09","flight_status":"scheduled","departure":{"airport":"Tokunoshima","timezone":"Asia/Tokyo","iata":"TKN","icao":"RJKN","terminal":null,"gate":"1","delay":null,"scheduled":"2025-07-09T19:00:00+00:00","estimated":"2025-07-09T19:00:00+00:00","actual":null,"estimated_runway":null,"actual_runway":null},"arrival":{"airport":"Kagoshima","timezone":"Asia/Tokyo","iata":"KOJ","icao":"RJFK","terminal":"D","gate":null,"baggage":null,"scheduled":"2025-07-09T20:15:00+00:00","delay":null,"estimated":null,"actual":null,"estimated_runway":null,"actual_runway":null},"airline":{"name":"ANA","iata":"NH","icao":"ANA"},"flight":{"number":"4354","iata":"NH4354","icao":"ANA4354","codeshared":{"airline_name":"japan airlines","airline_iata":"jl","airline_icao":"jal","flight_number":"3798","flight_iata":"jl3798","flight_icao":"jal3798"}},"aircraft":null,"live":null}]}