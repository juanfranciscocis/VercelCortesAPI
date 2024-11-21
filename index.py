import google.generativeai as genai
import os
from flask import Flask, request, jsonify, send_file
import urllib3
from pypdf import PdfReader
import tempfile
import requests
from bs4 import BeautifulSoup
import datetime

# Configuración de Flask
app = Flask(__name__)

# Configurar Generative AI
genai.configure(api_key="AIzaSyCJ1biYiA_IErtPWpUXMX7pPNeFWj3h_RM")

# Ruta principal
@app.route("/api", methods=["GET"])
def get_power_outage():
    zona = request.args.get("zona")

    data = informacion_de_zona(zona)

    jsonfinal = {
        "zona": zona,
        "horarios": data
    }

    return jsonify({"data": jsonfinal})


    


def scrapear_y_obtener_pdf(url):
    # Deshabilitar advertencias SSL
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Realiza la solicitud HTTP a la página
    response = requests.get(url, verify=False)

    # Verifica que la solicitud haya sido exitosa (código 200)
    if response.status_code == 200:
        # Parsear el contenido HTML de la página
        soup = BeautifulSoup(response.text, "html.parser")

        # Buscar el primer botón <a> con la clase "ver_noticia_home"
        button = soup.find("a", class_="ver_noticia_home")

        if button:
            # Obtener el enlace (href)
            link = button.get("href")

            # Descargar el contenido del enlace
            response = requests.get(link, verify=False)
            if response.status_code == 200:
                return response.content, None
            else:
                return None, f"Error al descargar el PDF: {response.status_code}"
        else:
            return None, 'No se encontró el botón con la clase "ver_noticia_home".'
    else:
        return None, f"Error al acceder a la página: {response.status_code}"

def informacion_de_zona(zona):
    print(f"Zona: {zona}")
    # Crear un archivo temporal para el PDF descargado
    pdf_content, error = scrapear_y_obtener_pdf('https://www.eeq.com.ec/cortes-de-servicio1')
    if error:
        print(f"Error: {error}")
        return

    # Guardar el contenido PDF en un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(pdf_content)
        temp_pdf_path = temp_pdf.name

    # Leer el PDF usando PdfReader
    reader = PdfReader(temp_pdf_path)

    # Imprimir el número de páginas del PDF
    print(f"Número de páginas: {len(reader.pages)}")



    # Obtener el contenido pagina por pagina hasta encontrar la zona
    for i in range(0,len(reader.pages)):
        page = reader.pages[i]
        text = page.extract_text()

        # Reemplazar los caracteres especiales
        text = text.replace("á", "a")
        text = text.replace("é", "e")
        text = text.replace("í", "i")
        text = text.replace("ó", "o")
        text = text.replace("ú", "u")
        text = text.replace("ñ", "n")
        text = text.replace("Á", "A")
        text = text.replace("É", "E")
        text = text.replace("Í", "I")
        text = text.replace("Ó", "O")
        text = text.replace("Ú", "U")
        text = text.replace("Ñ", "N")

        zona = zona.replace("á", "a")
        zona = zona.replace("é", "e")
        zona = zona.replace("í", "i")
        zona = zona.replace("ó", "o")
        zona = zona.replace("ú", "u")
        zona = zona.replace("ñ", "n")
        zona = zona.replace("Á", "A")
        zona = zona.replace("É", "E")
        zona = zona.replace("Í", "I")
        zona = zona.replace("Ó", "O")
        zona = zona.replace("Ú", "U")
        zona = zona.replace("Ñ", "N")


        print(f"Página {page}: {text}")

        print(f"Zona: {zona}")
        print(f"Texto: {text}")

        if zona.upper() in text.upper():
            print("Encontrada")
            print(f"Página Encontrada {page}: {text}")
            print(f"Zona encontrada: {zona}")

            # Buscar un / en el texto y extraer el hoario inicial y final 08:00 -12:00 / 4:00 - 8:00
            index = text.find("/")
            print(f"Index: {index}")
            inicio = text[index-13:index-1]
            fin = text[index+2:index+15]
            print(f"Inicio: {inicio}")
            print(f"Fin: {fin}")

            # Buscar en el texto 2024
            index = text.find("2024")
            print(f"Index: {index}")
            # Obtener la fecha : Viernes 24 de diciembre de 2024
            fecha = text[index-40:index+10]
            print(f"Fecha: {fecha}")
            # separa la fecha usando el espacio
            fecha = fecha.split(" ")
            print(f"Fecha separada: {fecha}")

            dia = obtener_primer_entero(fecha)
            print(f"Dia: {dia}")

            #Obtener el dia actual
            dia_actual = datetime.date.today().day
            print(f"Dia actual: {dia_actual}")

            if dia_actual <= dia: 
                return inicio, fin
    
    os.remove(temp_pdf_path)
    return "Zona no encontrada"

def obtener_primer_entero(lista):
    for elemento in lista:
        # Intentar convertir el elemento a entero
        try:
            return int(elemento)
        except ValueError:
            # Si no es posible convertirlo, continuar con el siguiente
            continue
    return None  # Retorna None si no se encuentra ningún número
# Punto de entrada
if __name__ == "__main__":
    app.run(debug=True)
