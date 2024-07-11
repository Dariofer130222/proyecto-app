from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)  # Permitir peticiones CORS para desarrollo

# Cargar datos desde el archivo Excel
def cargar_permisos_de_trabajo():
    try:
        df = pd.read_excel('verificar_permiso\permisos_trabajo.xlsx', engine='openpyxl')
        permisos_dict = df.to_dict(orient='records')
        permisos_de_trabajo = {str(permiso['numero_cedula']): {'nombre': permiso['nombre'], 'permiso_valido': permiso['permiso_valido']} for permiso in permisos_dict}
        return permisos_de_trabajo
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
    numero_cedula = data['numero_cedula']

    if numero_cedula in permisos_de_trabajo:
        if permisos_de_trabajo[numero_cedula]['permiso_valido'] == 'TRUE':  # Considerando que el valor en Excel es una cadena 'TRUE' o 'FALSE'
            return jsonify({'mensaje': 'Permiso válido para trabajar'})
        else:
            return jsonify({'mensaje': 'Permiso inválido para trabajar'}), 403
    else:
        return jsonify({'mensaje': 'Número de cédula no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)
