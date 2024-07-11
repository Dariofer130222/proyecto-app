from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)  # Permitir peticiones CORS para desarrollo

# Base de datos temporal simulada (reemplazar con una base de datos real)
permisos_de_trabajo = {}

# Ruta para cargar datos desde un archivo Excel
def cargar_datos_desde_excel(archivo_excel):
    # Especificar el motor para leer el archivo Excel
    df = pd.read_excel(archivo_excel, engine='openpyxl')
    for _, row in df.iterrows():
        numero_cedula = str(row['numero_cedula'])
        permisos_de_trabajo[numero_cedula] = {
            "nombre": row['nombre'],
            "permiso_valido": row['permiso_valido']
        }

# Cargar datos desde el archivo Excel al iniciar la aplicación
cargar_datos_desde_excel('permisos.xlsx')

# Ruta para renderizar la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para verificar el estado del permiso de trabajo
@app.route('/verificar_permiso', methods=['POST'])
def verificar_permiso():
    data = request.get_json()
    numero_cedula = data.get('numero_cedula')

    if numero_cedula in permisos_de_trabajo:
        permiso = permisos_de_trabajo[numero_cedula]
        if permiso['permiso_valido']:
            return jsonify({'mensaje': f'Permiso válido para trabajar para {permiso["nombre"]}'})
        else:
            return jsonify({'mensaje': f'Permiso inválido para trabajar para {permiso["nombre"]}'})
    else:
        return jsonify({'mensaje': 'Número de cédula no encontrado'})

if __name__ == '__main__':
    app.run(debug=True)
