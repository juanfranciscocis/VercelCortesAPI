import google.generativeai as genai
import os
from flask import Flask, request, jsonify, send_file
import urllib3
from pypdf import PdfReader
import tempfile
import requests
from bs4 import BeautifulSoup
import datetime
from datetime import datetime
import pytz


# Configuración de Flask
app = Flask(__name__)

# Configurar Generative AI
genai.configure(api_key="AIzaSyCJ1biYiA_IErtPWpUXMX7pPNeFWj3h_RM")

# Ruta principal
@app.route("/api", methods=["GET"])
def get_power_outage():
    zona = request.args.get("zona")
    print(f"Zona: {zona}")

    # Diccionario con los nombres de los meses en español
    meses_espanol = {
        1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
        5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
        9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
    }

    # Zona horaria de Ecuador
    ecuador_tz = pytz.timezone('America/Guayaquil')

    # Obtener la fecha y hora actual en Ecuador
    ecuador_time = datetime.now(ecuador_tz)



    # Formatear la fecha y hora
    dia = int(ecuador_time.strftime("%d"))
    mes = int(ecuador_time.strftime("%m"))
    mes_esp = meses_espanol[mes]
    ano = int(ecuador_time.strftime("%Y"))

    print("Fecha y hora en Ecuador:", dia)



    data = informacion_de_zona(zona, dia)

    jsonfinal = {
        "zona": zona,
        "horarios": data,
        "fecha": [dia, mes_esp, ano]
    }

    return jsonify({"data": jsonfinal})


    


def scrapear_y_obtener_todos_los_pdfs(url):
    # Deshabilitar advertencias SSL
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Realiza la solicitud HTTP a la página
    response = requests.get(url, verify=False)

    # Verifica que la solicitud haya sido exitosa (código 200)
    if response.status_code == 200:
        # Parsear el contenido HTML de la página
        soup = BeautifulSoup(response.text, "html.parser")

        # Buscar todos los botones <a> con la clase "ver_noticia_home"
        buttons = soup.find_all("a", class_="ver_noticia_home")
        pdfs = []

        # Descargar los contenidos de cada enlace
        for button in buttons:
            link = button.get("href")
            response = requests.get(link, verify=False)
            if response.status_code == 200:
                pdfs.append(response.content)
            else:
                print(f"Error al descargar el PDF en {link}: {response.status_code}")
        return pdfs, None
    else:
        return None, f"Error al acceder a la página: {response.status_code}"


def informacion_de_zona(zona,dia_ec):
    pdfs, error = scrapear_y_obtener_todos_los_pdfs('https://www.eeq.com.ec/cortes-de-servicio1')
    if error:
        print(f"Error: {error}")
        return

    for index, pdf_content in enumerate(pdfs):
        print(f"Procesando PDF #{index + 1}...")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(pdf_content)
            temp_pdf_path = temp_pdf.name

        try:
            reader = PdfReader(temp_pdf_path)
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                text = text.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
                text = text.replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U")
                text = text.replace("ñ", "n")
                text = text.replace("\n", " ")

                zona = zona.lower()
                zona = zona.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
                zona = zona.replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U")
                zona = zona.replace("ñ", "n")
                zona = zona.replace("\n", " ")

                print(f"Texto: {text}")

                if zona in text.lower():
                    # Procesar horarios y fecha
                    index_fecha = text.find("2024")
                    index_horarios = text.find("/")
                    if index_fecha != -1 and index_horarios != -1:
                        inicio = text[index_horarios - 13:index_horarios - 1].strip()
                        fin = text[index_horarios + 2:index_horarios + 15].strip()
                        fecha = text[index_fecha - 40:index_fecha + 10].strip()
                        fecha_separada = fecha.split(" ")
                        

                        dia = obtener_primer_entero(fecha_separada)


                        if dia == dia_ec:
                            os.remove(temp_pdf_path)
                            return inicio,fin
                        

                        dia = obtener_segundo_entero(fecha_separada)
                        if dia == dia_ec:
                            os.remove(temp_pdf_path)
                            return inicio,fin

            os.remove(temp_pdf_path)
        except Exception as e:
            os.remove(temp_pdf_path)
            print(f"Error procesando el PDF #{index + 1}: {e}")

    return "Zona no encontrada"


def obtener_primer_entero(lista):
    for elemento in lista:
        try:
            return int(elemento)
        except ValueError:
            continue
        return None

def obtener_segundo_entero(lista):
    elementos = []
    for elemento in lista:
        try:
            elementos.append(int(elemento))
        except ValueError:
            continue
    if len(elementos) > 1:
        return elementos[1]
    else:
        return None
    


@app.route("/api/specific_date", methods=["GET"])
def get_power_outage_specific_date():
    zona = request.args.get("zona")
    dia = request.args.get("dia")
    print(f"Zona: {zona}")
    print(f"Dia: {dia}")


        # Diccionario con los nombres de los meses en español
    meses_espanol = {
        1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
        5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
        9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
    }

    # Zona horaria de Ecuador
    ecuador_tz = pytz.timezone('America/Guayaquil')

    # Obtener la fecha y hora actual en Ecuador
    ecuador_time = datetime.now(ecuador_tz)


    mes = int(ecuador_time.strftime("%m"))
    mes_esp = meses_espanol[mes]
    ano = int(ecuador_time.strftime("%Y"))


    
    data = informacion_de_zona(zona, int(dia))

    jsonfinal = {
        "zona": zona,
        "horarios": data,
        "fecha": [dia, mes_esp, ano]
    }
    return jsonify({"data": jsonfinal})



# Punto de entrada
if __name__ == "__main__":
    app.run(debug=True)
