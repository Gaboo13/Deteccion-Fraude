# Sentinel AI - Sistema de Detección de Fraude en Tiempo Real

**Sentinel AI** es una aplicación web e industrial que integra un modelo de Machine Learning supervisado con un backend robusto de baja latencia y un dashboard interactivo premium, diseñada para predecir, clasificar y explicar la probabilidad de riesgo de estafas en transacciones bancarias en tiempo real.

---

## 👥 Equipo de Desarrollo / Autores

Este proyecto ha sido desarrollado e implementado por el siguiente equipo:

*   **Juan Sebastian Gomez Forero**
*   **Gabriel Felipe Garzon Daza**
*   **Hawi Daniel Acevedo Sanchez**
*   **Andres Santiago Jimenez Guzman**
*   **Edison Santiago Gómez Anzola**

---

## 🚀 Guía de Inicio Rápido: Cómo Levantar el Proyecto

Sigue estos pasos sencillos para instalar las dependencias y poner en marcha el servidor API y el Frontend interactivo en tu entorno local:

### Requisitos Previos
*   Tener **Python 3.10 o superior** instalado en tu sistema operativo.
*   El archivo del modelo entrenado y serializado (`model.pkl`) debe estar en la carpeta raíz del proyecto.

### Paso 1: Crear e iniciar el entorno virtual (Recomendado)
Para mantener las dependencias aisladas y no alterar la instalación de Python de tu sistema, crea un entorno virtual `.venv` ejecutando en la terminal:

```bash
# Crear el entorno virtual
python3 -m venv .venv

# Activar el entorno virtual (Linux/macOS)
source .venv/bin/activate

# Activar el entorno virtual (Windows PowerShell)
# .venv\Scripts\Activate.ps1
```

### Paso 2: Instalar las dependencias
Instala todas las librerías necesarias con el instalador de paquetes `pip` utilizando el archivo `requirements.txt` provisto:

```bash
pip install -r requirements.txt
```

*Las dependencias principales instaladas son:*
*   `Flask` (Servidor web y API ligera).
*   `Flask-Cors` (Control de llamadas asíncronas cruzadas).
*   `pandas` (Manipulación y estructuración de matrices de entrada).
*   `scikit-learn` (Carga y ejecución del bosque aleatorio entrenado).

### Paso 3: Levantar el Backend y Servidor de Aplicación
Ejecuta el archivo principal `app.py` usando el intérprete de tu entorno virtual:

```bash
python app.py
```

Al iniciar, verás en la consola la confirmación del cargado exitoso:
```text
✅ Modelo cargado exitosamente.
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Paso 4: ¡Acceder a la Aplicación Web!
Una vez levantado el servidor, abre tu navegador web favorito e ingresa a la siguiente dirección URL:

👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 📊 ¿Cómo Funciona la Inteligencia Artificial de Sentinel AI?

El núcleo predictivo del sistema está basado en un **Clasificador de Bosque Aleatorio** (`RandomForestClassifier`), un algoritmo de aprendizaje supervisado de ensamble que combina múltiples árboles de decisión para mitigar el sobreajuste y entregar predicciones consistentes.

### Mitigación del Desbalance mediante `class_weight='balanced'`
En la vida real, menos del 0.2% de las transacciones son fraudes. Para evitar que el modelo ignore las estafas y se incline por aprobar todo (sesgo de clase mayoritaria), se configuró el hiperparámetro `class_weight='balanced'`. Esto asigna automáticamente pesos de aprendizaje más pesados a la clase minoritaria ("Fraude"), penalizando severamente los errores cometidos en la detección de estafas, forzando así al modelo a capturar los patrones sospechosos clave.

### Glosario e Interpretación de los Campos de Entrada
Para realizar un análisis manual de transferencia, debes diligenciar 7 métricas determinantes en el panel de control:

1.  **Monto de Transferencia (`amount`):**  
    *   *Qué representa:* El valor numérico decimal en dólares de la transferencia en curso.
    *   *Por qué importa:* Las transferencias de montos inusualmente altos disparan de inmediato el riesgo del modelo.
2.  **Hora del Día (`hour`):**  
    *   *Qué representa:* La hora en formato militar (0 a 23, donde 0 es medianoche).
    *   *Por qué importa:* Los ciberdelincuentes operan prioritariamente en horas de la madrugada (1 AM a 5 AM) para retrasar la reacción de la víctima y el banco.
3.  **Día de la Semana (`day_of_week`):**  
    *   *Qué representa:* Día de ejecución codificado numéricamente de 0 a 6 (donde 0 = Lunes, 1 = Martes ... 6 = Domingo).
    *   *Por qué importa:* Permite rastrear la desviación en los patrones de consumo habituales en días laborables vs. fines de semana.
4.  **Transacciones Últimas 24 Horas (`transactions_last_24h`):**  
    *   *Qué representa:* La cantidad de movimientos realizados con la misma cuenta en el último día.
    *   *Por qué importa:* Los ataques de fraude suelen drenar los fondos del usuario rápidamente mediante múltiples compras consecutivas en ráfaga (*Velocity Attacks*).
5.  **Promedio Gasto Usuario (`avg_amount_user`):**  
    *   *Qué representa:* La línea base de consumo promedio histórico en transacciones legítimas del cliente.
    *   *Por qué importa:* Si la transferencia actual desvía drásticamente este promedio (ej. el promedio es $20 y se intentan transferir $3,000), el modelo activa señales de alarma críticas.
6.  **Distancia del Hogar (`distance_from_home`):**  
    *   *Qué representa:* La distancia geográfica medida en kilómetros (km) entre el punto de venta o terminal y el domicilio declarado del usuario.
    *   *Por qué importa:* Compras realizadas a miles de kilómetros del hogar del usuario sugieren de forma inminente clonación de tarjetas.
7.  **Tipo de Cobertura (`is_international`):**  
    *   *Qué representa:* Mapeo binario de geolocalización (0 = Nacional/Local, 1 = Internacional/Transfronteriza).
    *   *Por qué importa:* Los canales internacionales son sumamente explotados por estafadores para evadir regulaciones financieras locales y dificultar el rastreo de fondos.

---

## 🔎 Motor de Explicabilidad (Explainable AI - XAI): "El Por Qué"

El software incorpora una capa heurística de **Explicabilidad Dinámica**. Al presionar **"Analizar con Machine Learning"**, el frontend se conecta de manera asíncrona con el backend Flask para procesar la probabilidad matemática. A continuación, el motor analiza tus entradas de forma interpretativa y desglosa en la sección **"¿Por qué este diagnóstico?"** las razones lógicas asociadas:

*   **Si el monto se desvía del promedio:** Te alertará cuántas veces supera el valor actual al promedio habitual de tus consumos.
*   **Si la distancia es inusual:** Te indicará si la ubicación en kilómetros se sale del perímetro seguro.
*   **Si el horario es de alto riesgo:** Señalará si la madrugada representa un factor de peligro para la autorización automática.
*   **Si la frecuencia es alarmante:** Te indicará si hay comportamiento sospechoso de ráfaga (*Velocity Abuse*).
