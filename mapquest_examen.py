import urllib.parse
import requests
import time
from googletrans import Translator

    
main_api = "https://www.mapquestapi.com/directions/v2/route?"
clave = "jIrfimfkdRAWr3d0s05Q5nb9NvKXMl80"

translator = Translator()
average_fuel_efficiency = 25

fecha_actual = time.strftime("%Y-%m-%d")
hora_actual = time.strftime("%H:%M:%S")

print ("****************************************")
print ("Hola Bienvenido al Calculador de ruta")
print ("La Fecha de Hoy Es:" + fecha_actual )
print ("La Hora Actual es: " + hora_actual)
print ("Porfavor Ingresa los Datos Solicitados a Continuacion")
print ("****************************************")


while True:

    orig = input("Localizacion Actual: ")
    if orig == "S" or orig == "S" :
        break
    
    dest = input("Destino: ")
    if dest == "S" or dest == "S" :
        break



    url = main_api + urllib.parse.urlencode ({"key" : clave , "from" : orig , "to" : dest }) 

    json_data = requests.get (url) .json ()

    print ("URL: " + (url))

    json_data = requests.get (url).json()
    json_status = json_data ["info"] ["statuscode"]

    if json_status == 0:
        print("API Status: " + str(json_status) + " = A successful route call.\n")
        print("==================================================================")
        print("Direccion Desde : " + (orig) + " a : " + (dest))
        print("Duracion del Viaje: " + (json_data["route"]["formattedTime"]))
        print("Kilometros: " + str ("{:.1f}" .format((json_data ["route"]["distance"])*1.61)))

# Estimación del combustible utilizado
        if "fuelUsed" in json_data["route"]:
            fuel_used = json_data["route"]["fuelUsed"]
            print("Combustible utilizado (Ltr): " + str("{:.1f}".format(fuel_used * 3.78)))
        else:
            distance_miles = json_data["route"]["distance"]
            fuel_used_estimation = distance_miles / average_fuel_efficiency
            print("No se pudieron obtener los datos de combustible de MapQuest.")
            print("Estimado del combustible utilizado (Ltr): " + str("{:.1f}".format(fuel_used_estimation * 3.78)))

            
        print("==================================================================")

        print("Maniobras en español:")
        maneuvers = json_data["route"]["legs"][0]["maneuvers"]
        for maneuver in maneuvers:
            narrative = maneuver["narrative"]
            distance_km = maneuver["distance"] * 1.61
            translated_narrative = translator.translate(narrative, dest="es").text
            print ("- " + translated_narrative + " (" + "{:.1f}".format(distance_km)+ ")")
        
        print("==============================================================")
        
    elif json_status == 402:
        print("******************************************************************")
        print("Codigo de Estado: " + str (json_status) + "; Entradas de Usuario no Validas para Una o Ambas Ubicaciones. ")
        print("***************************************************************\ n")
    
    elif json_status == 601:
        print("******************************************************************")
        print("Codigo de Estado: " + str (json_status) + "; Falta una Entrada para Una o Ambas Ubicaciones.")
        print("******************************************************************")
    else:
        print("******************************************************************")
        print("Codigo de Estado: " + str (json_status) + "; Consulte")
        print(" https://developer.mapquest.com/documentation/directions-api/status-codes ")
        print("******************************************************************")