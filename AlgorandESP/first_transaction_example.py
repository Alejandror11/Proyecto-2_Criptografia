from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import transaction
from algosdk import constants
import json
import base64

#Conexión con el cliente

#Si usas PureStake

algod_client = algod.AlgodClient(
   algod_token="",
   algod_address="https://testnet-algorand.api.purestake.io/ps2",
   headers={"X-API-Key": "1gXkXLb7NUajpUivNCD1T6QRsdXaYuoA2tTVK4Cj"}
)

#Incluye la información de una de tus cuentas.
#Recuerda que los datos de la llave privada nunca deben estar en código
#Aquí lo hacemos para facilitar la explicación

my_address = "5TKAKOOFDXZYZVFMQ5ZPPROIUJT3UYLQQTUBPCDYWKMZNOPVSNP3XCAWZA"
private_key = mnemonic.to_private_key("slogan number extend agree hurry sibling fun pigeon test solar bottom coin swamp match disagree razor layer glimpse vault stone toast execute board absent shine")

#Verificando el balance de la cuenta

account_info = algod_client.account_info("5TKAKOOFDXZYZVFMQ5ZPPROIUJT3UYLQQTUBPCDYWKMZNOPVSNP3XCAWZA")
print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

# build transaction

params = algod_client.suggested_params()
# comment out the next two (2) lines to use suggested fees
params.flat_fee = True
params.fee = constants.MIN_TXN_FEE
receiver = "5TKAKOOFDXZYZVFMQ5ZPPROIUJT3UYLQQTUBPCDYWKMZNOPVSNP3XCAWZA"
note = "My first transaction".encode()
amount = 1000000
unsigned_txn = transaction.PaymentTxn(my_address, params, receiver, amount, None, note)

# sign transaction
signed_txn = unsigned_txn.sign(private_key)

#submit transaction
txid = algod_client.send_transaction(signed_txn)
print("Successfully sent transaction with txID: {}".format(txid))

# wait for confirmation
try:
    confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)
except Exception as err:
    print(err)


print("Transaction information: {}".format(json.dumps(confirmed_txn, indent=4)))
print("Decoded note: {}".format(base64.b64decode(confirmed_txn["txn"]["txn"]["note"]).decode()))
print("Starting Account balance: {} microAlgos".format(account_info.get('amount')))
print("Amount transfered: {} microAlgos".format(amount))
print("Fee: {} microAlgos".format(params.fee))

account_info = algod_client.account_info(my_address)
print("Final Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")