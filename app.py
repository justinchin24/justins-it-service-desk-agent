# This script defines a mock server that provides a way to test the agent locally without needing to connect to an external system with consistent results that you know to expect.

# FastAPI is used to create the web application instance.  It's the engine that sets up routing and listens for incoming web requests.  HTTPException is FastAPI's built-in error handler for web requests and network protocols, which sends back clean HTTP error codes with an explanation message to the user.
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# This is a built-in Python module to generate random numbers (e.g., ticket IDs) or simulate server response latencies to mock real-world behavior.
import random

# Displays a title and version number at the top of the UI page
app = FastAPI(title="Enterprise IT Service Desk Mock API", version="1.0")

# Within this class are 2 attributes that need to be included in the user's request, or else FastAPI does not proceed and sends back an error advising that something is missing. Pydantic handles the validation to check this.
class PermissionRequest(BaseModel):
    employee_id: str
    system_name: str

# Similar to the class above, these attributes also need to be included in the user's request, or else FastAPI does not proceed and sends back an error advising that something is missing. Pydantic handles the validation to check this. This needs to be separate from the class above that looks up the ID and system name and then checks the user's permissions inside that system name.
class TicketRequest(BaseModel):
    category: str
    description: str
    priority: str = "Medium"

# The '@' character is a 'decorator' which attaches a set of instructions to a function. For this check_permissions function, it is telling FastAPIto listen for POST requests (data coming in) and only runs if the request is sent to the path ending in /api/permissions.
@app.post("/api/permissions")
def check_permissions(payload: PermissionRequest):
    valid_systems = ["Jira", "ServiceNow", "Active Directory", "VPN", "Concur"]
    if payload.system_name not in valid_systems:
        raise HTTPException(status_code=404, detail="System not found in enterprise registry.")
    
    return {
        "employee_id": payload.employee_id,
        "system": payload.system_name,
        "status": "Active",
        "access_level": "Standard User",
        "last_audit_date": "2026-09-15"
    }

# For this create_ticket function, it is telling FastAPI to listen for POST requests (data coming in) and only runs if the request is sent to the path ending in /api/tickets.
@app.post("/api/tickets")
def create_ticket(payload: TicketRequest):
    ticket_id = f"INC-{random.randint(100000, 999999)}"
    return {
        "ticket_id": ticket_id,
        "status": "Logged",
        "category": payload.category,
        "priority": payload.priority,
        "message": "Ticket successfully created and routed to the IT Service Desk queue."
    }

# For get_system_status, FastAPI will hand the service_name portion of the URL to the function. @app.get retrieves or reads data, instead of sending or creating data like @app.post does.
@app.get("/api/status/{service_name}")
def get_system_status(service_name: str):
    statuses = ["Operational", "Degraded Performance", "Under Maintenance"]
    health = statuses[len(service_name) % len(statuses)] # This calculation takes the length of the service name and divides it by the number of options in 'statuses' to pick a consistent status with each service name. It's for testing/simulation purposes.
    return {
        "service": service_name,
        "health": health,
        "latency_ms": random.randint(25, 120) # Returns a random response time in ms between 25 and 120.
    }