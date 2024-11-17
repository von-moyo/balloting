import sys
import requests

def main():
    # Check if the correct number of arguments are provided
    if len(sys.argv) != 4:
        print("Usage: python script.py <matric_no> <password> <HallId>")
        sys.exit(1)

    matric_no = sys.argv[1]
    password = sys.argv[2]
    hall_id = sys.argv[3]

    # Step 1: Log in to obtain the token
    login_url = 'https://studentportalbeta.unilag.edu.ng/users/login'
    login_data = {
        'MatricNo': matric_no,
        'Password': password
    }

    try:
        login_response = requests.post(login_url, data=login_data, timeout=120)
        login_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("The initial request failed or timed out:", e)
        sys.exit(1)

    # Extract the authorization token from the login response
    login_json = login_response.json()
    authorization_token = login_json.get("Data", {}).get("Token")

    if not authorization_token:
        print("Failed to obtain the authorization token.")
        sys.exit(1)

    # Step 2: Make the reservation request with the token
    reservation_url = 'https://studentportalbeta.unilag.edu.ng/accomodation/saveAccommodationReservation'
    headers = {
        'Authorization': f'Bearer {authorization_token}'
    }
    reservation_data = {
        'HallId': hall_id
    }

    try:
        reservation_response = requests.post(reservation_url, headers=headers, data=reservation_data)
        reservation_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Failed to make the reservation request:", e)
        sys.exit(1)

    # Print the reservation response
    print("Reservation:", reservation_response.json())

if __name__ == "__main__":
    main()
