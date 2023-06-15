from logistic import * 

logistic = Logistic()

def imprimir_productos():
    msj = ""
    for i in range(0, len(logistic.asset)):
        msj += str(i+1)
        msj += ": ID="
        msj += str(logistic.asset[i])
        msj += ", ->"
        msj += logistic.directory[logistic.asset[i]]
        if i < len(logistic.asset)-1:
            msj += "\n"

    print(msj)

def imprimir_destinos():
    print("*Estados Unidos")
    print("*China")
    print("*Canada")

def imprimir_tipo_certificado():
    print("1. NOM-066-FITO-2002")
    print("2. NOM-650-FITO-2006")
    print("3. NOM-250-FITO-2004")

def ingresa_verifica_datos_O1():
    bandera = False
    cantidad = 0
    while bandera == False:
        cantidad = input("Ingresa la cantidad total del producto")
        if cantidad.isdigit():
            bandera = True
    
    bandera = False
    unitName = ""
    while bandera == False:
        unitName = input("Ingresa el nombre de la unidad del producto")
        if unitName.isalpha():
            bandera = True
    
    bandera = False
    assetName = ""
    while bandera == False:
        assetName = input("Ingresa el nombre del producto")
        if assetName.isalpha():
            bandera = True
    
    url = input("Ingresa un url con información del producto")
    
    return cantidad, unitName, assetName, url

def ingresa_verifica_datos_O2():
    imprimir_productos()
    asset_id = 0
    bandera = False
    while bandera == False:
        asset_id = input("Ingresa el id del Producto")
        if asset_id.isdigit():
            for i in range(0, len(logistic.asset)):
                if logistic.asset[i] == asset_id:
                    bandera = True
                    break
                else:
                    print("El ID del producto no coincide con los mostrados. Intente otra vez")
        else:
            print("No se ingresó un número como ID")
    
    return asset_id

def ingresa_verifica_datos_O3():
    imprimir_productos()
    asset_id = 0
    bandera = False
    while bandera == False:
        asset_id = input("Ingresa el id del Producto")
        if asset_id.isdigit():
            for i in range(0, len(logistic.asset)):
                if logistic.asset[i] == asset_id:
                    bandera = True
                    break
                else:
                    print("El ID del producto no coincide con los mostrados. Intente otra vez")
        else:
            print("No se ingresó un número como ID. Intente otra vez")

    sender = logistic.accounts[0]
    skSender = logistic.SKs[0]

    imprimir_destinos()
    addressReceiver = ""
    bandera = False
    while bandera == False:
        receiver = input("Ingresa el nombre de uno de los tres destinos mostrados")
        if receiver.isalpha():
            for c, r in logistic.directory.items():
                if receiver == r:
                    addressReceiver = c
                    bandera = True
                    break
                else:
                    print("El nombre del prodcuto no coincide con los mostrados. Intente otra vez")
        else:
            print("No se ingresó un nombre en formato de texto. Intente otra vez")

    amt = 0
    bandera = False
    while bandera ==False:
        amt = input("Ingresa el total de producto a transferir")
        if amt.isdigit():
            bandera = True
        else:
            print("No se ingresó un número como monto")

    data = {
        "Tipo_Certificado": "",
        "Fecha_Cosecha": "",
        "Fecha_Embalaje": "",
    }

    imprimir_tipo_certificado()
    tipo_certificado = 0
    bandera = False
    while bandera == False:
        tipo_certificado = input("Ingresar la opción del certificado que cumple su producto")
        if tipo_certificado.isdigit():
            if tipo_certificado == "1" or tipo_certificado == "2" or tipo_certificado == "3":
                if tipo_certificado == "1":
                    tipo_certificado = "NOM-066-FITO-2002"
                elif tipo_certificado == "2":
                    tipo_certificado = "NOM-650-FITO-2006"
                else:
                    tipo_certificado = "NOM-250-FITO-2004"
                bandera=True
            else:
                print("No se ingresó una opción válida")
        else:
            print("No se ingresó un número como opción")
    
    fecha_cosecha = ""
    bandera = False
    while bandera == False:
        fecha_cosecha = input("Ingresa la fecha de cosecha del producto (formato AAAA-MM-DD): ")
        try:
            fecha = datetime.strptime(fecha_cosecha, "%Y-%m-%d")
            bandera = True
        except ValueError:
            print("La fecha ingresada no cumple con el formato AAAA-MM-DD.")

    fecha_embalaje = ""
    bandera = False
    while bandera == False:
        fecha_embalaje = input("Ingresa la fecha de embalaje del producto (formato AAAA-MM-DD): ")
        try:
            fecha = datetime.strptime(fecha_embalaje, "%Y-%m-%d")
            bandera = True
        except ValueError:
            print("La fecha ingresada no cumple con el formato AAAA-MM-DD.")

    data["Tipo_Certificado"] = tipo_certificado
    data["Fecha_Cosecha"] = fecha_cosecha
    data["Fecha_Embalaje"] = fecha_embalaje
    
    return sender, skSender, addressReceiver, amt, asset_id, data

