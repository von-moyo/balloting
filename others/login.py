import requests

def login(matricNo, password):
    loginUrl = 'https://studentportalbeta.unilag.edu.ng/users/login'
    loginData = {
        'matricNo': matricNo,
        'password': password
    }
    session = requests.Session()
    response = session.post(loginUrl, data=loginData)
    
    if response.status_code == 200:
        responseData = response.json()
        success = responseData.get("Success")
        message = responseData.get("Message")
        token = responseData.get("Data", {}).get("Token")
        
        if success:
            print("Success:", success)
            print("Message:", message)
            if token:
                print("Token retrieved:", token)
                return token
            else:
                print("Token was not found!")
                return None
        else:
            print("Login unsuccessful:", message)
            return None
    else:
        print("Login failed with status code:", response.status_code)
        return None

# Example usage
login('190805025', 'vonn2109')
