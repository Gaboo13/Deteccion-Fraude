# app.py
import os
import time
import pickle
import pandas as pd
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='.')
CORS(app)  # Habilitar CORS para permitir llamadas cross-origin si el HTML se abre localmente

# Cargar el modelo de Random Forest serializado
MODEL_PATH = "model.pkl"
model = None

try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    print("✅ Modelo cargado exitosamente.")
except Exception as e:
    print(f"❌ Error al cargar el modelo ({MODEL_PATH}): {str(e)}")

# Ruta principal para servir el Frontend HTML interactivo
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# Endpoint API para predecir transacciones fraudulentas
@app.route('/predecir', methods=['POST'])
def predecir():
    start_time = time.time()
    
    if model is None:
        return jsonify({
            "error": "El modelo de predicción no está cargado en el servidor."
        }), 500
        
    try:
        data = request.json  # Recibe los datos en formato JSON
        if not data:
            return jsonify({"error": "No se proporcionaron datos en la solicitud"}), 400
            
        # Validar campos obligatorios que espera el RandomForest
        campos_requeridos = ['amount', 'hour', 'day_of_week', 'transactions_last_24h', 'avg_amount_user', 'distance_from_home', 'is_international']
        campos_faltantes = [campo for campo in campos_requeridos if campo not in data]
        
        if campos_faltantes:
            return jsonify({
                "error": "Faltan campos obligatorios para la predicción",
                "campos_faltantes": campos_faltantes
            }), 400
            
        # Crear DataFrame para Pandas con las columnas ordenadas
        df_input = pd.DataFrame([data])[campos_requeridos]
        
        # Realizar predicción y cálculo de probabilidades
        prediccion = model.predict(df_input)[0]
        probabilidad = model.predict_proba(df_input)[0][1]
        
        # Categorizar el nivel de riesgo según la probabilidad
        prob_percent = float(probabilidad) * 100
        if prob_percent < 15:
            riesgo = "Bajo"
            color_riesgo = "#10b981"  # Emerald / Verde
        elif prob_percent < 50:
            riesgo = "Medio"
            color_riesgo = "#f59e0b"  # Amber / Amarillo
        elif prob_percent < 85:
            riesgo = "Alto"
            color_riesgo = "#f97316"  # Orange / Naranja
        else:
            riesgo = "Crítico"
            color_riesgo = "#ef4444"  # Red / Rojo
            
        execution_time_ms = (time.time() - start_time) * 1000
        
        return jsonify({
            "es_fraude": bool(prediccion),
            "probabilidad": float(probabilidad),
            "probabilidad_porcentaje": prob_percent,
            "riesgo": riesgo,
            "color_riesgo": color_riesgo,
            "metadatos": {
                "tiempo_ejecucion_ms": round(execution_time_ms, 2),
                "algoritmo": "RandomForestClassifier",
                "balanceo_clases": "class_weight='balanced'"
            }
        })
        
    except Exception as e:
        return jsonify({
            "error": "Error interno al procesar la predicción",
            "detalles": str(e)
        }), 500

if __name__ == '__main__':
    # Habilitar el servidor en el puerto 5000
    app.run(host='0.0.0.0', port=5000, debug=True)