from rest_framework.decorators import api_view
from rest_framework.response import Response
from web3 import Web3
from django.conf import settings


@api_view(['POST'])
def create(request):
    return Response()

@api_view(['GET'])
def total_supply(request):
    provider_url = settings.PROVIDER_URL
    w3 = Web3(Web3.HTTPProvider(provider_url))
    address = settings.CONTRACT_ADDRESS
    abi = settings.CONTRACT_ABI
    contract_instance = w3.eth.contract(address=address, abi=abi)
    totalSupply = contract_instance.functions.totalSupply().call()
    response_data = {'totalSupply': totalSupply}
    return Response(response_data)    

@api_view(['GET'])
def list_tokens(request):
    return Response()