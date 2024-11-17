import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# USERS
# yr 5 -> 18
# yr 4 -> 19
# yr 3 -> 21
# yr 2 -> 23
# yr 1 -> 24

# 400 AND 500 LEVEL
# users = [
#     {
#       'name': 'florish',
#       'matricNo': '190805025', 
#       'password': 'vonn2109', 
#       'hall': 'MARIERE HALL'
#     },
#     {
#       'name': 'daniel',
#       'matricNo': '190501029', 
#       'password': 'Awesome&God33', 
#       'hall': 'MARIERE HALL'
#     },
#     {
#       'name': "daniel (bolade's guy 3)",
#       'matricNo': '190806001', 
#       'password': 'dumebiag', 
#       'hall': 'MARIERE HALL'
#     },
# ]

# 300LEVEL
users = [
    {
      'name': 'sheriff',
      'matricNo': '210201186', 
      'password': 'olami', 
      'hall': 'MARIERE HALL'
    },
    {
      'name': "zainab (sheriff's guy 1)",
      'matricNo': '210903007', 
      'password': 'eniola', 
      'hall': 'MADAM TINUBU HALL'
    },
    {
      'name': "x (bolade's guy 1)",
      'matricNo': '210801043', 
      'password': ',', 
      'hall': 'MADAM TINUBU HALL'
    },
    {
      'name': "y (bolade's guy 2)",
      'matricNo': '210801030', 
      'password': 'fattymama08', 
      'hall': 'MADAM TINUBU HALL'
    },
]

# 200 LEVEL
# users = [
#     {
#       'name': 'oyindamola',
#       'matricNo': '230314079', 
#       'password': 'OYINDAMOLA', 
#       'hall': 'MOREMI HALL'
#     },
#     {
#       'name': 'temidayo',
#       'matricNo': '230801179', 
#       'password': 'temmyd27', 
#       'hall': 'MOREMI HALL'
#     },
#     {
#         'name': 'daniel (sheriff's guy 2)',
#         'matricNo': '230319021', 
#         'password': 'danny', 
#         'hall': 'MARIERE HALL'
#     },
# ]

# 100 LEVEL
# users =[
    
# ]


def loginAndAccessAccommodation(user):
    loginUrl = 'https://studentportalbeta.unilag.edu.ng/users/login'
    accomodationReservationUrl = 'https://studentportalbeta.unilag.edu.ng/accomodation/saveAccommodationReservation'
    accomodationConfirmationUrl = 'https://studentportalbeta.unilag.edu.ng/accomodation/accomodationConfirmation'

    name = user['name']
    matricNo = user['matricNo']
    password = user['password']
    hall = user['hall']

    session = requests.Session()
    loginData = {'matricNo': matricNo, 'password': password}
    response = session.post(loginUrl, data=loginData)

    if response.status_code == 200:
        responseData = response.json()
        success = responseData.get("Success")
        token = responseData.get("Data", {}).get("Token")

        if success and token:
            print(f"Login successful for {name}")
            headers = {'Authorization': f'Bearer {token}'}
            reservationData = {'HallId': hall}

            # Retry accommodation reservation up to 100 times or until successful
            reservation_success = False
            print(f"Trying balloting for {name} in {hall}...")
            for attempt in range(10000):
                # print(f"Reservation attempt {attempt + 1} for {name}")
                reservationResponse = session.post(accomodationReservationUrl, headers=headers, data=reservationData)
                if reservationResponse.status_code == 200:
                    reservationData = reservationResponse.json()
                    if reservationData.get("Success") == True:
                        print(f"Reservation successful for {name} on attempt {attempt + 1}")
                        reservation_success = True
                        break
                time.sleep(0.1)  # Delay to avoid too rapid requests

            if not reservation_success:
                return {"matricNo": matricNo, "success": False, "message": "Failed to reserve accommodation after 100 attempts"}
            
            # Only proceed with confirmation if reservation is successful
            if reservation_success == True:
                for attempt in range(10000):
                    print(f"Confirmation attempt {attempt + 1} for {name}")
                    confirmationResponse = session.get(accomodationConfirmationUrl, headers=headers)
                    if confirmationResponse.status_code == 200:
                        confirmationData = confirmationResponse.json()
                        print(confirmationData)
                        if confirmationData.get("Success") == True:
                            print(f"Confirmation successful for {name} on attempt {attempt + 1}")
                            print(f"Hostel gotten for {name} for {hall} hall!")
                            return {
                                "matricNo": matricNo,
                                "success": True,
                                "message": "Reservation and confirmation successful",
                                "reservation": reservationData,
                                "confirmation": confirmationData
                            }
                    time.sleep(0.1)  # Delay between retries for confirmation

                return {"matricNo": matricNo, "success": False, "message": "Failed to confirm accommodation after 50 attempts"}
        else:
            print(f"Login failed for {name}")
            return {"matricNo": matricNo, "success": False, "message": "Login failed or token not found"}
    else:
        print(f"Login request failed for {name}")
        return {"matricNo": matricNo, "success": False, "message": "Login request failed"}

def handleMultipleUsers(users):
    results = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(loginAndAccessAccommodation, user): user for user in users}
        for future in as_completed(futures):
            user = futures[future]
            try:
                result = future.result()
                results.append(result)
                print(f"Process completed for {user['name']}: {result}")
            except Exception as e:
                print(f"Error for user {user['name']}: {e}")
    return results

handleMultipleUsers(users)
