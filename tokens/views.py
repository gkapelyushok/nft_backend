from rest_framework.decorators import api_view
from rest_framework.response import Response
from web3 import Web3
from django.conf import settings
from .models import Token
from .serializers import TokenSerializer
import random
import string
from .pagination import TokenPagination

@api_view(['POST'])
def create(request):
    owner = request.data.get('owner')
    media_url = request.data.get('media_url')
    unique_hash = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    token = Token.objects.create(
        owner=owner, 
        media_url=media_url, 
        unique_hash=unique_hash
    )
    token.save()
    w3, contract_instance = get_contract()
    private_key = settings.PRIVATE_KEY
    sender_address = w3.eth.account.from_key(private_key).address
    nonce = w3.eth.get_transaction_count(sender_address)
    gas_price = w3.eth.gas_price
    tx = contract_instance.functions.mint(owner, media_url, unique_hash).build_transaction({
        'from': sender_address,
        'nonce': nonce,
        'gas': 200000,
        'gasPrice': gas_price
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    w3.eth.wait_for_transaction_receipt(tx_hash)
    receipt = w3.eth.get_transaction_receipt(tx_hash)
    if receipt == 0:
        return Response("Transaction failed", status=400)
    token.tx_hash = w3.to_hex(tx_hash)
    token.save()
    serializer = TokenSerializer(token)
    return Response(serializer.data)

@api_view(['GET'])
def total_supply(request):
    _, contract_instance = get_contract()
    totalSupply = contract_instance.functions.totalSupply().call()
    response_data = {'totalSupply': totalSupply}
    return Response(response_data)    

@api_view(['GET'])
def list_tokens(request):
    tokens = Token.objects.all()
    paginator = TokenPagination()
    result_page = paginator.paginate_queryset(tokens, request)
    serializer = TokenSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)



def get_contract():
    provider_url = settings.PROVIDER_URL
    w3 = Web3(Web3.HTTPProvider(provider_url))
    address = settings.CONTRACT_ADDRESS
    abi = settings.CONTRACT_ABI
    return w3, w3.eth.contract(address=address, abi=abi)