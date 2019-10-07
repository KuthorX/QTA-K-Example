# -*- coding: utf-8 -*-


def request_get(url, headers=None, proxies=None, if_print_curl_str=True, test_case=None):
    """
    GET request
    :param url:
    :param headers:
    :param proxies: e.g. {"http": "http://127.0.0.1:80", "https": "http://127.0.0.1:80"}
    :param if_print_curl_str: if print linux-curl-str
    :param test_case: QTA TestCase
    :return: http_code, response_text, exception
    """
    if headers is None:
        headers = {}
    if proxies is None:
        proxies = {"http": "", "https": ""}

    if if_print_curl_str:
        curl_headers_str = ""
        for k, v in headers.items():
            curl_headers_str += " -H \"%s: %s\" " % (k, v)
        curl_str = """curl -v \"%s\" %s""" % (url, curl_headers_str)
        print(curl_str)
        if test_case:
            test_case.log_info(curl_str)

    import requests
    exception = None
    try:
        r = requests.get(url, headers=headers, proxies=proxies)
    except Exception as err:
        return -1, "", str(err)
    return r.status_code, r.text, exception


def request_post(url, headers=None, post_data=None, proxies=None, if_print_curl_str=True, test_case=None):
    """
    POST request
    :param url:
    :param headers:
    :param post_data:
    :param proxies: e.g. {"http": "http://127.0.0.1:80", "https": "http://127.0.0.1:80"}
    :param if_print_curl_str: if print linux-curl-str
    :param test_case: QTA TestCase
    :return: http_code, response_text, exception
    """
    if headers is None:
        headers = {}
    if post_data is None:
        post_data = {}
    if proxies is None:
        proxies = {"http": "", "https": ""}

    if if_print_curl_str:
        import json
        curl_headers_str = ""
        for k, v in headers.items():
            curl_headers_str += " -H \"%s: %s\" " % (k, v)
        curl_str = """curl -v \"%s\" %s -d '%s'""" % (url, curl_headers_str, json.dumps(post_data))
        print(curl_str)
        if test_case:
            test_case.log_info(curl_str)

    import requests
    exception = None
    try:
        r = requests.post(url, data=post_data, headers=headers, proxies=proxies)
    except Exception as err:
        return -1, "", str(err)
    return r.status_code, r.text, exception


def add_uuid(url, k="uuid", s="&"):
    """
    append uuid to url params
    :param url:
    :param k:
    :param s:
    :return: appended url
    """
    import uuid
    u = uuid.uuid4()
    return "%s%s%s=%s" % (url, s, k, u)

