# IMPORTS
import csv
import json


# ----------------------------------------------------- File Reader -----------------------------------------------------#

# E: String nombre del archivo csv
# D: Lee el archivo y lo retorna como una matriz
# S: Matriz de strings donde la primera fila es el encabezado y el resto los datos
def readCSV(fileName):
    document = []
    with open(fileName + ".csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            document += [row]
    return document


# E: Matriz de strings donde la primera fila es el encabezado y el resto los datos
# D: Imprime la matriz
# S: ningúna
def printData(data):
    for row in data:
        print(row)


# ----------------------------------------------------- File Writer -----------------------------------------------------#

# E: Matriz de string donde la primera fila es el encabezado y el resto los datos , String nombre del archivo json
# D:
# S:
def writeJSON(data, path):
    with open(path + ".json", "w", encoding="utf-8") as jsonf:
        jsonString = json.dumps(data, indent=4)
        jsonf.write(jsonString)


# ---------------------------------------------------------- UI ----------------------------------------------------------#

# E: ninguna
# D: Despliega interfaz de usuario para usar el comvertidor
# S: ninguna


def menu():
    print("# ---------------------------------------------------------- #")
    print("# ------------------ CSV to JSON Converter ----------------- #")
    print("# ---------------------------------------------------------- #")
    print("")
    print("Asegurese que se encuentra en la carpeta donde se encuentran los archivos")
    print("")
    print("")
    filename = input(
        "Digite el nombre del archivo a convertir (No incluya la extensión '.csv'): "
    )
    print("")
    print("Leyendo archivo...")
    data = readCSV(filename)
    print("Transformando archivo...")
    print("Escribiendo archivo...")
    writeJSON(data, filename)
    print()
    print("Archivo creado con éxito con el nombre: " + filename + ".json")


menu()
