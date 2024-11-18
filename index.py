import google.generativeai as genai
import os
import tempfile
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import urllib3

# Configuración de Flask
app = Flask(__name__)

# Configurar Generative AI
genai.configure(api_key="AIzaSyCJ1biYiA_IErtPWpUXMX7pPNeFWj3h_RM")

# Ruta principal
@app.route("/api", methods=["GET"])
def get_power_outage():
    zona = request.args.get("zona")
    if not zona:
        return jsonify({"error": "Zona es un parámetro obligatorio"}), 400

    try:
        # Descargar el PDF en memoria
        pdf_content, error = scrapear_y_obtener_pdf(
            "https://www.eeq.com.ec/cortes-de-servicio1"
        )
        if error:
            return jsonify({"error": error}), 400

        # Escribir el PDF en un archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(pdf_content)
            temp_pdf_path = temp_pdf.name

        # Subir el archivo PDF a Gemini
        file = genai.upload_file(path=temp_pdf_path, display_name="Corte Luz UIO")

        # Usar modelo generativo
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

        # Obtener la fecha actual
        date = os.popen("date +%Y-%m-%d").read().strip()
        prompt = (
            f"Dime el corte de luz para el día {date}, para {zona}, responde de la siguiente manera: "
            f"en formato json con ciudad, fecha y horarios[]"
        )

        # Generar contenido
        response = model.generate_content([prompt, file])

        # Parsear JSON de la respuesta
        response_text = response.text
        json_data = response_text.split("```json")[1].split("```")[0].strip()

        # Eliminar el archivo temporal
        os.remove(temp_pdf_path)

        return jsonify({"data": json_data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


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

            # Descargar el contenido del enlace en memoria
            response = requests.get(link, verify=False)
            if response.status_code == 200:
                return response.content, None
            else:
                return None, f"Error al descargar el PDF: {response.status_code}"
        else:
            return None, 'No se encontró el botón con la clase "ver_noticia_home".'
    else:
        return None, f"Error al acceder a la página: {response.status_code}"


# Punto de entrada
if __name__ == "__main__":
    app.run(debug=True)