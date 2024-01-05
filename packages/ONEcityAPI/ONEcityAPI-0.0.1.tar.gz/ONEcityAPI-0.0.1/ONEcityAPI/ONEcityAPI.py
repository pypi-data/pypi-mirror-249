import requests
import urllib3
from requests.exceptions import RequestException
from typing import Optional
import json

from ONEcityAPI import exceptions
from ONEcityAPI.consumption import Consumption
from ONEcityAPI.consumptions import Consumptions
from ONEcityAPI.customer import Customer
from ONEcityAPI.user import User

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def request_wrapper(
        method: str,
        url: str,
        *args,
        session: Optional[requests.Session] = None,
        exception: Exception,
        **kwargs,
) -> requests.models.Response:
    if session is None:
        session = requests.Session()
    try:
        response = session.request(method, url, *args, **kwargs)
        response.raise_for_status()
    except RequestException as e:
        raise exception from e
    return response


def extract_numbers(input_string):
    return int(''.join(filter(str.isdigit, input_string)))


class ONEcityAPI:
    ENDPOINT = 'https://city4u.co.il'

    def __init__(self, user: User):
        self._token = None
        self._user = user
        self._request_token()

    def _request_token(self):
        data = {
            'ServiceName': 'LoginUser',
            'UserName': self._user.userName,
            'Password': self._user.password,
            'customerID': self._user.customerID,
            'CustomerSite': self._user.customerID,
        }

        response = request_wrapper(
            "POST",
            f"{ONEcityAPI.ENDPOINT}/WebApiUsersManagement/v1/UsrManagements/LoginUser",
            data=data,
            exception=exceptions.RequestFailedException("Failed to get token"),
        )

        if response.status_code != 200:
            raise exceptions.RequestFailedException(
                f"Failed to get token. Response status code: {response.status_code}")

        self._token = json.loads(response.text)['UserToken']

    def _get_token(self):  # TODO - add token expiration check
        if self._token is None:
            self._request_token()
        return self._token

    def get_water_consumption(self):
        token = self._get_token()
        headers = {
            'token': token,
            'UserName': self._user.userName,
            'customerID': self._user.customerID,
        }

        response = request_wrapper(
            "GET",
            f"{ONEcityAPI.ENDPOINT}/WebApiCity4u/v1/WaterConsumption/ReadingMoneWater/{self._user.customerID}/{self._user.userName}",
            headers=headers,
            exception=exceptions.RequestFailedException("Failed to get water consumption"),
        )

        if response.status_code != 200:
            raise exceptions.RequestFailedException(
                f"Failed to get water consumption. Response status code: {response.status_code}")

        consumption_objects = [Consumption(**entry) for entry in json.loads(response.text)]
        return Consumptions(consumption_objects)

    def get_customer_info(self):
        token = self._get_token()
        headers = {
            'token': token,
            'UserName': self._user.userName,
            'customerID': self._user.customerID,
        }

        response = request_wrapper(
            "GET",
            f"{ONEcityAPI.ENDPOINT}/WebApiCity4u/v1/WaterConsumption/GetCustomerInquires?customerId={self._user.customerID}&meshalemIdentity={self._user.userName}&ownerIdentity={self._user.userName}",
            headers=headers,
            exception=exceptions.RequestFailedException("Failed to get customer info"),
        )

        if response.status_code != 200:
            raise exceptions.RequestFailedException(
                f"Failed to get customer info. Response status code: {response.status_code}")

        tarif_fields = [f'tarif{i}Field' for i in range(1, 7) if
                        f'tarif{i}Field' in json.loads(response.text)['mgi430n0ResponseGruraField'][0]]
        rates = [json.loads(response.text)['mgi430n0ResponseGruraField'][0][field] for field in tarif_fields]

        number_of_persons = extract_numbers(
            json.loads(response.text)['mgi430n0ResponseGruraField'][0]['teurMahutShimushField'])

        return Customer(number_of_persons, rates)
