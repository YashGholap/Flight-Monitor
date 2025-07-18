# Copyright (c) 2025, Yash Gholap and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class FlightSettings(Document):
	def get_credentials(self):
		"""
		This functions returns the essentials credentials required to call the Flight API.
		"""
		return {
			"api_key": self.get_password("api_key"),
			"api_base_url" : self.api_base_url
		}
