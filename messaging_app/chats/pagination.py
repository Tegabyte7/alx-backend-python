from rest_framework import PageNumberPagination
from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    """
    Custom pagination class for messages
    """
    page_size = 10 # Numbers of messages per page
    page_size_query = 'page_size' # Allow client to overwrite page
    max_page_size = 100 # Maximum limit per client request
    page_query_param = 'page' # Query parameter for page number

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })