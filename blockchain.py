import json
import base64
from algosdk import mnemonic
from algosdk.v2client import algod
from algosdk.transaction import *

class Blockchain:
    def __init__(self):
        #Conexión con el cliente con PureStake
        self.algod_client = algod.AlgodClient(
            algod_token="",
            algod_address="https://testnet-algorand.api.purestake.io/ps2",
            headers={"X-API-Key": "1gXkXLb7NUajpUivNCD1T6QRsdXaYuoA2tTVK4Cj"}
        )

    #  Función de utilidad para imprimir el activo creado para la cuenta y el assetid
    def print_created_asset(self, account, assetid):
        account_info = self.algod_client.account_info(account)
        idx = 0;
        for my_account_info in account_info['created-assets']:
            scrutinized_asset = account_info['created-assets'][idx]
            idx = idx + 1
            if (scrutinized_asset['index'] == assetid):
                print("Asset ID: {}".format(scrutinized_asset['index']))
                print(json.dumps(my_account_info['params'], indent=4))
                break

    #Función de utilidad para imprimir la tenencia de activos para la cuenta y assetid
    def print_asset_holding(self, account, assetid):
        account_info = self.algod_client.account_info(account)
        idx = 0
        for my_account_info in account_info['assets']:
            scrutinized_asset = account_info['assets'][idx]
            idx = idx + 1
            if (scrutinized_asset['asset-id'] == assetid):
                print("Asset ID: {}".format(scrutinized_asset['asset-id']))
                print(json.dumps(scrutinized_asset, indent=4))
                print("\n")
                break

    # Función para crear un activo
    def create_asset(self,sender,skSender,total,unitName,assetName,manager,reserve,freeze,clawback,url):
        params = self.algod_client.suggested_params()
        params.fee = 1000
        params.flat_fee = True

        txn = AssetConfigTxn(
            sender=sender,
            sp=params,
            total=total,
            default_frozen=False,
            unit_name=unitName,
            asset_name=assetName,
            manager=manager,
            reserve=reserve,
            freeze=freeze,
            clawback=clawback,
            url=url,
            decimals=0)
        stxn = txn.sign("{}".format(skSender))

        try:
            txid = self.algod_client.send_transaction(stxn)
            print("Signed transaction with txID: {}".format(txid))
            confirmed_txn = wait_for_confirmation(self.algod_client, txid, 4)
            print("TXID: ", txid)
            print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))

        except Exception as err:
            print(err)
    
    # Modificando un activo
    def modify_asset(self,sender,skSender,asset_id,manager,reserve,freeze,clawback):
        params = self.algod_client.suggested_params()

        txn = AssetConfigTxn(
            sender=sender,
            sp=params,
            index=asset_id,
            manager=manager,
            reserve=reserve,
            freeze=freeze,
            clawback=clawback)
        stxn = txn.sign(skSender)

        try:
            txid = self.algod_client.send_transaction(stxn)
            print("Signed transaction with txID: {}".format(txid))
            confirmed_txn = wait_for_confirmation(self.algod_client, txid, 4)
            print("TXID: ", txid)
            print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))

        except Exception as err:
            print(err)

    # Función para optar por recibir un activo
    def opt_in(self,receiver,skReceiver,asset_id):
        params = self.algod_client.suggested_params()
        account_info = self.algod_client.account_info(receiver)
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
                sender=receiver,
                sp=params,
                receiver=receiver,
                amt=0,
                index=asset_id)
            stxn = txn.sign(skReceiver)

            try:
                txid = self.algod_client.send_transaction(stxn)
                print("Signed transaction with txID: {}".format(txid))
                confirmed_txn = wait_for_confirmation(self.algod_client, txid, 4)
                print("TXID: ", txid)
                print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))

            except Exception as err:
                print(err)

    # Transferir un activo
    def transfer_asset(self,sender,skSender,receiver,amt,asset_id):
        params = self.algod_client.suggested_params()

        txn = AssetTransferTxn(
            sender=sender,
            sp=params,
            receiver=receiver,
            amt=amt,
            index=asset_id)
        stxn = txn.sign(skSender)

        try:
            txid = self.algod_client.send_transaction(stxn)
            print("Signed transaction with txID: {}".format(txid))
            confirmed_txn = wait_for_confirmation(self.algod_client, txid, 4)
            print("TXID: ", txid)
            print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))

        except Exception as err:
            print(err)
    
    def transfer_asset_schema(self,sender,skSender,receiver,amt,asset_id,data):
        params = self.algod_client.suggested_params()
        certificate_note = json.dumps(data)
        txn = AssetTransferTxn(
            sender=sender,
            sp=params,
            receiver=receiver,
            amt=amt,
            index=asset_id,
            note=certificate_note.encode())
        stxn = txn.sign(skSender)

        try:
            txid = self.algod_client.send_transaction(stxn)
            print("Signed transaction with txID: {}".format(txid))
            confirmed_txn = wait_for_confirmation(self.algod_client, txid, 4)
            print("TXID: ", txid)
            print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))

        except Exception as err:
            print(err)

    # Congelar un activo
    def freeze_asset(self,sender,skSender,asset_id,target):
        params = self.algod_client.suggested_params()

        txn = AssetFreezeTxn(
            sender=sender,
            sp=params,
            index=asset_id,
            target=target,
            new_freeze_state=True
        )
        stxn = txn.sign(skSender)

        try:
            txid = self.algod_client.send_transaction(stxn)
            print("Signed transaction with txID: {}".format(txid))
            confirmed_txn = wait_for_confirmation(self.algod_client, txid, 4)
            print("TXID: ", txid)
            print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
        except Exception as err:
            print(err)

    # Revocar un activo
    def revocation_asset(self,sender,skSender,receiver,amt,asset_id,target):
        params = self.algod_client.suggested_params()
        txn = AssetTransferTxn(
            sender=sender,
            sp=params,
            receiver=receiver,
            amt=amt,
            index=asset_id,
            revocation_target=target
        )
        stxn = txn.sign(skSender)
        try:
            txid = self.algod_client.send_transaction(stxn)
            print("Signed transaction with txID: {}".format(txid))
            confirmed_txn = wait_for_confirmation(self.algod_client, txid, 4)
            print("TXID: ", txid)
            print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
        except Exception as err:
            print(err)

    # Destruir un activo
    def destroy_asset(self,sender,skSender,asset_id):
        params = self.algod_client.suggested_params()

        txn = AssetConfigTxn(
            sender=sender,
            sp=params,
            index=asset_id,
            strict_empty_address_check=False
            )

        stxn = txn.sign(skSender)

        try:
            txid = self.algod_client.send_transaction(stxn)
            print("Signed transaction with txID: {}".format(txid))
            confirmed_txn = wait_for_confirmation(self.algod_client, txid, 4)
            print("TXID: ", txid)
            print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
        except Exception as err:
            print(err)