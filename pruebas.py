import json
import time
import base64
import hashlib
from algosdk.v2client import algod
from algosdk import account, mnemonic, encoding, transaction
from algosdk.transaction import *

algod_client = algod.AlgodClient(
   algod_token="",
   algod_address="https://testnet-algorand.api.purestake.io/ps2",
   headers={"X-API-Key": "1gXkXLb7NUajpUivNCD1T6QRsdXaYuoA2tTVK4Cj"}
)

def load_account_from_mnemonic(mnemonic_phrase):
    private_key = mnemonic.to_private_key(mnemonic_phrase)
    return account.address_from_private_key(private_key)

def create_signed_transaction(sender, receiver, amount, note):
    params = algod_client.suggested_params()
    params.fee = 1000  # Adjust fee as needed
    params.flat_fee = True

    txn = transaction.PaymentTxn(sender, params, receiver, amount, None, note.encode())
    signed_txn = txn.sign(sender.sk)

    return signed_txn

def create_asset(sender, total_supply, asset_name, asset_unit, asset_url, certificate_schema):
    params = algod_client.suggested_params()
    params.fee = 1000  # Adjust fee as needed
    params.flat_fee = True

    certificate_schema_json = json.dumps(certificate_schema, sort_keys=True)
    metadata_hash = hashlib.sha256(certificate_schema_json.encode()).digest()

    asset = transaction.AssetConfigTxn(
        sender=sender,
        sp=params,
        total=total_supply,
        default_frozen=False,
        unit_name=asset_unit,
        asset_name=asset_name,
        manager=sender,
        reserve=sender,
        clawback=sender,
        url=asset_url,
        decimals=0,
        metadata_hash=metadata_hash,
        strict_empty_address_check=False,
    )

    signed_txn = asset.sign(sk)

    transaction_id = algod_client.send_transaction(signed_txn)

    return transaction_id


def create_product_certificate(sender, asset_id, product_id, certificate_data):
    params = algod_client.suggested_params()
    params.fee = 1000  # Adjust fee as needed
    params.flat_fee = True

    certificate = {
        "product_id": product_id,
        "data": certificate_data
    }

    certificate_note = json.dumps(certificate)

    asset_transfer = transaction.AssetTransferTxn(
        sender=sender,
        sp=params,
        receiver=sender,
        amt=0,
        index=235711358,
        note=certificate_note.encode()
    )

    signed_txn = asset_transfer.sign(sk)

    transaction_id = algod_client.send_transaction(signed_txn)

    return transaction_id


def create_transport_route(sender, route_name, waypoints):
    params = algod_client.suggested_params()
    params.fee = 1000  # Adjust fee as needed
    params.flat_fee = True

    route_note = {
        "route_name": route_name,
        "waypoints": waypoints
    }

    route_note_str = json.dumps(route_note)

    asset_transfer = transaction.AssetTransferTxn(
        sender=sender,
        sp=params,
        receiver=sender,
        amt=0,
        index=235711358,
        note=route_note_str.encode()
    )

    signed_txn = asset_transfer.sign(sk)

    transaction_id = algod_client.send_transaction(signed_txn)

    return transaction_id

def opt_in():
    asset_id = 235711358
    params = algod_client.suggested_params()
    params.fee = 1000
    params.flat_fee = True
    # Verificar si asset_id esta en la cuenta 3 antes del opt-in
    account_info = algod_client.account_info("MKA6TV22LKM34L4D64F6ICF34ECYWUILCW5E2VE6Y3KOSIBN34W232NNU4")
    holding = None
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1
        if (scrutinized_asset['asset-id'] == asset_id):
            holding = True
            break
    if not holding:
    # Usamos la clase AssetTransferTxn para transferir y realizar opt-in
        txn = AssetTransferTxn(
            sender="MKA6TV22LKM34L4D64F6ICF34ECYWUILCW5E2VE6Y3KOSIBN34W232NNU4",
            sp=params,
            receiver="MKA6TV22LKM34L4D64F6ICF34ECYWUILCW5E2VE6Y3KOSIBN34W232NNU4",
            amt=0,
            index=asset_id)
        stxn = txn.sign(sk1)
        # Se envia la transacción a la red
        try:
            txid = algod_client.send_transaction(stxn)
            print("Signed transaction with txID: {}".format(txid))
            confirmed_txn = wait_for_confirmation(algod_client, txid, 1)
            print("TXID: ", txid)
            print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))

        except Exception as err:
            print(err)
        # Verificamos que el activo pertenece a esta cuenta
        # Este debe mostrar balance de 0

def transfer_asset(sender, receiver_address, asset_id, amount, certificate_data):
    params = algod_client.suggested_params()
    params.fee = 1000  # Adjust fee as needed
    params.flat_fee = True

    receiver = receiver_address

    # Get asset info
    asset_info = algod_client.asset_info(235711358)

    # Check compliance with certificate
    certificate_note = json.dumps(certificate_data)
    asset_transfer = transaction.AssetTransferTxn(
        sender=sender,
        sp=params,
        receiver=receiver,
        amt=amount,
        index=235711358,
        note=certificate_note.encode()
    )

    # Add compliance condition
    signed_txn = asset_transfer.sign(sk)

    transaction_id = algod_client.send_transaction(signed_txn)

    return transaction_id

# Load sender's account
mnemonic_phrase = "slogan number extend agree hurry sibling fun pigeon test solar bottom coin swamp match disagree razor layer glimpse vault stone toast execute board absent shine"
mnemonic_phrase1 = "glare boost oblige pipe injury author renew mountain valid lobster into refuse favorite crop light wink motion quality sleep jar smooth electric innocent able cigar"
sender = load_account_from_mnemonic(mnemonic_phrase)
sk = "{}".format(mnemonic.to_private_key(mnemonic_phrase))
sk1 = "{}".format(mnemonic.to_private_key(mnemonic_phrase1))

# Create an asset with certificate schema
# total_supply = 1000000
# asset_name = "Food Asset"
# asset_unit = "FA"
# asset_url = "https://example.com/food_asset"

# certificate_schema = {
#     "certificate_type": "Food Safety",
#     "expiry_date": "2023-12-31",
#     "issuer": "Certification Authority"
# }

#asset_id = create_asset(sender, total_supply, asset_name, asset_unit, asset_url, certificate_schema)
asset_id="VLY2QSOS3AKLUAZU2DXZGEOR3644CZIBBCDB7MS2IETKTAX3LKPA"
print(f"Asset created with ID: {asset_id}")

# # Create a product certificate
# product_id = "Product123"
# certificate_data = {
#     "certificate_type": "Food Safety",
#     "expiry_date": "2023-12-31",
#     "issuer": "Certification Authority"
# }
# create_product_certificate(sender, asset_id, product_id, certificate_data)
# print("Product certificate created.")

# Define the transport route
route_name = "Route1"
# waypoints = ["Location A", "Location B", "Location C", "Location D"]

# # Create the transport route
# create_transport_route(sender, route_name, waypoints)
# print("Transport route created successfully.")

# Transfer the asset along with the product certificate using the defined route
receiver_address = "MKA6TV22LKM34L4D64F6ICF34ECYWUILCW5E2VE6Y3KOSIBN34W232NNU4"
amount = 100
certificate_data = {
    "certificate_type": "Food Safety",
    "expiry_date": "2023-12-31",
    "issuer": "Certification Authority",
    "transport_route": route_name
}
opt_in()
transfer_asset(sender, receiver_address, asset_id, amount, certificate_data)
print("Asset transferred successfully with product and route.")