import requests
import frappe
import json

def sync_flight_statuses(payload: dict):
    """
    Fetchs live flight data from external API and upserts records into the flight doctype.
    """
    # get settings
    settings_doc = frappe.get_doc("Flight Settings")
    api_key = settings_doc.api_key
    if not api_key:
        frappe.log_error("sync flight statuses", "Missing Flight API Key in Flight Settings")
        # frappe.throw("Missing Flight API Key in Flight Settings")
        return
    
    # use API URL from doc or switch to aviation stack as default
    base_url = settings_doc.api_base_url or "https://api.aviationstack.com/v1"
    endpoint = f"{base_url}/flights?access_key={api_key}"
    
    # try fetching data
    try:
        # response = requests.get(endpoint, timeout=30)
        # response.raise_for_status()
        # data = response.json().get("data", [])
        data = payload.get("data", [])
        frappe.log_error("Aviation Stack Payload", f"{data}")
    except Exception as e:
        frappe.log_error("sync_flight_statuses", f"Flight API request failed: {e}")
        return
    
    # upsert each flight record
    for flight in data:
        iata = flight.get("flight",{}).get("iata")
        airline_name = flight.get("airline", {}).get("name")
        
        if not iata:
            continue
        
        if airline_name:
            frappe.get_doc({
                "doctype": "Airline",
                "airline": airline_name,
                "name": airline_name
            }).insert(ignore_permissions=True, ignore_if_duplicate=True)
            frappe.db.commit()
            
        # preparing doc 
        doc_dict = {
            "doctype": "Flight",
            "flight_number": iata,
            "airline": frappe.db.get_value("Airline",{"airline": airline_name}),
            "origin": flight.get("departure",{}).get("iata"),
            "destination": flight.get("arrival",{}).get("iata"),
            "status": flight.get("flight_status"),
            "scheduled_departure": flight.get("departure", {}).get("scheduled"),
            "estimated_departure": flight.get("departure", {}).get("estimated"),
            "actual_departure": flight.get("departure", {}).get("actual"),
            "scheduled_arrival": flight.get("arrival", {}).get("scheduled"),
            "estimated_arrival": flight.get("arrival", {}).get("estimated"),
            "actual_arrival": flight.get("arrival", {}).get("actual"),
            "delay_duration": flight.get("departure", {}).get("delay"),
            "latitude": flight.get("departure", {}).get("terminal") or None,
            "longitude": flight.get("arrival", {}).get("terminal") or None,
        }
        
        # upsert logic
        if frappe.db.exists("Flights", iata):
            doc = frappe.get_doc("Flight", iata)
            doc.update(doc_dict)
            doc.save(ignore_permissions=True)
        else:
            doc = frappe.get_doc("Flight", doc_dict)
            doc.insert(ignore_permissions= True)
            
    frappe.db.commit()