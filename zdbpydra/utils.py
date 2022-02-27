import json
import logging
import requests


def get_logger(name="zdbpydra", loglevel=None):
    logger = logging.getLogger(name)
    if not logger.handlers:
        stream = logging.StreamHandler()
        if loglevel is not None and loglevel != stream.level:
            stream.setLevel(loglevel)
        stream.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s", "%Y-%m-%d %H:%M:%S"))
        logger.addHandler(stream)
        if loglevel is not None and loglevel != logger.level:
            logger.setLevel(loglevel)
    else:
        if loglevel is not None and logger.level != loglevel:
            logger.setLevel(loglevel)
    return logger


def get_request(url, headers={}):
    if "User-Agent" not in headers:
        headers["User-Agent"] = "zdbpydra 0.0.0"
    try:
        return requests.get(url, headers=headers)
    except requests.exceptions.RequestException as err:
        logger = get_logger()
        logger.error(err.__class__.__name__)
        return None


def response_ok(response, loglevel=None):
    if response is None:
        return False
    if response.status_code == 200:
        return True
    else:
        logger = get_logger(loglevel=loglevel)
        logger.error("HTTP request to {0} failed!".format(response.url))
        logger.error("HTTP response code is {0}.".format(response.status_code))
        return False


def response_json(response):
    if response_ok(response):
        response = response.json()
        if response:
            return response


def json_request(url, headers={}):
    response = get_request(url, headers=headers)
    return response_json(response)


def json_str(data):
    return json.dumps(data, ensure_ascii=False)


def json_str_pretty(data):
    return json.dumps(data, ensure_ascii=False, indent=2)
