import requests
import json
from fairlib.core.interfaces.tools import AbstractTool

class HotelTool(AbstractTool):
    name = "hotel_search_tool"
    description = (
        "A tool for finding hotels."
        "Inputs must follow the exact format of the examples"
        "Example inputs:\n"
        '{"cityCode": "PAR", "ratings": "3,4,5", "adults": "2", "checkInDate": "2025-11-05", "checkOutDate": "2025-11-10", "priceRange": "200-300"}\n'
    )

    def use(self, expression: str) -> str:
        expression = expression.upper()
        user_specs_obj = json.loads(expression)
        hotel_list = self.list_hotels(user_specs_obj)
        hotelIDs = [hotel["hotelId"] for hotel in hotel_list["data"]]
        hotels = self.search_hotels(user_specs_obj, hotelIDs)
        return hotels

    def get_auth_token(self):
        base_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        api_key = {
            "grant_type":"client_credentials",
            "client_id":"Wfu8DWyUjgHDfzjzOwXDJLZb6THWv9iZ",
            "client_secret":"xMnzA2dQP4o5GsCE"
        }

        response = requests.post(base_url, headers=headers, data=api_key).json()
        token = response["access_token"]
        return token
    
    def list_hotels(self, hotelInfo):
        base_url = "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city"
        
        # Gather user input
        cityCode = hotelInfo["CITY"].strip().upper()
        ratings = hotelInfo["RATINGS"].strip().upper()

        # Optional: you could also let users specify returnDate, adults, etc.
        params = {
            "cityCode": cityCode,
            "ratings": ratings
        }

        # Replace this with your real token
        token = self.get_auth_token()
        headers = {
            "Authorization": "Bearer " + token
        }

        try:
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            return json.dumps(data)
        
        except requests.exceptions.RequestException as e:
            return(f"API request failed: {e}")

    def search_hotels(self, hotelInfo, hotelIDs):
        base_url = "https://test.api.amadeus.com/v3/shopping/hotel-offers"
        
        # Gather user input
        hotel_ids = ",".join(hotelIDs)
        adults = hotelInfo["ADULTS"].strip()
        checkInDate = hotelInfo["CHECKIN"].strip()
        checkOutDate = hotelInfo["CHECKOUT"].strip()
        priceRange = hotelInfo["PRICE"].strip()

        # Optional: you could also let users specify returnDate, adults, etc.
        params = {
            "hotelIds": hotel_ids,
            "adults": adults,
            "checkInDate": checkInDate,
            "checkOutDate": checkOutDate,
            "priceRange": priceRange,
            "currency": "USD"
        }

        # Replace this with your real token
        token = self.get_auth_token()
        headers = {
            "Authorization": "Bearer " + token
        }

        try:
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            return json.dumps(data)
        except requests.exceptions.RequestException as e:
            return(f"API request failed: {e}")


tool = HotelTool()
out = tool.use('{"cityCode": "PAR", "ratings": "3,4,5", "adults": "2", "checkInDate": "2025-11-05", "checkOutDate": "2025-11-10", "priceRange": "200-300"}\n')
print(out)