import google.generativeai as genai
import os
from flask import Flask, request, jsonify, send_file

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
        # Enviar un PDF a Gemini
        # Llamada a la función con la URL proporcionada
        scrapear_y_descargar_pdf('https://www.eeq.com.ec/cortes-de-servicio1')
        file = genai.upload_file(path="./PDFs/VSD.pdf", display_name="Corte Luz UIO")

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

        return jsonify({"data": json_data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route("/privacy", methods=["GET"])
def privacy():
    privacy_html = "./privacy.html"
    return send_file(privacy_html, mimetype="text/html")

    

import requests
from bs4 import BeautifulSoup

def scrapear_y_descargar_pdf(url):
    # Realiza la solicitud HTTP a la página
    response = requests.get(url)

    # Verifica que la solicitud haya sido exitosa (código 200)
    if response.status_code == 200:
        # Parsear el contenido HTML de la página
        soup = BeautifulSoup(response.text, 'html.parser')

        # Buscar el primer botón <a> con la clase "ver_noticia_home"
        button = soup.find('a', class_='ver_noticia_home')

        if button:
            # Obtener el enlace (href) y el texto del botón
            link = button.get('href')
            text = button.text.strip()

            print(f'Enlace: {link}')
            print(f'Texto del botón: {text}')
            
            # Descargar el contenido de la página en el directorio actual PDFs
            response = requests.get(link)
            
            # Crear el directorio 'PDFs' si no existe
            import os
            os.makedirs('PDFs', exist_ok=True)
            
            with open('PDFs/VSD.pdf', 'wb') as f:
                f.write(response.content)
            
            print('PDF descargado exitosamente.')
            
        else:
            print('No se encontró el botón con la clase "ver_noticia_home".')

    else:
        print(f'Error al acceder a la página: {response.status_code}')



# Punto de entrada
if __name__ == "__main__":
    app.run(debug=True)