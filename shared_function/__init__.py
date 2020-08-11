import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('in main from shared_function')
    return func.HttpResponse(f"Hello abc")
