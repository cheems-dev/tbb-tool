from dotenv import load_dotenv
load_dotenv()  # Cargar las variables del archivo .env
import openai
import os
from flask import Flask, render_template_string, request, send_file

# Configura tu clave API
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)


# Prompts para cada paso
prompts = {"paso1":"""Actúa como un ingeniero experto en refactorización de código y realiza las siguientes transformaciones en el código proporcionado, **comentando las líneas originales** y escribiendo las correcciones una línea debajo según estas reglas:

1. **Comenta `#include <pthread.h>`**:  
   - Comenta todas las referencias a la biblioteca pthread (`// #include <pthread.h>`).  

2. **Transforma las declaraciones de variables `pthread_t`**:  
   - Comenta las declaraciones `pthread_t t;` y escribe su transformación debajo como `void* t;`.  

3. **Refactoriza las llamadas a `pthread_create`**:  
   - Comenta llamadas como `pthread_create(t, a, f, x);` y escribe debajo su transformación como `t = f(x);`, asegurándote de que la función `f` devuelva un valor de tipo `void*`.  

4. **Refactoriza las llamadas a `pthread_join`**:  
   - Si el segundo argumento no es `NULL`, comenta la línea original (por ejemplo, `pthread_join(t, x);`) y escribe debajo la corrección (`x = t;`).  
   - Si el segundo argumento es `NULL`, comenta la llamada y deja una nota indicando que ha sido eliminada, como `// pthread_join(t, NULL);`.  

5. **Asignaciones en operaciones pthread**:  
   - Si una operación pthread aparece en el lado derecho de una asignación (por ejemplo, `r = pthread_join(t, x);`), comenta la línea original y escribe dos líneas debajo:  
     ```  
     // r = pthread_join(t, x);  
     r = 0;  
     x = t;  
     ```  

6. **Comenta estructuras vacías**:  
   - Si un bucle `for` no contiene operaciones tras comentar las llamadas a pthread, comenta todo el bucle y deja una nota indicando que ha sido eliminado:  
     ```  
     // for (i = 0; i < NRSTAGES; i++)  
     // pthread_join(workerid[i], NULL);  
     // (El bucle se ha eliminado porque no contiene operaciones relevantes).  
     ```  
   - Si un `if` tiene una rama vacía tras comentar operaciones pthread, comenta el `if` completo y deja una nota indicando la transformación, o conserva la otra rama si aplica.  

Realiza estas transformaciones respetando la lógica original del programa y asegurándote de que el código resultante sea limpio y fácil de entender.""",
    "paso2": """Dado un código de bajo nivel que utiliza pthreads, realiza una refactorización con las siguientes características:

Transformación general:

Reemplaza el uso de pthreads por Intel TBB para aprovechar sus capacidades de paralelización y facilidad de mantenimiento.
Optimiza el código con un enfoque en bajo consumo de CPU, manteniéndolo mantenible, adaptable y portable.
Organización modular:

Descompón el código en etapas o funciones individuales para cada paso importante, siguiendo un modelo basado en pipelines con tbb::parallel_pipeline o una estructura equivalente en TBB.
Las funciones deben ser expresivas y fáciles de identificar (pueden llamarse Stage1, Stage2, ..., StageN según corresponda).
Refactorización del flujo principal:

Reestructura el bucle principal utilizando Intel TBB pipeline.
Garantiza que cada etapa del pipeline procese los datos de manera independiente, maximizando el paralelismo.
Si existen datos compartidos, aplica técnicas seguras para evitar condiciones de carrera.
Optimización de la estructura de datos:

Adecúa las estructuras de datos existentes (como PipeStruct en el ejemplo) para un entorno multi-threading eficiente con Intel TBB.
Ejemplo: Si la estructura tiene entradas y salidas, define claramente qué datos fluyen entre etapas y asegúrate de que no haya dependencia innecesaria.
Generalización:

El código debe soportar cualquier tipo de datos en las entradas y salidas. El tamaño y tipo de datos dependerán del código de entrada proporcionado.
Asegúrate de que la lógica de cada etapa sea modular y adaptable.
Mantenibilidad y claridad:

Documenta el código refactorizado con comentarios claros que expliquen las etapas del pipeline y cómo se transformó el código.
Si se optimiza alguna lógica, describe brevemente los cambios.
Ejemplo a seguir:
A continuación, un ejemplo de cómo un código basado en pthreads puede ser refactorizado con Intel TBB:

Código original (simplificado):
     ```  
struct PipeStruct {
  int* i_1;
  int output_1;
  int output_2;
};

PipeStruct S1(PipeStruct arg) {
  // Lógica de la etapa 1
  return arg;
}

PipeStruct S2(PipeStruct arg) {
  // Lógica de la etapa 2
  return arg;
}

void process() {
  do {
    PipeStruct arg = {&i_1};
    arg = S2(S1(arg));
  } while (*arg.i_1 >= 0);
}
 
     ```       
     Código refactorizado usando Intel TBB:
     ```   
     #include <tbb/tbb.h>
#include <iostream>

struct PipeStruct {
  int* i_1;
  int output_1;
  int output_2;
};

PipeStruct Stage1(PipeStruct arg) {
  // Lógica de la etapa 1
  return arg;
}

PipeStruct Stage2(PipeStruct arg) {
  // Lógica de la etapa 2
  return arg;
}

void processPipeline(int* input) {
  tbb::parallel_pipeline(
      tbb::task_scheduler_init::default_num_threads(),
      tbb::make_filter<void, PipeStruct>(
          tbb::filter::serial_in_order, [&](tbb::flow_control& fc) -> PipeStruct {
            if (*input < 0) {
              fc.stop();
              return {};
            }
            return PipeStruct{input};
          }) &
          tbb::make_filter<PipeStruct, PipeStruct>(
              tbb::filter::parallel, [&](PipeStruct arg) { return Stage1(arg); }) &
          tbb::make_filter<PipeStruct, void>(
              tbb::filter::serial_in_order, [&](PipeStruct arg) { Stage2(arg); }));
}

     ```   
     """,
    "patron_pipeline":"""Refactoriza el siguiente código en C++ que utiliza pthreads para un pipeline paralelo, utilizando Intel TBB y sus funciones modernas como `tbb::parallel_pipeline` y `tbb::make_filter`.

1. Identifica las etapas del pipeline en el código basado en pthreads (por ejemplo, generación de datos, procesamiento, finalización) y refactoriza cada una a un filtro en TBB utilizando `tbb::make_filter`.
2. Para la etapa que produce datos, usa `tbb::filter::serial` y asegúrate de que sea una etapa secuencial que detenga el flujo cuando termine de generar los datos.
3. Para las etapas de procesamiento en paralelo, usa `tbb::filter::parallel` para ejecutar las operaciones en paralelo sobre los datos generados.
4. Refactoriza el código para que el flujo de datos entre las etapas sea gestionado automáticamente por TBB sin necesidad de manejo manual de hilos o sincronización.
5. Asegúrate de que el código resultante sea modular, eficiente y aproveche las capacidades paralelizadas de TBB.
6. Mantén la estructura de etapas del pipeline similar a la siguiente: 
    - Etapa 1: Generación de datos.
    - Etapa 2: Procesamiento paralelo.
    - Etapa 3: Procesamiento final.

El resultado debe tener un código limpio y modular usando `tbb::parallel_pipeline` y `tbb::make_filter`, donde cada etapa del pipeline está claramente definida y usa las funciones más modernas de TBB.
""",
    "patron_paralelismo_tareas":"""Refactoriza el siguiente código que utiliza pthreads para realizar multiplicación de matrices y reemplázalo por un enfoque usando Intel TBB con el patrón de diseño 'Paralelismo de tarea'.
      El código debe estar estructurado para utilizar tbb::parallel_for de forma eficiente, distribuyendo las iteraciones del bucle en paralelo, asegurando que las operaciones de multiplicación de matrices se realicen de manera 
      concurrente y optimizada. Mantén la funcionalidad original del código, procesando matrices de tamaño definido en tiempo de ejecución, pero refactoriza todo el manejo de la concurrencia y el procesamiento de las filas de la 
      matriz utilizando Intel TBB."""
   
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
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 0;
        }
        h1 {
            text-align: center;
            color: #2c3e50;
            margin-top: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        form {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        label {
            font-size: 16px;
            font-weight: bold;
            color: #333;
        }
        textarea {
            width: 100%;
            padding: 10px;
            font-size: 14px;
            border: 1px solid #ccc;
            border-radius: 4px;
            resize: vertical;
        }
        button {
            background-color: #3498db;
            color: white;
            padding: 10px;
            font-size: 16px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #2980b9;
        }
        button:active {
            background-color: #1f6fa3;
        }
        .button-container {
            display: flex;
            gap: 10px;
            justify-content: center;
        }
        .button-container button {
            width: 180px;
        }
    </style>
</head>
<body>
    <h1>Refactorización de Código de pthreads a Intel TBB</h1>
    <div class="container">
        <form method="POST" action="/generate">
            <label for="code">Inserta el código base:</label>
            <textarea name="code" id="code" rows="10" cols="50"></textarea>
            <div class="button-container">
                <button type="submit" name="step" value="paso1">Generar Paso 1</button>
                <button type="submit" name="step" value="paso2">Generar Paso 2</button>
                <button type="submit" name="step" value="patron_pipeline">patron pipeline</button>
                <button type="submit" name="step" value="patron_paralelismo_tareas">paralelismo de tareas </button>
            </div>
        </form>
    </div>
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
    app.run(debug=True)

