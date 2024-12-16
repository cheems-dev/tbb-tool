# Proyecto Flask con OpenAI

Este proyecto utiliza Flask para construir un servidor web que interactúa con la API de OpenAI. A continuación, se describen los pasos necesarios para configurar y ejecutar el proyecto en tu entorno local.

## Requisitos previos

1. **Python 3.8 o superior**: Asegúrate de tener Python instalado. Puedes verificarlo ejecutando:
   ```bash
   python --version
   ```

## Instrucciones para levantar el proyecto

1. **Clona el repositorio o descomprime los archivos**.
   Aseg Aseg\u00rate de tener todos los archivos del proyecto, incluyendo `main.py`, `requirements.txt` y un archivo `.env` (creado más adelante).

2. **Crea un entorno virtual** (recomendado):
   En la carpeta del proyecto, ejecuta:

   ```bash
   python -m venv env
   ```

3. **Activa el entorno virtual**:

   - En Windows:
     ```bash
     .\env\Scripts\activate
     ```
   - En macOS/Linux:
     ```bash
     source env/bin/activate
     ```

4. **Instala las dependencias**:
   Con el entorno virtual activo, ejecuta:

   ```bash
   pip install -r requirements.txt
   ```

5. **Configura las variables de entorno**:
   Crea un archivo llamado `.env` en la carpeta del proyecto y define las siguientes variables:

   ```env
   OPENAI_API_KEY=tu_clave_api_de_openai
   ```

6. **Ejecuta la aplicación**:
   Con el entorno virtual activo, inicia el servidor Flask:

   ```bash
   python main.py
   ```

7. **Accede a la aplicación**:
   Abre un navegador y ve a `http://127.0.0.1:5000` para interactuar con la aplicación.

## Estructura del proyecto

- `main.py`: Archivo principal que contiene la lógica de la aplicación Flask.
- `requirements.txt`: Lista de dependencias necesarias para ejecutar el proyecto.
- `.env`: Archivo para almacenar variables de entorno, como la clave API de OpenAI.

## Notas adicionales

- Asegúrate de que tu clave de API de OpenAI sea válida y tenga suficientes límites disponibles para las solicitudes.
- Si deseas instalar dependencias adicionales o cambiar alguna versión, edita el archivo `requirements.txt` y vuelve a instalar con `pip install -r requirements.txt`.

## Solución de problemas

1. **Error al ejecutar `main.py`**:

   - Verifica que el entorno virtual esté activo.
   - Asegúrate de que las dependencias estén instaladas correctamente.

2. **Error de clave API**:

   - Revisa el archivo `.env` para confirmar que la variable `OPENAI_API_KEY` está correctamente configurada.

3. **Error de dependencia no satisfecha**:
   - Asegúrate de tener la versión correcta de Python y `pip`. Actualiza si es necesario:
     ```bash
     python -m pip install --upgrade pip
     ```
