import os
from acp_plugin_gamesdk.acp_plugin import AcpToken
import requests
from eth_keys import keys
from eth_utils import keccak
import json

token = os.environ.get("ACP_TOKEN_BUYER")
acp_token_client = AcpToken(
    token,
    "https://base-sepolia-rpc.publicnode.com/"
)
web3 = acp_token_client.web3

# Sender private key
account = web3.eth.account.from_key(token)
sender = account.address

# Construct unsigned transaction
encoded_data = acp_token_client.contract.encode_abi("memoCounter", args=[])

trx_data = {
    "target": acp_token_client.get_contract_address(),
    "value": 0,
    "data": encoded_data
}
message_hash = keccak(json.dumps(trx_data, sort_keys=False).encode())

# Sign the transaction
print("private_key:", token)
private_key = keys.PrivateKey(bytes.fromhex(token[2:]))
signature = private_key.sign_msg_hash(message_hash)
payload = {
    "agentWallet": "0x895dab20e8C52cEa7D03F3cEef38536f8edB8e74",
    "trxData": trx_data,
    "signature": signature.to_hex()
}

# Submit to custom API
api_url = "https://acpx.virtuals.gg/api/acp-agent-wallets/transactions"
response = requests.post(api_url, json=payload)
print("✅ Payload sent!")
print("Status:", response.status_code)
print("Response:", response.json())