
# ✈️ Flight Monitor – Frappe App

A Frappe-based app for **Live Flight Status Monitoring** with real-time updates from the AviationStack API. Built for travelers, support staff, and operations teams to track flights, delays, and manage airline operations efficiently.

---

## ✅ Features

### 🔄 Flight Sync & Automation
- Integrates with [AviationStack API](https://aviationstack.com/) to fetch live flight status.
- Automatically updates the **Flight** doctype with:
  - Flight Number, Airline, Status, Terminal, Gate
  - Departure and Arrival times (Scheduled, Estimated, Actual)
  - Delay Duration, Latitude/Longitude
- Uses a background job (`frappe.enqueue`) to avoid UI blocking.
- Runs every hour using `cron` scheduler.

### 👥 Roles and User Experiences

#### 👤 Traveler
- Web page: `/track-flight`
- Input flight number → View status, gate, boarding time.
- Built with Frappe’s **Web Page** and minimal form.

#### 🛫 Support Staff
- Custom **Script Report**: `Flight Report`
- Filters: `Status`, `Delay Duration`
- Permissions set via `Support Staff` role.

#### 🧭 Operations Manager
- 📊 **Dashboard** with charts:
  - `Delays by Airline` (Bar Chart with filters)
  - Time-based view (weekly, monthly)
- Summary-level insights, useful for real-time overview.

---

## ⚙️ Installation

### Prerequisites
- Python 3.10+
- Redis, Node.js, Yarn
- Bench & Frappe Framework installed

### 1. Get the app

```bash
cd frappe-bench
bench get-app https://github.com/YashGholap/Flight-Monitor.git
```

### 2. Install app on your site

```bash
bench --site [your-site-name] install-app flight_monitor
```

> Replace `[your-site-name]` with your actual site name.

### 3. Apply database changes and load fixtures

```bash
bench --site [your-site-name] migrate
```

This loads:
- Roles
- Reports
- Dashboard Charts
- Web Pages
- Custom Fields (via fixtures)

---

## 🚀 Usage

### 1. Setup API Credentials

Go to **Flight Settings**:
```
Flight Monitor > Flight Settings
```
- Enter your AviationStack API key
- Optionally set the base URL

### 2. Sync Flight Data (Manual)

From the Frappe Console or API:

```python
from flight_monitor.aviation_api.flight_sync import sync_flight_statuses
sync_flight_statuses()
```

### 3. Automated Background Sync

Your `hooks.py` includes a cron job:

```python
scheduler_events = {
	"hourly": [
		"flight_monitor.aviation_api.flight_sync.enque_sync_flight"
	],  
}
```

> Every hour, the app will auto-sync flights.

---

## 📂 Directory Structure

```
flight_monitor/
├── aviation_api/
│   └── flight_sync.py          # Main logic to sync flights
|   └── get_flight_status.py    # for reports
├── config/
│   └── desktop.py              # Module registration
├── public/
│   └── track_flight.html       # Traveler's input form
├── flight_monitor/
│   └── fixtures/               # All exported fixtures (roles, reports, charts)
```

---

## ✅ Best Practices Followed

- ✔️ `frappe.enqueue` used for async jobs
- ✔️ Scheduler in `hooks.py`
- ✔️ Data normalization:
  - ISO timestamps → naive Python datetime
  - Dynamic Select field options (e.g. `status`) handled via `get_meta()`
- ✔️ Flight records **upserted** using primary key (`flight_number`)
- ✔️ Modular, reusable functions (e.g. `ensure_airline_exists()`)
- ✔️ Reports and charts filtered via `filters_json` to avoid bloat
- ✔️ Fixtures stored and loaded using `export-fixtures` and `migrate`

---

## 🧪 Development Tips

- To export new fixtures:

```bash
bench --site [your-site-name] export-fixtures
```

- To reload on a new site:

```bash
bench --site [your-site-name] migrate
```

- To test background job from console:

```python
frappe.enqueue("flight_monitor.aviation_api.flight_sync.sync_flight_statuses")
```

---

## 📬 License

MIT License – Free to use, modify, and distribute with credit.

---

## 🙌 Author

Built by [Yash Gholap](https://github.com/YashGholap)  
Connect on [LinkedIn](https://linkedin.com/in/yashgholap)

---
