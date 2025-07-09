# Copyright (c) 2025, Yash Gholap and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns = [
		{"fieldname": "flight_number", "label": "Flight", "fieldtype": "Data", "width": 150},
		{"fieldname": "status", "label": "Status", "fieldtype": "Data", "width": 100},
		{"fieldname": "delay_duration", "label": "Delay (min)", "fieldtype": "Int", "width": 100},
		{"fieldname": "scheduled_departure", "label": "Scheduled Departure", "fieldtype": "Datetime", "width": 180}
	]

	conditions = []
	if filters.get("status"):
		conditions.append("status = %(status)s")
	if filters.get("delay_duration"):
		conditions.append("delay_duration >= %(delay_duration)s")

	condition_str = " and ".join(conditions)
	if condition_str:
		condition_str = "where " + condition_str

	data = frappe.db.sql(
		f"""
		SELECT flight_number, status, delay_duration, scheduled_departure
		FROM `tabFlight`
		{condition_str}
		ORDER BY scheduled_departure DESC
		""",
		filters,
		as_dict=True
	)
	return columns, data
