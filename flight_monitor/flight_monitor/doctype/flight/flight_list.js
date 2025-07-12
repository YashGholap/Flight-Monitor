frappe.listview_settings["Flight"] = {
    onload: function(listview){
        listview.page.add_inner_button(__("Sync Flight Data Manually"), ()=>{
            frappe.call({
                method: "flight_monitor.aviation_api.flight_sync.sync_flight_statuses",
                callback(r){
                    if(!r.exc) {
                        frappe.msgprint(__("Flight data synced sucessfully!"));
                        listview.refresh;
                    }
                    else{
                    frappe.throw(__("Flight data sync failed!"));
                    frappe.log_error("Manual Flight Sync", `Error: ${r.exc} \n Traceback: \n${frappe.get_traceback()}`);
                    }
                }
            })
        });
    }
}