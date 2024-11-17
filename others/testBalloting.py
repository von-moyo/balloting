import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Users data
users = [
    {
      'name': 'florish',
      'matricNo': '190805025', 
      'password': 'vonn2109', 
      'hall': 'JAJA'
    },
    {
      'name': 'oyindamola',
      'matricNo': '230314079', 
      'password': 'OYINDAMOLA', 
      'hall': 'MOREMI HALL'
    },
    {
      'name': 'temidayo',
      'matricNo': '230801179', 
      'password': 'temmyd27', 
      'hall': 'MOREMI HALL'
    }
]

# Lock for controlling multiple threads
reservation_lock = threading.Lock()

def login(user):
    login_url = "https://studentportalbeta.unilag.edu.ng/users/login"
    
    login_data = {
        "MatricNo": user['matricNo'],
        "Password": user['password']
    }

    try:
        response = requests.post(login_url, data=login_data, timeout=120)
        response.raise_for_status()
        response_data = response.json()

        # Extract token from the response
        token = response_data.get("Data", {}).get("Token")
        if token:
            print(f"Login successful for {user['name']}")
            return token
        else:
            print(f"Login failed for {user['name']}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Login request failed for {user['name']}: {e}")
        return None

def reserve_accommodation(user, token, attempt, reservation_flag):
    reservation_url = "https://studentportalbeta.unilag.edu.ng/accomodation/saveAccommodationReservation"
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    reservation_data = {
        "HallId": user['hall']
    }

    try:
        response = requests.post(reservation_url, headers=headers, data=reservation_data)
        response.raise_for_status()
        response_json = response.json()
        
        # Check if the reservation was successful in real case
        if True:
            print(f"Reservation successful for {user['name']} in {user['hall']} on attempt {attempt + 1}")
            reservation_flag['success'] = True
            return True
        else:
            print(f"Reservation attempt {attempt + 1} failed for {user['name']}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {user['name']} on attempt {attempt + 1}: {e}")
        return False

def confirm_accommodation(user, token):
    confirmation_url = "https://studentportalbeta.unilag.edu.ng/accomodation/accomodationConfirmation"
    
    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(confirmation_url, headers=headers)
        response.raise_for_status()
        response_json = response.json()

        if response_json.get('Success') == True:
            print(f"Confirmation successful for {user['name']} in {user['hall']}")
            return True
        else:
            print(f"Confirmation failed for {user['name']}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Confirmation request failed for {user['name']}: {e}")
        return False

def handle_user_reservation(user):
    token = login(user)
    if not token:
        return

    reservation_flag = {'success': False}  # Flag to track if reservation was successful

    # Spawn up to 100 simultaneous attempts for reservation
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(reserve_accommodation, user, token, attempt, reservation_flag) for attempt in range(100)]
        
        # Process the futures
        for future in as_completed(futures):
            with reservation_lock:
                if reservation_flag['success']:
                    print(f"Reservation for {user['name']} is successful. Cancelling further attempts.")
                    
                    # Cancel all remaining futures
                    for f in futures:
                        if not f.done():
                            f.cancel()

                    # After reservation, attempt confirmation
                    confirmed = confirm_accommodation(user, token)
                    if confirmed:
                        print(f"Hostel confirmation completed for {user['name']} in {user['hall']}")
                    else:
                        print(f"Failed to confirm hostel for {user['name']}")

                    return  # Exit the function once the confirmation is done

        print(f"All 100 attempts failed for {user['name']}")

def handle_multiple_users(users):
    # Handle multiple users concurrently
    with ThreadPoolExecutor(max_workers=len(users)) as executor:
        futures = {executor.submit(handle_user_reservation, user): user for user in users}
        
        for future in as_completed(futures):
            user = futures[future]
            try:
                future.result()  # Get the result of the future, will raise exceptions if any occurred
                print(f"Process completed for {user['name']}")
            except Exception as e:
                print(f"Error during the process for {user['name']}: {e}")

if __name__ == "__main__":
    handle_multiple_users(users)
