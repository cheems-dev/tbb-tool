from dotenv import load_dotenv
load_dotenv()  # Cargar las variables del archivo .env
import openai
import os
from flask import Flask, render_template_string, request, send_file

# Configura tu clave API
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)


# Prompts para cada paso
prompts = {
    "paso1": "Comenta todas las líneas de código relacionadas con pthreads en el siguiente código, incluyendo `#include <pthread.h>`, llamadas a `pthread_create`, `pthread_join`, y variables relacionadas como `pthread_t`. Mantén el resto del código intacto y añade comentarios explicativos donde sea necesario.",
    "paso2": "Toma el código del Paso 1 y comenta las funciones relacionadas que serán reemplazadas por un enfoque basado en el patrón de diseño **parallel_pipeline** de Intel TBB. Utiliza **parallel_pipeline** para procesar las etapas del pipeline de manera paralela y eficiente. Proporciona comentarios indicando cómo se sustituirán las etapas del pipeline utilizando **parallel_pipeline** y cuáles son las diferencias clave con respecto a un pipeline secuencial. Asegúrate de resaltar las ventajas de este enfoque en comparación con el uso de hilos manuales.",
    "paso3": "Refactoriza completamente el código proporcionado utilizando Intel TBB. Si es más adecuado, implementa el patrón **Farm** para dividir el trabajo entre varios trabajadores. Si el patrón **Pipeline** es más apropiado, utiliza **parallel_pipeline** sin recurrir a `parallel.h` ni `scheduler.h`. Asegúrate de que el código final sea funcional y aproveche correctamente las herramientas de la biblioteca Intel TBB sin necesidad de los encabezados mencionados."
}

@app.route('/')
def index():
    return render_template_string(''' 
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Refactorización de Código</title>
        </head>
        <body>
            <h1>Refactorización de Código de pthreads a Intel TBB</h1>
            <form method="POST" action="/generate">
                <label for="code">Inserta el código base:</label><br>
                <textarea name="code" id="code" rows="10" cols="50"></textarea><br><br>
                <button type="submit" name="step" value="paso1">Generar Paso 1</button>
                <button type="submit" name="step" value="paso2">Generar Paso 2</button>
                <button type="submit" name="step" value="paso3">Generar Paso 3</button>
            </form>
        </body>
        </html>
    ''')

@app.route('/generate', methods=['POST'])
def generate():
    step = request.form['step']
    code = request.form['code']

    # Selecciona el prompt adecuado
    prompt = prompts[step]
    full_prompt = f"{prompt}\n\nCódigo base:\n{code}"

    # Llama a la API de OpenAI usando ChatCompletion
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente que ayuda a refactorizar código."},
            {"role": "user", "content": full_prompt}
        ]
    )

    # Extrae el código generado
    generated_code = response["choices"][0]["message"]["content"].strip()

    # Obtén la ruta del directorio donde se está ejecutando el script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = f"codigo_{step}.cpp"
    file_path = os.path.join(current_dir, file_name)  # Usar el directorio actual

    with open(file_path, "w") as file:
        file.write(generated_code)

    # Ofrece el archivo para descargar
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

