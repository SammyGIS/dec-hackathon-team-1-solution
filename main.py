#************************************************************************
# Authors:
# Date:
#************************************************************************
import requests

restcountries_url = "https://restcountries.com/v3.1/all"


def get_data(url: str) -> dict:
    # Send a GET request to the specified URL
    request = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if request.status_code == 200:
        # Parse the response content as JSON
        response = request.json()
        # Return the parsed JSON data
        return response
    else:
        # If the request was not successful, return an error message
        return 'Error fetching data'


