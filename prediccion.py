import pickle
import numpy as np

def cargar_modelo():
    with open('modelo_riesgo_cardiovascular.pkl', 'rb') as archivo:
        datos = pickle.load(archivo)
    return datos

def predecir_riesgo(edad, genero, actividad_fisica, habitos_alimenticios, imc, presion_arterial, consumo_sustancias, nivel_estres=None):
    # Cargar el modelo y los codificadores
    datos_modelo = cargar_modelo()
    modelo = datos_modelo['modelo']
    le_genero = datos_modelo['le_genero']
    le_actividad = datos_modelo['le_actividad']
    le_habitos = datos_modelo['le_habitos']
    le_presion = datos_modelo['le_presion']
    le_consumo = datos_modelo['le_consumo']
    
    # Transformar las entradas categóricas
    genero_encoded = le_genero.transform([genero])[0]
    actividad_encoded = le_actividad.transform([actividad_fisica])[0]
    habitos_encoded = le_habitos.transform([habitos_alimenticios])[0]
    presion_encoded = le_presion.transform([presion_arterial])[0]
    consumo_encoded = le_consumo.transform([consumo_sustancias])[0]
    
    # Crear el vector de características
    caracteristicas = np.array([[edad, genero_encoded, actividad_encoded, habitos_encoded, 
                                imc, presion_encoded, consumo_encoded]])
    
    # Realizar la predicción
    prediccion = modelo.predict(caracteristicas)[0]
    
    # Convertir la predicción numérica a categoría
    nivel_riesgo_pred = datos_modelo['le_nivel_estres'].inverse_transform([prediccion])[0]
    
    # Determinar el nivel de riesgo basado en la predicción
    if nivel_riesgo_pred == 'Bajo':
        nivel_riesgo = 'Bajo'
    elif nivel_riesgo_pred == 'Moderado':
        nivel_riesgo = 'Medio'
    else:
        nivel_riesgo = 'Alto'
    
    return nivel_riesgo

# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo de datos de entrada (valores numéricos como en el formulario)
    edad = 25
    genero = "M"  # M o F como en el formulario
    actividad_fisica = 2  # 1-5 (1-2: Sedentario, 3: Moderado, 4-5: Activo)
    habitos_alimenticios = "frutas y verduras"  # Texto descriptivo de alimentación
    imc = 28.5
    presion_arterial = 130  # Valor numérico en mmHg
    consumo_sustancias = 1  # 0-3 (0: Ninguno, 1: Bajo, 2: Moderado, 3: Alto)
    nivel_estres = 5  # 1-5 (1-2: Bajo, 3-4: Moderado, 5: Alto)
    
    # Procesamiento como en app.py
    if genero == "M":
        genero_procesado = "Masculino"
    else:
        genero_procesado = "Femenino"
        
    if actividad_fisica <= 2:
        actividad_procesada = "Sedentario"
    elif actividad_fisica == 3:
        actividad_procesada = "Moderado"
    else:
        actividad_procesada = "Activo"
        
    if "fruta" in habitos_alimenticios.lower() and not "frito" in habitos_alimenticios.lower():
        habitos_procesados = "Saludables"
    else:
        habitos_procesados = "No Saludables"
        
    if presion_arterial < 120:
        presion_procesada = "Normal"
    elif presion_arterial < 140:
        presion_procesada = "Prehipertensión"
    else:
        presion_procesada = "Hipertensión"
        
    if consumo_sustancias > 0:
        consumo_procesado = "Sí"
    else:
        consumo_procesado = "No"
        
    if nivel_estres <= 2:
        estres_procesado = "Bajo"
    elif nivel_estres <= 4:
        estres_procesado = "Moderado"
    else:
        estres_procesado = "Alto"
    
    riesgo = predecir_riesgo(edad, genero_procesado, actividad_procesada, habitos_procesados, 
                            imc, presion_procesada, consumo_procesado)
    print(f"El nivel de riesgo cardiovascular es: {riesgo}")