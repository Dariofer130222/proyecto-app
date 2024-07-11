from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)  # Permitir peticiones CORS para desarrollo

# Función para cargar datos desde el archivo Excel
def cargar_permisos_de_trabajo():
    try:
        df = pd.read_excel('permisos_trabajo.xlsx', engine='openpyxl')

        # Verificar que las columnas necesarias existan en el archivo Excel
        required_columns = ['numero_cedula', 'nombre', 'permiso_valido']
        if not all(col in df.columns for col in required_columns):
            raise Exception("El archivo Excel no tiene todas las columnas requeridas")

        permisos_dict = df.to_dict(orient='records')
        permisos_de_trabajo = {str(permiso['numero_cedula']): {'nombre': permiso['nombre'], 'permiso_valido': permiso['permiso_valido']} for permiso in permisos_dict}
        return permisos_de_trabajo
    except FileNotFoundError:
        print("Archivo Excel no encontrado.")
    except Exception as e:
        print(f'Error al cargar el archivo Excel: {str(e)}')
    return {}

# Base de datos de permisos de trabajo (se carga desde el archivo Excel)
permisos_de_trabajo = cargar_permisos_de_trabajo()

# Ruta para renderizar la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para verificar el estado del permiso de trabajo
@app.route('/verificar_permiso', methods=['POST'])
def verificar_permiso():
    data = request.get_json()
    numero_cedula = data.get('numero_cedula')

    if not numero_cedula:
        return jsonify({'mensaje': 'Número de cédula no proporcionado'}), 400

    if numero_cedula in permisos_de_trabajo:
        if permisos_de_trabajo[numero_cedula]['permiso_valido'].upper() == 'TRUE':  # Convertir a mayúsculas y comparar
            return jsonify({'mensaje': 'Permiso válido para trabajar'})
        else:
            return jsonify({'mensaje': 'Permiso inválido para trabajar'}), 403
    else:
        return jsonify({'mensaje': 'Número de cédula no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)
