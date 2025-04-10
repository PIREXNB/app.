import json
import time
import requests

# Dictionary to store API keys and their expiration timestamps
api_keys = {}

def add_api_key(key, days):
    expiration_time = time.time() + (days * 86400)  # Convert days to seconds
    api_keys[key] = expiration_time
    return {"message": f"API key '{key}' added with {days} days validity."}

def remove_api_key(key):
    if key in api_keys:
        del api_keys[key]
        return {"message": f"API key '{key}' has been removed successfully."}
    return {"error": "API key not found."}, 404

def check_all_api_keys():
    active_keys = {}
    current_time = time.time()

    for key, expiry in api_keys.items():
        remaining_days = int((expiry - current_time) / 86400)  # Convert seconds to days
        if remaining_days > 0:
            active_keys[key] = remaining_days

    return {"active_keys": active_keys}

def proxy_request(room_id, name_spam, player_id, api_key):
    # Validate API key
    if not api_key or api_key not in api_keys or api_keys[api_key] < time.time():
        return {"error": "Invalid or expired API key."}, 403

    # Calculate remaining days for the API key
    current_time = time.time()
    remaining_days = int((api_keys[api_key] - current_time) / 86400)

    # Send request to the game server
    url = f"https://ozw8wy29r3.execute-api.ap-southeast-1.amazonaws.com/{room_id}/{name_spam}/{player_id}"
    try:
        response = requests.get(url)
        data = response.json()
    except requests.exceptions.RequestException:
        return {"error": "Failed to connect to the game server. Please try again later."}, 500

    # Add developer signature and remaining days
    data["Developers"] = "@siir_pirex & @bradx"
    data["remaining_days"] = remaining_days

    return data

def handler(request):
    # Get the path parameters and query parameters
    path = request.path.strip('/').split('/')
    room_id = path[0]
    name_spam = path[1]
    player_id = path[2]

    # Check for valid query parameter 'key'
    api_key = request.args.get('key')

    # Handle requests based on the path
    if request.method == 'GET':
        if path[0] == 'addky' and len(path) == 3:
            # Add API key
            key = path[1]
            days = int(path[2])
            response = add_api_key(key, days)
            return json.dumps(response), 200

        elif path[0] == 'removeky' and len(path) == 2:
            # Remove API key
            key = path[1]
            response = remove_api_key(key)
            return json.dumps(response), 200

        elif path[0] == 'Brad' and path[1] == 'vcheck':
            # Check all active API keys
            response = check_all_api_keys()
            return json.dumps(response), 200

        else:
            # Handle proxy request to game server
            response = proxy_request(room_id, name_spam, player_id, api_key)
            return json.dumps(response), 200

    return {"error": "Method not allowed."}, 405
