from flask import Flask, render_template, request
from prediccion import predecir_riesgo

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/entendimiento_negocio')
def entendimiento_negocio():
    return render_template('entendimiento_negocio.html')

@app.route('/ingenieria_datos')
def ingenieria_datos():
    return render_template('ingenieria_datos.html')

@app.route('/ingenieria_modelo')
def ingenieria_modelo():
    return render_template('ingenieria_modelo.html')

@app.route('/pcga')
def pcga():
    return render_template('pcga.html')

@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
    nivel_riesgo = None
    if request.method == 'POST':
        # Obtener datos del formulario
        edad = int(request.form['edad'])
        genero = request.form['genero']
        if genero == 'M':
            genero = 'Masculino'
        else:
            genero = 'Femenino'
        
        # Convertir nivel de actividad física a categoría
        nivel_actividad = int(request.form['actividad'])
        if nivel_actividad <= 2:
            actividad_fisica = 'Sedentario'
        elif nivel_actividad == 3:
            actividad_fisica = 'Moderado'
        else:
            actividad_fisica = 'Activo'
        
        # Determinar hábitos alimenticios
        alimentacion = request.form['alimentacion'].lower()
        if 'fruta' in alimentacion and not 'frito' in alimentacion:
            habitos_alimenticios = 'Saludables'
        else:
            habitos_alimenticios = 'No Saludables'
        
        # Obtener IMC
        imc = float(request.form['imc'])
        
        # Determinar presión arterial
        presion = int(request.form['presion'])
        if presion < 120:
            presion_arterial = 'Normal'
        elif presion < 140:
            presion_arterial = 'Prehipertensión'
        else:
            presion_arterial = 'Hipertensión'
        
        # Determinar consumo de sustancias
        consumo = int(request.form['consumo'])
        if consumo > 0:
            consumo_sustancias = 'Sí'
        else:
            consumo_sustancias = 'No'
        
        # Obtener nivel de estrés
        nivel_estres_num = int(request.form['estres'])
        if nivel_estres_num <= 2:
            nivel_estres = 'Bajo'
        elif nivel_estres_num <= 4:
            nivel_estres = 'Moderado'
        else:
            nivel_estres = 'Alto'
        
        # Realizar predicción
        nivel_riesgo = predecir_riesgo(edad, genero, actividad_fisica, habitos_alimenticios, 
                                      imc, presion_arterial, consumo_sustancias, nivel_estres)
    
    # Renderizar la misma plantilla con o sin resultados
    return render_template('ingresar.html', nivel_riesgo=nivel_riesgo)

if __name__ == '__main__':
    app.run(debug=True)