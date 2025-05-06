from __future__ import annotations
from typing import Optional


def base_response(data: Optional[dict | str] = None, success: bool = True):
    """
    The base_response function is a helper function that returns a dictionary with the following keys:
        success: A boolean indicating whether or not the request was successful.
        error: An optional string containing an error message if success is False.
        response: An optional object which will be returned as-is in the request's response.

    :param cls: Refer to the class that is being instantiated
    :param data:dict=None: Pass a dictonary to the response
    :param success:bool=False: Determine whether or not the response was a success
    :return: A dictionary with the keys:

    """
    return {success, data}
