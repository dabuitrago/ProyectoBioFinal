from flask import Flask, render_template, request, jsonify
import requests
from collections import defaultdict
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

app = Flask(__name__)

# DEFINIMOS LAS RUTAS PARA LOS LINKS DEL NAVBAR
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ecosistemas')
def ecosistemas():
    return render_template('ecosistemas.html')   

@app.route('/fauna')
def fauna():
    return render_template('fauna.html')

@app.route('/flora')
def flora():
    return render_template('flora.html')    

@app.route('/parques')
def parques():
    return render_template('parques.html')

# DEFINIMOS LAS RUTAS PARA LOS LINKS DEL DROPDOWN
@app.route('/pnnChingaza', methods=['GET', 'POST'])
def pnn_chingaza():
    return render_weather_template('pnnChingaza.html')

@app.route('/pnnCocuy', methods=['GET', 'POST'])
def pnn_cocuy():
    return render_weather_template('pnnCocuy.html')

@app.route('/pnnOceta', methods=['GET', 'POST'])
def pnn_oceta():
    return render_weather_template('pnnOceta.html')

@app.route('/pnnPisba', methods=['GET', 'POST'])
def pnn_pisba():
    return render_weather_template('pnnPisba.html')

@app.route('/pnnSumapaz', methods=['GET', 'POST'])
def pnn_sumapaz():
    return render_weather_template('pnnSumapaz.html')

@app.route('/paramoGuargua', methods=['GET', 'POST'])
def paramo_guargua():
    return render_weather_template('paramoGuargua.html')

# DEFINIMOS LAS RUTAS PARA RENDERIZAR DATOS CSV DE PARAMOS

@app.route('/data')
def data():
    df = pd.read_csv('xn--Pramos-pta.csv', sep=',', index_col="ComplejoNombre")
    paramos_consolidado = df.groupby('DistritoNombre').sum('AreaHa')
    html_table = df.to_html(classes='table table-striped', index=False)
    return render_template('data.html', table=html_table)    

@app.route('/get_paramos', methods=['POST'])
def get_paramos():
    departamento = request.form['departamento']
    url = f"https://www.datos.gov.co/resource/r2yz-k5z7.json?$select=nombre_paramo,sum(rea_hect_reas) as total_hectareas,nombre_de_municipio&$where=nombre_del_departamento=%22{departamento}%22&$group=nombre_paramo,nombre_de_municipio"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        
        # Agrupar los resultados por nombre_paramo
        resultados_agrupados = defaultdict(lambda: {'total_hectareas': 0.0, 'municipios': []})
        
        for item in data:
            nombre_paramo = item['nombre_paramo']
            nombre_municipio = item['nombre_de_municipio']
            total_hectareas = float(item['total_hectareas']) if item['total_hectareas'] else 0.0
            
            resultados_agrupados[nombre_paramo]['total_hectareas'] += total_hectareas
            resultados_agrupados[nombre_paramo]['municipios'].append(nombre_municipio)

        # Convertir el resultado a una lista
        resultados_finales = []
        for nombre_paramo, info in resultados_agrupados.items():
            resultados_finales.append({
                'nombre_paramo': nombre_paramo,
                'total_hectareas': info['total_hectareas'],
                'municipios': ', '.join(set(info['municipios']))
            })

        return jsonify(resultados_finales)
    else:
        return jsonify({"error": "No se pudieron obtener los datos"}), response.status_code    

def render_weather_template(template_name):
    weather_data = None
    error_message = None
    
    if request.method == 'POST':
        city = request.form['search']
        url = f"https://wttr.in/{city}?format=3"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.text
            return render_template(template_name, weather=weather_data)
        else:
            error_message = "No se pudo obtener la información del clima."
            return render_template(template_name, error=error_message)
    return render_template(template_name)    

if __name__ == '__main__':
    app.run(port=5500, debug=True)


# LOS GRAFICOS SE RENDERIZAN COMO IMAGENES

#Gráfico de áreas

#total_areas = paramos_consolidado.sum(axis=1);
#paramos_consolidado.plot(kind='bar');
#plt.bar(total.index, total);
#plt.title('Total Areas');
#plt.xlabel('ComplejoNombre');
#plt.ylabel('AreaHa');
#plt.show();

#Gráficos apilados:
#paramos_consolidado.plot(kind='barh', title="Áreas Totales Páramos Cundinamarca - Boyacá", ylabel='ComplejoNombre') 

#plt.show(); 