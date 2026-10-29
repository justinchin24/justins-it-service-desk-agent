import os
# Requests is used to create a bridge between this script and the FastAPI script (app.py), allowing GET and POST web requests to be sent.
import requests
from dotenv import load_dotenv
from google import genai
# The 'types' module allows Google's configuration templates to be used (for parameters, as an example)
from google.genai import types

load_dotenv()

# Initialize the official Google GenAI client
client = genai.Client()

# Tool wrapper #1 (tool wrapper = bridge between Gemini and app.py)
# Gemini looks at the user's query, reads the instructions between the triple quotes, and extracts the employee ID and system name values from the query. The function then runs and sends the extracted values in JSON format to the URL. If there is an error, the message is stored in 'e' and assigned to a dictionary value called "error", which Gemini uses to convert the error message to something more user friendly to the end user. '-> dict' is a type hint and has no impact on how the function runs.
def check_permissions(employee_id: str, system_name: str) -> dict:
    """Check active access permissions for an employee in an enterprise system."""
    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/permissions",
            json={"employee_id": employee_id, "system_name": system_name}
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Tool wrapper #2
# 'Medium' is assigned as the default priority value if none is specified in the user's query
def create_ticket(category: str, description: str, priority: str = "Medium") -> dict:
    """Log a new incident or service request ticket into the IT helpdesk queue."""
    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/tickets",
            json={"category": category, "description": description, "priority": priority}
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Tool wrapper #3
# Returns the service name, health, and latency in json format
def get_system_status(service_name: str) -> dict:
    """Check the real-time health and latency of an infrastructure domain."""
    try:
        response = requests.get(f"http://127.0.0.1:8000/api/status/{service_name}")
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Bundle the tool wrappers/functions into a single list for passing to Gemini. If additional wrappers are configured, the name can be inserted into this list.
my_tools = [check_permissions, create_ticket, get_system_status]

# A lookup table that maps string key names to the Python functions of the same name above, so that Python knows which function to execute.
tool_map = {
    "check_permissions": check_permissions,
    "create_ticket": create_ticket,
    "get_system_status": get_system_status
}


# Agent Execution Loop

def run_it_agent(user_prompt: str):
    """Sends a user prompt to Gemini with tools enabled, handling automatic execution."""
    print(f"\n👤 User: {user_prompt}")

    # client.chats.create is a feature of the Google GenAI SDK that tells the SDK to start a multi-turn chat session with the Gemini API, use a specified chat model, and package several parameters into 'config'
    chat = client.chats.create(
        model="gemini-3.5-flash-lite",
        config=types.GenerateContentConfig( # The 3 model parameters below are packaged for reusability
            tools=my_tools,
            temperature=0.0, # Controls how create, random, or varied Gemini's responses are. 0.0 is strict, while higher numbers give room for more variation or expression.
            system_instruction=(
                "You are an autonomous IT Service Desk assistant. "
                "Use your tools to query enterprise systems, check permissions, "
                "check infrastructure health, and log support tickets accurately."
            )
        )
    )

    # Send initial user message to Gemini. chat.send_message() does the work to return Gemini's response and stores it in 'response'.
    response = chat.send_message(user_prompt)

    # Check if Gemini decided to call one or more tools using the Google SDK's built-in feature called 'function_calls', which . The 'for' loop allows multiple tools to be called in a single query. call.name (returns the name of the function that Gemini wants to run) and call.args (returns the Python dictionary of arguments that Gemini extracted from the user's query) are built-in attributes provided by Google's SDK.
    if response.function_calls:
        for call in response.function_calls:
            # Example: 🛠️ [Agent Tool Call]: Calling `get_system_status` with args {'service_name': 'vpn'}
            print(f"🛠️ [Agent Tool Call]: Calling `{call.name}` with args {call.args}")
            
            selected_function = tool_map.get(call.name) # Variable that becomes an alias for the applicable function, allowing 'selected_function' to be run as a function itself
            if selected_function:
                # The double asterisks unpack the key-value pairs inside call.args and formats them so that the function can run successfully. An HTTP request, using the parameters in the matching function above, is sent to the server (app.py). The corresponding decorator runs its logic and its defined return dictionary is passed back to tool_result in agent.py.
                tool_result = selected_function(**call.args)
                print(f"📥 [FastAPI Backend Response]: {tool_result}")
                
                # Sends the function name and returned dictionary values to Gemini, who returns its readable answer in final_response. It knows how to respond because the 'chat' object that was created above (chat = client.chats.create) stores all of the conversation history in memory.
                final_response = chat.send_message(
                    types.Part.from_function_response(
                        name=call.name,
                        response={"result": tool_result}
                    )
                )
                print(f"🤖 Gemini: {final_response.text}")
                return final_response.text
    else:
        # If there are no functions to call, Gemini responds accordingly with a readable answer
        print(f"🤖 Gemini: {response.text}")
        return response.text


# Test directly in the terminal. Need to ensure that the mock server (app.py) is running before this can be tested by running 'uvicorn app:app --reload'.
if __name__ == "__main__":
        
    run_it_agent("Can you check the current health status of Jira?")
    
    run_it_agent("Can you check access permissions for employee EMP-4412 on Active Directory?")
    
    run_it_agent("Please log a high priority ticket for a critical VPN outage affecting remote workers.")