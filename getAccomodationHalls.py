import requests
def loginAndAccessAccommodation(matricNo, password):
    loginUrl = 'https://studentportalbeta.unilag.edu.ng/users/login'
    accomodationHallsUrl = 'https://studentportalbeta.unilag.edu.ng/accomodation/accomodationHalls'
    session = requests.Session()
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
          # Access accommodation halls information
          hallsResponse = session.get(accomodationHallsUrl, headers=headers)
          if hallsResponse.status_code == 200:
            print("Accommodation Halls:", hallsResponse.json())
          else:
            print("Failed to retrieve accommodation halls!")
        else:
          print("Token was not found!")
          return None
    else:
      print("Login Details are incorrect!")
      return None

loginAndAccessAccommodation('190805025', 'vonn2109')