import json
import requests
import logging
from requests.adapters import HTTPAdapter, Retry
from multipledispatch import dispatch
import traceback

class ProtectoVault:
    def __init__(self, auth_token, default_url="https://trial.protecto.ai/api/vault/"):
        self.auth_token = f"Bearer {auth_token}"
        self.default_url = default_url
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain',
           'Authorization': self.auth_token}

    @dispatch(list)
    def mask(self, data):
        # Implementation of mask logic - ML detection
        # This method will take data as input and mask it using the authkey and the base URL.
        # input format:
        # ["Gina lives in the U.S.A","George Washington is happy"]
        try:
            logging.info(f"started mask operation for data: {data}")
            input_data = list()
            for value in data:
                input_data.append({"value": "{}".format(value)})
            response = self.service_call(input_data, "mask", "mask")
            logging.info("retrieved masked data")
            return response
        except Exception as e :
            logging.error(f"Error in mask: {traceback.format_exc()}")
            return e

    @dispatch(dict)
    def mask(self,data):
        # Implementation of mask logic for input of type json
        # This method will take data as input and mask it using the authkey and the base URL.
        # input format:
        # {"mask": [{"value": "He lives in the U.S.A"},{"value": "Ram is in Lanka"}]}
        try:
            logging.info(f"started mask operation for data: {data}")
            response = self.service_call(data["mask"], "mask", "mask")
            logging.info("retrieved masked data")
            return response
        except Exception as e:
            logging.error(f"Error in mask: {traceback.format_exc()}")
            return e


    @dispatch(list,str,str)
    def mask(self, data, token_name, format):
        # Implement masking logic - given token_name and format
        # This method will take data as input and mask it using the authkey and the base URL.
        # input format:
        # (["1234-4567-7890"], "Text Token", "Credit Card")
        try:
            logging.info(f"started mask operation for data:{data}")
            input_data = list()
            for value in data:
                input_data.append({"value": "{}".format(value), "token_name": token_name, "format": format})
            response = self.service_call(input_data, "mask", "mask")
            logging.info("retrieved masked data")
            return response
        except Exception as e:
            logging.error(f"Error in mask: {traceback.format_exc()}")
            return e

    @dispatch(list,str)
    def mask(self, data, token_name):
        # Implementation of mask logic  - only token_name provided
        # This method will take data as input and mask it using the authkey and possibly the base URL.
        # input format:
        # (["Gina","Australia"], "Text Token")
        try:
            logging.info(f"started mask operation for data: {data}")
            input_data = list()
            for value in data:
                input_data.append({"value": "{}".format(value), "token_name": token_name})
            response = self.service_call(input_data, "mask", "mask")
            logging.info("retrieved masked data")
            return response
        except Exception as e:
            logging.error(f"Error in mask: {traceback.format_exc()}")
            return e

    @dispatch(list)
    def unmask(self, masked_data):
        # Implementation of unmask logic
        # This method will take masked data and unmask it using the authkey and possibly the base URL.
        # input format:
        # ["mTiygJz7Tf","<PER>mTiygJz7Tf</PER> lives in the <ADDRESS>oQLxg3gisk.G2jPUYZHcv.bHIrJ0Mb7k</ADDRESS>""]
        try:
            logging.info(f"started unmask operation for data: {masked_data}")
            input_data = list()
            for token in masked_data:
                input_data.append({"token_value": "{}".format(token)})
            response = self.service_call(input_data, "unmask", "unmask")
            logging.info("retrieved unmasked data")
            return response
        except Exception as e:
            logging.error(f"Error in unmask: {traceback.format_exc()}")
            return e

    def async_mask(self,data):
        # This method will take the input data to be masked in a json format and returns the tracking_id which in turn can be used to get the status if the request.
        # input format:
        # {"mask": [{"value": "Ram lives in the U.S.A"}]}
        try:
            logging.info(f"received async mask request for data: {data}")
            response = self.service_call(data["mask"], "mask", "mask/async")
            logging.info("submitted async request and retrieved tracking_id")
            return response
        except Exception as e:
            logging.error(f"Error in submitting async_mask request: {traceback.format_exc()}")
            return e

    def async_unmask(self,masked_data):
        # This method takes a list of data to be unmasked and returns the tracking_id which in turn can be used to get the status if the request.
        # input format:
        # ["mTiygJz7Tf","<PER>mTiygJz7Tf</PER> lives in the <ADDRESS>oQLxg3gisk.G2jPUYZHcv.bHIrJ0Mb7k</ADDRESS>""]
        try:
            logging.info(f"received async unmask request for data: {masked_data}")
            input_data = list()
            for token in masked_data:
                input_data.append({"token_value": "{}".format(token)})
            response = self.service_call(input_data, "unmask", "unmask/async")
            logging.info("submitted async request and retrieved tracking_id")
            return response
        except Exception as e:
            logging.error(f"Error in submitting async_unmask request: {traceback.format_exc()}")
            return e

    def async_status(self,tracking_id_list):
        # This method will return the status of async mask/unmask requests based on the provided tracking_id.
        # input format:
        # ["9f178448-fe87-44c1-b2b3-80d6277ca6b028122023141605","055089d7-6fab-4c3a-9219-17c3420be6c628122023142250"]
        try:
            logging.info(f"started async status operation for tracking_id: {tracking_id_list}")
            input_data = list()
            for tracking_id in tracking_id_list:
                input_data.append({"tracking_id": "{}".format(tracking_id)})
            response = self.service_call(input_data, "status", "async-status")
            logging.info("retrieved status of requests")
            return response
        except Exception as e:
            logging.error(f"Error in retrieving status of async request: {traceback.format_exc()}")
            return e

    def service_call(self,data, key, path):
        response = self.submit_request({key: data}, path)
        return response.json()

    def submit_request(self,input_data, path):
        session = self.get_session()
        response = session.put("{}{}".format(self.default_url, path), data=json.dumps(input_data), headers=self.headers)
        return response

    def get_session(self):
        session = requests.Session()
        retries = Retry(total=3,
                        backoff_factor=0.2,
                        status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        session.mount(self.default_url, adapter)
        return session

