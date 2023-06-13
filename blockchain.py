import json
import base64
from algosdk.v2client import algod
from algosdk import account, mnemonic, encoding
from algosdk.transaction import *

class Blockchain:
    def __init__(self):
        # Iniciar cuentas con las direcciones
        addressProductor = "5TKAKOOFDXZYZVFMQ5ZPPROIUJT3UYLQQTUBPCDYWKMZNOPVSNP3XCAWZA"
        addressPointA = "MKA6TV22LKM34L4D64F6ICF34ECYWUILCW5E2VE6Y3KOSIBN34W232NNU4"
        addressPointB = "GMPUDHJVBZSR2Z3UDA4JPLPDN5O42W5GZJBECEEHMBOBHTIPMSYOODUMPY"
        addressPointC = "LPUAYVXAXWMM4ZIFO3L6RMQJ23CTGMFBHBYSOKFOLDM5ZQXGEYZNI7KF5Y"
        self.accounts = [addressProductor, addressPointA, addressPointB, addressPointC]

        # Obtenemos las llaves privadas usando mnemónicos
        mnemonicProdcutor = "slogan number extend agree hurry sibling fun pigeon test solar bottom coin swamp match disagree razor layer glimpse vault stone toast execute board absent shine"
        mnemonicPointA = "glare boost oblige pipe injury author renew mountain valid lobster into refuse favorite crop light wink motion quality sleep jar smooth electric innocent able cigar"
        mnemonicPointB = "shoulder party omit alley bus exotic agent history flame boring scissors loop must option market sock swim aerobic add easy chef gauge ghost abandon title"
        mnemonicPointC = "cheese danger matrix rebel believe broccoli glory island tissue dash road dune silk draw rather glow field muscle order typical betray fine across above tube"
        sk1 = "{}".format(mnemonic.to_private_key(mnemonicProdcutor))
        sk2 = "{}".format(mnemonic.to_private_key(mnemonicPointA))
        sk3 = "{}".format(mnemonic.to_private_key(mnemonicPointB))
        sk4 = "{}".format(mnemonic.to_private_key(mnemonicPointC))
        self.SKs = [sk1, sk2, sk3, sk4]

        #Conexión con el cliente con PureStake
        self.algod_client = algod.AlgodClient(
            algod_token="",
            algod_address="https://testnet-algorand.api.purestake.io/ps2",
            headers={"X-API-Key": "1gXkXLb7NUajpUivNCD1T6QRsdXaYuoA2tTVK4Cj"}
        )

    #  Función de utilidad para imprimir el activo creado para la cuenta y el assetid
    def print_created_asset(self, account, assetid):
        account_info = self.algodclient.account_info(account)
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
        account_info = self.algodclient.account_info(account)
        idx = 0
        for my_account_info in account_info['assets']:
            scrutinized_asset = account_info['assets'][idx]
            idx = idx + 1
            if (scrutinized_asset['asset-id'] == assetid):
                print("Asset ID: {}".format(scrutinized_asset['asset-id']))
                print(json.dumps(scrutinized_asset, indent=4))
                break

        print("Productor address: {}".format(self.accounts[0]))
        print("Point A address: {}".format(self.accounts[1]))
        print("Point B address: {}".format(self.accounts[2]))
        print("Point C address: {}".format(self.accounts[3]))

    def create_asset(self):
        params = self.algod_client.suggested_params()
        params.fee = 1000
        params.flat_fee = True

        txn = AssetConfigTxn(
            sender=self.accounts[0],
            sp=params,
            total=1000,
            default_frozen=False,
            unit_name="Ag",
            asset_name="Aguacate",
            manager=self.accounts[0],
            reserve=self.accounts[0],
            freeze=self.accounts[0],
            clawback=self.accounts[0],
            url="https://www.gob.mx/cms/uploads/attachment/file/257067/Potencial-Aguacate.pdf",
            decimals=0)
        stxn = txn.sign("{}".format(self.SKs[0]))

        try:
            txid = self.algod_client.send_transaction(stxn)
            print("Signed transaction with txID: {}".format(txid))
            confirmed_txn = wait_for_confirmation(self.algod_client, txid, 4)
            print("TXID: ", txid)
            print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))

        except Exception as err:
            print(err)

        print("Transaction information: {}".format(
            json.dumps(confirmed_txn, indent=4)))
        try:
            ptx = self.algod_client.pending_transaction_info(txid)
            asset_id = ptx["asset-index"]
            self.print_created_asset(self.algod_client, self.accounts[0], asset_id)
            self.print_asset_holding(self.algod_client, self.accounts[0], asset_id)
        except Exception as e:
            print(e)
    
    # Modificando un activo
    def modify_asset(self,asset_id):
        params = self.algod_client.suggested_params()

        txn = AssetConfigTxn(
            sender=self.accounts[1],
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