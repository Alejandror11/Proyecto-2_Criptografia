import json
import base64
from algosdk.v2client import algod
from algosdk import account, mnemonic, encoding
from algosdk.transaction import *

# Aquí usamos mnemónicos que por seguridad no incluimos en el código

mnemonic1 = "mnemonic1"
mnemonic2 = "mnemonic2"
mnemonic3 = "mnemonic3"
address1 = "address1"
address2 = "address2"
address3 = "address3"

accounts = [address1, address2, address3]

# Obtenemos las llaves privadas usando mnemónicos

sk1 = "{}".format(mnemonic.to_private_key(mnemonic1))
sk2 = "{}".format(mnemonic.to_private_key(mnemonic2))
sk3 = "{}".format(mnemonic.to_private_key(mnemonic3))
SKs = [sk1, sk2, sk3]

#Conexión con el cliente

#Si usas PureStake

#algod_client = algod.AlgodClient(
#    algod_token="",
#    algod_address="https://testnet-algorand.api.purestake.io/ps2",
#    headers={"X-API-Key": "API KEY"}
#)

#Si usas AlgoNode

algod_client = algod.AlgodClient(
    algod_token="",
    algod_address="https://testnet-api.algonode.cloud",
    headers={"X-API-Key": ""}
)

#  Función de utilidad para imprimir el activo creado para la cuenta y el assetid

def print_created_asset(algodclient, account, assetid):
    account_info = algodclient.account_info(account)
    idx = 0;
    for my_account_info in account_info['created-assets']:
        scrutinized_asset = account_info['created-assets'][idx]
        idx = idx + 1
        if (scrutinized_asset['index'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['index']))
            print(json.dumps(my_account_info['params'], indent=4))
            break


#Función de utilidad para imprimir la tenencia de activos para la cuenta y assetid

def print_asset_holding(algodclient, account, assetid):
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1
        if (scrutinized_asset['asset-id'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['asset-id']))
            print(json.dumps(scrutinized_asset, indent=4))
            break

    print("Account 1 address: {}".format(accounts[0]))
    print("Account 2 address: {}".format(accounts[1]))
    print("Account 3 address: {}".format(accounts[2]))


# Crear un activo
# Obtener parámetros de red para transacciones antes de cada transacción.

params = algod_client.suggested_params()
params.fee = 1000
params.flat_fee = True

txn = AssetConfigTxn(
    sender=accounts[0],
    sp=params,
    total=1000,
    default_frozen=False,
    unit_name="MIMONEDA",
    asset_name="MiMoneda",
    manager=accounts[1],
    reserve=accounts[1],
    freeze=accounts[1],
    clawback=accounts[1],
    url="https://path/to/my/asset/details",
    decimals=0)
stxn = txn.sign("{}".format(SKs[0]))

try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))

except Exception as err:
    print(err)

print("Transaction information: {}".format(
    json.dumps(confirmed_txn, indent=4)))
try:
    ptx = algod_client.pending_transaction_info(txid)
    asset_id = ptx["asset-index"]
    print_created_asset(algod_client, accounts[0], asset_id)
    print_asset_holding(algod_client, accounts[0], asset_id)
except Exception as e:
    print(e)

# Modificando un activo

params = algod_client.suggested_params()

txn = AssetConfigTxn(
    sender=accounts[1],
    sp=params,
    index=asset_id,
    manager=accounts[0],
    reserve=accounts[1],
    freeze=accounts[1],
    clawback=accounts[1])
stxn = txn.sign(SKs[1])

try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))

except Exception as err:
    print(err)
print_created_asset(algod_client, accounts[0], asset_id)

# OPT-IN

params = algod_client.suggested_params()

account_info = algod_client.account_info(accounts[2])
holding = None
idx = 0
for my_account_info in account_info['assets']:
    scrutinized_asset = account_info['assets'][idx]
    idx = idx + 1
    if (scrutinized_asset['asset-id'] == asset_id):
        holding = True
        break

if not holding:

    txn = AssetTransferTxn(
        sender=accounts[2],
        sp=params,
        receiver=accounts[2],
        amt=0,
        index=asset_id)
    stxn = txn.sign(SKs[2])

    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))

    except Exception as err:
        print(err)
    print_asset_holding(algod_client, accounts[2], asset_id)

# Transferir un activo

params = algod_client.suggested_params()

txn = AssetTransferTxn(
    sender=accounts[0],
    sp=params,
    receiver=accounts[2],
    amt=10,
    index=asset_id)
stxn = txn.sign(SKs[0])

try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))

except Exception as err:
    print(err)

print_asset_holding(algod_client, accounts[2], asset_id)

# Congelar un activo

params = algod_client.suggested_params()

txn = AssetFreezeTxn(
    sender=accounts[1],
    sp=params,
    index=asset_id,
    target=accounts[2],
    new_freeze_state=True
)
stxn = txn.sign(SKs[1])

try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
except Exception as err:
    print(err)

print_asset_holding(algod_client, accounts[2], asset_id)

# Revocar un activo

params = algod_client.suggested_params()

txn = AssetTransferTxn(
    sender=accounts[1],
    sp=params,
    receiver=accounts[0],
    amt=10,
    index=asset_id,
    revocation_target=accounts[2]
)
stxn = txn.sign(SKs[1])

try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
except Exception as err:
    print(err)

print("Account 3")
print_asset_holding(algod_client, accounts[2], asset_id)

print("Account 1")
print_asset_holding(algod_client, accounts[0], asset_id)

# Destruir un activo

params = algod_client.suggested_params()

txn = AssetConfigTxn(
    sender=accounts[0],
    sp=params,
    index=asset_id,
    strict_empty_address_check=False
    )

stxn = txn.sign(SKs[0])

try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
except Exception as err:
    print(err)
try:
    print("Account 3 must do a transaction for an amount of 0, ")
    print("with a close_assets_to to the creator account, to clear it from its accountholdings")
    print("For Account 1, nothing should print after this as the asset is destroyed on the creator account")
    print_asset_holding(algod_client, accounts[0], asset_id)
    print_created_asset(algod_client, accounts[0], asset_id)

except Exception as e:
    print(e)