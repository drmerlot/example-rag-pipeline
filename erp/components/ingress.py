import logging
from starlette.requests import Request


logger = logging.getLogger("ray.serve")


class Ingress:
    """Ingress parent class

    Parent class for any main task deployments
    created in the deployments. Sharing the parent
    class keeps the logic dealing with request/response
    paradigm cleaner.

    Note:
        Ingress assumes request is parsable as a dict
        with request option as 'option' key
    """

    async def ingress(self, request: Request) -> dict:
        """Ingress method that parses http input for server requests

        Args:
            request (startlet.Request): HTTP request to parse

        Returns:
            Dict of request for single image services
        """
        request = await request.json()
        self.validator(request)
        return request

    def validator(self, request: dict):
        """validates the request

        Args:
            request (dict): list of dics from request

        Raises:
            TypeError: when input is not a dict
        """
        # check input type
        if type(request) is not dict:
            raise ValueError('Request is not parsable as type dict')
        else:
            pass

        # check image exists
        if request['option'] is None:
            raise ValueError('No option specified')
        else:
            pass
