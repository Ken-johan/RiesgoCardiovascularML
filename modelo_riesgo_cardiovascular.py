import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Cargar el dataset
ruta_dataset = 'dataset_riesgo_cardiovascular_jovenes_bogota.csv'
datos = pd.read_csv(ruta_dataset)

# Preprocesamiento de datos
# Convertir variables categóricas a numéricas
le_genero = LabelEncoder()
le_actividad = LabelEncoder()
le_habitos = LabelEncoder()
le_presion = LabelEncoder()
le_consumo = LabelEncoder()
le_nivel_estres = LabelEncoder()

datos['Género'] = le_genero.fit_transform(datos['Género'])
datos['Actividad_Física'] = le_actividad.fit_transform(datos['Actividad_Física'])
datos['Hábitos_Alimenticios'] = le_habitos.fit_transform(datos['Hábitos_Alimenticios'])
datos['Presión_Arterial'] = le_presion.fit_transform(datos['Presión_Arterial'])
datos['Consumo_Sustancias'] = le_consumo.fit_transform(datos['Consumo_Sustancias'])
datos['Nivel_Estrés'] = le_nivel_estres.fit_transform(datos['Nivel_Estrés'])

# Definir características (X) y variable objetivo (y)
X = datos.drop('Nivel_Estrés', axis=1)  # Asumimos que Nivel_Estrés es la variable objetivo
y = datos['Nivel_Estrés']

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Definir parámetros para búsqueda de hiperparámetros
param_grid = {
    'max_depth': [None, 5, 10, 15, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'criterion': ['gini', 'entropy']
}

# Crear y entrenar el modelo con búsqueda de hiperparámetros
grid_search = GridSearchCV(DecisionTreeClassifier(random_state=42), param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Obtener el mejor modelo
mejor_modelo = grid_search.best_estimator_

# Evaluar el modelo
y_pred = mejor_modelo.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
reporte = classification_report(y_test, y_pred)
matriz_confusion = confusion_matrix(y_test, y_pred)

print(f"Precisión del modelo: {accuracy:.4f}")
print("\nReporte de clasificación:")
print(reporte)
print("\nMatriz de confusión:")
print(matriz_confusion)
print("\nMejores parámetros:", grid_search.best_params_)

# Guardar el modelo entrenado y los codificadores
with open('modelo_riesgo_cardiovascular.pkl', 'wb') as archivo:
    pickle.dump({
        'modelo': mejor_modelo,
        'le_genero': le_genero,
        'le_actividad': le_actividad,
        'le_habitos': le_habitos,
        'le_presion': le_presion,
        'le_consumo': le_consumo,
        'le_nivel_estres': le_nivel_estres
    }, archivo)

print("Modelo guardado exitosamente como 'modelo_riesgo_cardiovascular.pkl'")