def ingresa_verifica_datos_O4():
    imprimir_productos()
    asset_id = 0
    bandera = False
    while bandera == False:
        asset_id = input("Ingresa el id del Producto")
        if asset_id.isdigit():
            for i in range(0, len(logistic.asset)):
                if logistic.asset[i] == asset_id:
                    bandera = True
                    break
                else:
                    print("El ID del producto no coincide con los mostrados. Intente otra vez")
        else:
            print("No se ingresó un número como ID")
    
    return asset_id

def ingresa_verifica_datos_O5():
    sender = logistic.accounts[1]
    skSender = logistic.SKs[1]

    imprimir_productos()
    asset_id = 0
    bandera = False
    while bandera == False:
        asset_id = input("Ingresa el id del Producto")
        if asset_id.isdigit():
            for i in range(0, len(logistic.asset)):
                if logistic.asset[i] == asset_id:
                    bandera = True
                    break
                else:
                    print("El ID del producto no coincide con los mostrados. Intente otra vez")
        else:
            print("No se ingresó un número como ID")
        
    
    imprimir_destinos()
    addressTarget = ""
    bandera = False
    while bandera == False:
        receiver = input("Ingresa el nombre de uno de los tres destinos como objetivo")
        if receiver.isalpha():
            for c, r in logistic.directory.items():
                if receiver == r:
                    addressTarget = c
                    bandera = True
                    break
                else:
                    print("El nombre del prodcuto no coincide con los mostrados. Intente otra vez")
        else:
            print("No se ingresó un nombre en formato de texto. Intente otra vez")
    
    return sender, skSender, asset_id, addressTarget
    
def main():
    while True:
        print("""\nSelecciona una opción del menú:
        1. Crear un producto para exportar
        2. Permitir que todos los implicados puedan aceptar el producto
        3. Enviar producto para verificar y exportar
        4. Verificar la tenencia de producto en la red
        5. Congelar producto
        6. Salir""")

        opcion = input("Opción seleccionada: ")
        
        # Realiza una acción en función de la opción seleccionada
        if opcion == "1":
            print("Ha seleccionado la opción 1")
            cantidad,unitName,assetName,url = ingresa_verifica_datos_O1()
            logistic.create_product(cantidad,unitName,assetName,url)
        elif opcion == "2":
            print("Ha seleccionado la opción 2")
            asset_id = ingresa_verifica_datos_O2()
            logistic.accept_product_network(asset_id)
        elif opcion == "3":
            print("Ha seleccionado la opción 3")
            sender,skSender,receiver,amt,asset_id,data = ingresa_verifica_datos_O3()
            logistic.transfer_producto_verify(sender,skSender,receiver,amt,asset_id,data)
        elif opcion == "4":
            print("Ha seleccionado la opción 4")
            asset_id = ingresa_verifica_datos_O4()
            logistic.show_product_holding_network(asset_id)
        elif opcion == "5":
            print("Ha seleccionado la opción 5")
            sender,skSender,asset_id,target=ingresa_verifica_datos_O5()
            logistic.freeze_product(sender,skSender,asset_id,target)
        elif opcion == "6":
            print("Saliendo del programa...")
            break  # Sale del bucle while
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()