import requests
import frappe
import json
from datetime import datetime
from frappe.model.meta import get_meta



def enque_sync_flight():
    """
    This Function takes flight sync function and runs in background through worker.
    """
    try:
        frappe.enqueue(
            method="flight_monitor.aviation_api.flight_sync.sync_flight_statuses",
            queue="default",
            is_async=True
        )
        frappe.log_error("Flight Sync Enqueue", "Function sync_flight_statuses enqueued successfully")
    except Exception as e:
        frappe.log_error("Flight Sync Enqueue", f"Error : {e}\n Traceback: {frappe.get_traceback()}")
        raise 

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


def sync_flight_statuses(): 
    """
    Fetchs live flight data from external API and upserts records into the flight doctype.
    """
    settings_doc = frappe.get_single("Flight Settings")
    creds = settings_doc.get_credentials()
    api_key = creds.get("api_key")

    if not api_key:
        frappe.log_error("sync flight statuses", "Missing Flight API Key in Flight Settings")
        return
    
    # # use API URL from doc or switch to aviation stack as default
    base_url = creds.get("api_base_url") or "https://api.aviationstack.com/v1"
    endpoint = f"{base_url}/flights?access_key={api_key}"
    
    # try fetching data
    try:
        response = requests.get(endpoint, timeout=30)
        response.raise_for_status()
        data = response.json()
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
    