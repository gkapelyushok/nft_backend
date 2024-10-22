from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def create(request):
    return Response()

@api_view(['GET'])
def total_supply(request):
    return Response()

@api_view(['GET'])
def list_tokens(request):
    return Response()