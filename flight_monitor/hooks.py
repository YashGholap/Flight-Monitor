app_name = "flight_monitor"
app_title = "Flight Monitor"
app_publisher = "Yash Gholap"
app_description = "Flight Monitoring System."
app_email = "gholapyash@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "flight_monitor",
# 		"logo": "/assets/flight_monitor/logo.png",
# 		"title": "Flight Monitor",
# 		"route": "/flight_monitor",
# 		"has_permission": "flight_monitor.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/flight_monitor/css/flight_monitor.css"
# app_include_js = "/assets/flight_monitor/js/flight_monitor.js"

# include js, css files in header of web template
# web_include_css = "/assets/flight_monitor/css/flight_monitor.css"
# web_include_js = "/assets/flight_monitor/js/flight_monitor.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "flight_monitor/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "flight_monitor/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "flight_monitor.utils.jinja_methods",
# 	"filters": "flight_monitor.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "flight_monitor.install.before_install"
# after_install = "flight_monitor.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "flight_monitor.uninstall.before_uninstall"
# after_uninstall = "flight_monitor.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "flight_monitor.utils.before_app_install"
# after_app_install = "flight_monitor.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "flight_monitor.utils.before_app_uninstall"
# after_app_uninstall = "flight_monitor.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "flight_monitor.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"flight_monitor.tasks.all"
# 	],
# 	"daily": [
# 		"flight_monitor.tasks.daily"
# 	],
# 	"hourly": [
# 		"flight_monitor.tasks.hourly"
# 	],
# 	"weekly": [
# 		"flight_monitor.tasks.weekly"
# 	],
# 	"monthly": [
# 		"flight_monitor.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "flight_monitor.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "flight_monitor.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "flight_monitor.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["flight_monitor.utils.before_request"]
# after_request = ["flight_monitor.utils.after_request"]

# Job Events
# ----------
# before_job = ["flight_monitor.utils.before_job"]
# after_job = ["flight_monitor.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"flight_monitor.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

scheduler_events = {
	"hourly": [
		"flight_monitor.aviation_api.flight_sync.enque_sync_flight"
	],  
    # "cron": {
    #     "*/2 * * * *":[
    #         "flight_monitor.aviation_api.flight_sync.enque_sync_flight"
    #     ]
    # }
}

# fixtures = [
#     # Roles
#     {"dt": "Role", "filters": [["name", "in", [
#         "Support Staff", "Traveler", "Operations Manager"
#     ]]]},

#     # Permissions (Custom DocPerms)
#     {"dt": "Custom DocPerm", "filters": [["parent", "in", [
#         "Flight", "Airline", "Dashboard", "Dashboard Chart", "Report"
#     ]]]},

#     # Reports
#     {"dt": "Report", "filters": [["ref_doctype", "in", [
#         "Flight", "Airline"
#     ]]]},

#     # Dashboard Charts
#     {"dt": "Dashboard Chart", "filters": [["document_type", "in", [
#         "Flight"
#     ]]]},

#     # Dashboards (if you're using Workspace/Dashboard Doctype)
#     {"dt": "Dashboard", "filters": [["name", "in", [
#         "Flight Operations Dashboard"
#     ]]]},

#     # Web Pages (like track-flight)
#     {"dt": "Web Page", "filters": [["name", "in", [
#         "track-flight"
#     ]]]},

#     # Property Setters (if you made dynamic field updates like adding fields to List View)
#     {"dt": "Property Setter", "filters": [["doc_type", "in", [
#         "Flight"
#     ]]]}
# ]

