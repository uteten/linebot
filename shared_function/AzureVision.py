from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import os
import sys
import time
import logging

"""
    Need
    env[COMPUTER_VISION_SUBSCRIPTION_KEY]
    env[COMPUTER_VISION_ENDPOINT]
"""


class AzureVision():
    def __init__(self):
        if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
            self.subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
        else:
            msg = "\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment.\n"
            print(msg)
            logging.info(msg)
            sys.exit()

        if 'COMPUTER_VISION_ENDPOINT' in os.environ:
            self.endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
        else:
            msg = "\nSet the COMPUTER_VISION_ENDPOINT environment.\n"
            print(msg)
            logging.info(msg)
            sys.exit()

    def image2textFromURL(self, image_url):
        logging.info("azureVision image2textFromURL")
        logging.info("azureVision aaa")
        computervision_client = ComputerVisionClient(
            self.endpoint,
            CognitiveServicesCredentials(self.subscription_key)
        )
        logging.info("azureVision bbb")
        logging.info("azureVision image2textFromURL-read")
        recognize_handw_results = computervision_client.read(image_url, raw=True)
        logging.info("azureVision read done")
        operation_location_remote = recognize_handw_results.headers["Operation-Location"]
        operation_id = operation_location_remote.split("/")[-1]
        while True:
            get_handw_text_results = computervision_client.get_read_result(operation_id)
            if get_handw_text_results.status not in ['NotStarted', 'running']:
                break
            time.sleep(1)

        lines = [" "]
        # Print the detected text, line by line
        if get_handw_text_results.status == OperationStatusCodes.succeeded:
            for text_result in get_handw_text_results.analyze_result.read_results:
                for line in text_result.lines:
                    lines.append(line.text)
        else:
            logging.info("AzureVision error")
        return ' '.join(lines)

    def image2text(self, image):
        logging.info("azureVision image2text")
        return ' '.join(self.image2lines(image))

    def image2lines(self, image):
        logging.info("azureVision image2line")
        computervision_client = ComputerVisionClient(
            self.endpoint,
            CognitiveServicesCredentials(self.subscription_key)
        )
        logging.info("azureVision read_in_stream")
        recognize_handw_results = computervision_client.read_in_stream(
            image, language='en', custom_headers=None, raw=True, callback=None)
        logging.info("azureVision read_in_stream done")
        # Get the operation location (URL with an ID at the end) from the response
        operation_location_remote = recognize_handw_results.headers["Operation-Location"]
        # Grab the ID from the URL
        operation_id = operation_location_remote.split("/")[-1]
        # Call the "GET" API and wait for it to retrieve the results
        while True:
            get_handw_text_results = computervision_client.get_read_result(operation_id)
            if get_handw_text_results.status not in ['NotStarted', 'running']:
                break
            time.sleep(1)
        lines = [" "]
        # Print the detected text, line by line
        if get_handw_text_results.status == OperationStatusCodes.succeeded:
            for text_result in get_handw_text_results.analyze_result.read_results:
                for line in text_result.lines:
                    lines.append(line.text)
        else:
            logging.info("AzureVision error")
        return lines
