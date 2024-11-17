import requests
def loginAndAccessAccommodation(matricNo, password, hall):
    # URLs for login and accommodation services
    loginUrl = 'https://studentportalbeta.unilag.edu.ng/users/login'
    accomodationChecksUrl = 'https://studentportalbeta.unilag.edu.ng/accomodation/accommodationChecks'
    accomodationReservationUrl = 'https://studentportalbeta.unilag.edu.ng/accomodation/saveAccommodationReservation'
    accomodationConfirmationUrl = 'https://studentportalbeta.unilag.edu.ng/accomodation/accomodationConfirmation'

    # Create a session object to persist login cookies
    session = requests.Session()

    # Step 1: Log in with provided credentials
    loginData = {
        'matricNo': matricNo,
        'password': password
    }
    
    response = session.post(loginUrl, data=loginData)
    
    # Check if login was successful and extract the token
    if response.status_code == 200:
      responseData = response.json()
      success = responseData.get("Success")
      token = responseData.get("Data", {}).get("Token")
      if success:
        print('login successful')
        if token:
          headers = {'Authorization': f'Bearer {token}'}

          # Access accommodation checks information
          checksResponse = session.get(accomodationChecksUrl, headers=headers)
          if checksResponse.status_code == 200:
              print("Accommodation Checks:", checksResponse.json())
          else:
              print("Failed to retrieve accommodation checks!")

          # Access accommodation reservation
          reservationData = {
            'HallId': hall  # Replace with actual data needed
          }
          reservationResponse = session.post(accomodationReservationUrl, headers=headers, data=reservationData)
          if reservationResponse.status_code == 200:
              print("Accommodation Reservation Successful:", reservationResponse.json())
          else:
              print("Failed to reserve accommodation!")

          # Access accommodation confirmation
          confirmationResponse = session.get(accomodationConfirmationUrl, headers=headers)
          if confirmationResponse.status_code == 200:
              print("Accommodation Confirmation:", confirmationResponse.json())
          else:
              print("Failed to retrieve accommodation confirmation!")
        else:
          print("Token was not found!")
          return None
    else:
      print("Login Details are incorrect!")
      return None

loginAndAccessAccommodation('190805025', 'vonn2109', 'JAJA')