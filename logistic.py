from datetime import datetime
from blockchain import *

class Logistic:
    def __init__(self):
        # Definir id del activo
        self.asset = [238629010]
        # Iniciar cuentas con las direcciones
        addressProductor = "5TKAKOOFDXZYZVFMQ5ZPPROIUJT3UYLQQTUBPCDYWKMZNOPVSNP3XCAWZA"
        addressAuthority = "MQBCADL5BST4WNBSMKOT4TS6HAZNMMTNK2PREHRNVEJDDHLJ7L26GPRHLE"
        addressPointA = "MKA6TV22LKM34L4D64F6ICF34ECYWUILCW5E2VE6Y3KOSIBN34W232NNU4"
        addressPointB = "GMPUDHJVBZSR2Z3UDA4JPLPDN5O42W5GZJBECEEHMBOBHTIPMSYOODUMPY"
        addressPointC = "LPUAYVXAXWMM4ZIFO3L6RMQJ23CTGMFBHBYSOKFOLDM5ZQXGEYZNI7KF5Y"
        self.accounts = [addressProductor, addressAuthority, addressPointA, addressPointB, addressPointC]
        # Obtenemos las llaves privadas usando mnemónicos
        mnemonicProdcutor = "slogan number extend agree hurry sibling fun pigeon test solar bottom coin swamp match disagree razor layer glimpse vault stone toast execute board absent shine"
        mnemonicAuthority = "sport between rookie ability still decline damp narrow craft future gesture clump cereal manual place strategy matter legal relax bid electric essence sketch about supply"
        mnemonicPointA = "glare boost oblige pipe injury author renew mountain valid lobster into refuse favorite crop light wink motion quality sleep jar smooth electric innocent able cigar"
        mnemonicPointB = "shoulder party omit alley bus exotic agent history flame boring scissors loop must option market sock swim aerobic add easy chef gauge ghost abandon title"
        mnemonicPointC = "cheese danger matrix rebel believe broccoli glory island tissue dash road dune silk draw rather glow field muscle order typical betray fine across above tube"
        sk1 = "{}".format(mnemonic.to_private_key(mnemonicProdcutor))
        sk2 = "{}".format(mnemonic.to_private_key(mnemonicAuthority))
        sk3 = "{}".format(mnemonic.to_private_key(mnemonicPointA))
        sk4 = "{}".format(mnemonic.to_private_key(mnemonicPointB))
        sk5 = "{}".format(mnemonic.to_private_key(mnemonicPointC))
        self.SKs = [sk1, sk2, sk3, sk4, sk5]
        self.bc = Blockchain()
        self.directory ={"5TKAKOOFDXZYZVFMQ5ZPPROIUJT3UYLQQTUBPCDYWKMZNOPVSNP3XCAWZA":"México",
                         "MQBCADL5BST4WNBSMKOT4TS6HAZNMMTNK2PREHRNVEJDDHLJ7L26GPRHLE":"Autoridad Certificadora",
                         "MKA6TV22LKM34L4D64F6ICF34ECYWUILCW5E2VE6Y3KOSIBN34W232NNU4":"Estados Unidos",
                         "GMPUDHJVBZSR2Z3UDA4JPLPDN5O42W5GZJBECEEHMBOBHTIPMSYOODUMPY":"China",
                         "LPUAYVXAXWMM4ZIFO3L6RMQJ23CTGMFBHBYSOKFOLDM5ZQXGEYZNI7KF5Y":"Canada",
                         238629010:"Aguacate",
                         238629010:"Tomate",
                         238629010:"Pimiento"}

    def create_product(self,total,unitName,assetName,url):
        self.bc.create_asset(self.accounts[0],self.SKs[0],total,unitName,assetName,self.accounts[0],self.accounts[0],self.accounts[1],self.accounts[0],url)
    
    def accept_product_network(self,asset_id):
        for i in range(1 ,len(self.accounts)):
            self.bc.opt_in(self.accounts[i],self.SKs[i],asset_id)

    def show_product_holding_network(self,asset_id):
        for i in range(0 ,len(self.accounts)):
            self.bc.print_asset_holding(self.accounts[i],asset_id)
    
    def transfer_product(self,sender,skSender,receiver,amt,asset_id):
        self.bc.transfer_asset(sender,skSender,receiver,amt,asset_id)
        print("Producto enviado de {} correctamente a {}".format(self.directory[sender],self.directory[receiver]))
    
    def transfer_producto_verify(self,sender,skSender,receiver,amt,asset_id,data):
        self.transfer_product(sender,skSender,self.accounts[1],amt,asset_id)
        enviar = False
        if self.directory[asset_id] == "Aguacate":
            date_end = datetime.strptime(data["Fecha_Embalaje"], "%Y-%m-%d")
            date_start = datetime.strptime(data["Fecha_Cosecha"], "%Y-%m-%d")
            gap =date_end-date_start
            msj = ""
            if gap.days < 30 and data["Tipo_Certificado"] == "NOM-066-FITO-2002":
                enviar = True
            else:
                msj += """El producto Aguacate no cumple con las siguientes condiciones para exportar:
                El tiempo entre la cosecha y el embalaje no debe ser mayor a 30 días
                El certificado del prodcuto no sigue las normas de NOM-066-FITO-2002
                Revise nuevamente las condiciones de su producto para exportar"""
        elif self.directory[asset_id] == "Tomate":
            date_end = datetime.strptime(data["Fecha_Embalaje"], "%Y-%m-%d")
            date_start = datetime.strptime(data["Fecha_Cosecha"], "%Y-%m-%d")
            gap =date_end-date_start
            msj = ""
            if gap.days < 20 and data["Tipo_Certificado"] == "NOM-650-FITO-2006":
                enviar = True
            else:
                msj += """El producto Tomate no cumple con las siguientes condiciones para exportar:
                El tiempo entre la cosecha y el embalaje no debe ser mayor a 20 días
                El certificado del prodcuto no sigue las normas de NOM-650-FITO-2006
                Revise nuevamente las condiciones de su producto para exportar"""
        elif self.directory[asset_id] == "Pimiento":
            date_end = datetime.strptime(data["Fecha_Embalaje"], "%Y-%m-%d")
            date_start = datetime.strptime(data["Fecha_Cosecha"], "%Y-%m-%d")
            gap =date_end-date_start
            msj = ""
            if gap.days < 90 and data["Tipo_Certificado"] == "NOM-250-FITO-2004":
                enviar = True
            else:
                msj += """El producto Tomate no cumple con las siguientes condiciones para exportar:
                El tiempo entre la cosecha y el embalaje no debe ser mayor a 90 días
                El certificado del prodcuto no sigue las normas de NOM-250-FITO-2004
                Revise nuevamente las condiciones de su producto para exportar"""
        else:
            print("El producto no es uno que nosotros como entidad podamos validar")
        if enviar == True:
            self.bc.transfer_asset_schema(sender,skSender,receiver,amt,asset_id,data)
            print("Producto exportado de {} correctamente a {}".format(self.directory[sender],self.directory[receiver]))
        else:
            self.transfer_product(self.accounts[1],self.SKs[1],sender,amt,asset_id)
            print(msj)

    def freeze_product(self,sender,skSender,asset_id,target):
        self.bc.freeze_asset(sender,skSender,asset_id,target)
        print("Se han congelado el producto {} en el país {} debido a irregularidades detectadas".format(self.dictionary[asset_id],self.directory[target]))
