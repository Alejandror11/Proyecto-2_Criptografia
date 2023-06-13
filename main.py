from blockchain import *

asset_id = 0
accounts = []
SKs = []

def initialize():
    global asset_id,accounts,SKs
    # Definir id del activo
    asset_id = 235711358
    # Iniciar cuentas con las direcciones
    addressProductor = "5TKAKOOFDXZYZVFMQ5ZPPROIUJT3UYLQQTUBPCDYWKMZNOPVSNP3XCAWZA"
    addressPointA = "MKA6TV22LKM34L4D64F6ICF34ECYWUILCW5E2VE6Y3KOSIBN34W232NNU4"
    addressPointB = "GMPUDHJVBZSR2Z3UDA4JPLPDN5O42W5GZJBECEEHMBOBHTIPMSYOODUMPY"
    addressPointC = "LPUAYVXAXWMM4ZIFO3L6RMQJ23CTGMFBHBYSOKFOLDM5ZQXGEYZNI7KF5Y"
    accounts = [addressProductor, addressPointA, addressPointB, addressPointC]
    # Obtenemos las llaves privadas usando mnemónicos
    mnemonicProdcutor = "slogan number extend agree hurry sibling fun pigeon test solar bottom coin swamp match disagree razor layer glimpse vault stone toast execute board absent shine"
    mnemonicPointA = "glare boost oblige pipe injury author renew mountain valid lobster into refuse favorite crop light wink motion quality sleep jar smooth electric innocent able cigar"
    mnemonicPointB = "shoulder party omit alley bus exotic agent history flame boring scissors loop must option market sock swim aerobic add easy chef gauge ghost abandon title"
    mnemonicPointC = "cheese danger matrix rebel believe broccoli glory island tissue dash road dune silk draw rather glow field muscle order typical betray fine across above tube"
    sk1 = "{}".format(mnemonic.to_private_key(mnemonicProdcutor))
    sk2 = "{}".format(mnemonic.to_private_key(mnemonicPointA))
    sk3 = "{}".format(mnemonic.to_private_key(mnemonicPointB))
    sk4 = "{}".format(mnemonic.to_private_key(mnemonicPointC))
    SKs = [sk1, sk2, sk3, sk4]

initialize()

bc = Blockchain()
bc.print_asset_holding(accounts[0], asset_id)
bc.print_created_asset(accounts[0], asset_id)