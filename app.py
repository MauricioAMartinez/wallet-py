from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sqlalchemy import create_engine, text

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "http://localhost:4200"}})

def obtener_datos(personal_info_id):
    engine = create_engine('mysql+mysqlconnector://root:12345@mysql-container/walletApIa')
    connection = engine.connect()

    sql_query = text("""
        SELECT ia.MotivoSolicitud, ia.NivelEducativo, ia.EstadoCivil, ia.DependientesFinancieros,
               hc.Puntuacion, hc.LimiteCredito, hc.NumeroTarjetasPosecion, hc.AntiguedadCuentas,
               fi.IngresosMensuales, tt.Nombre AS Tipotrabajos, fi.AntiguedadEmpleo, fi.GastosMensuales
        FROM InformacionAdicional ia
        JOIN HistorialCrediticio hc ON ia.PersonalInfoId = hc.PersonalInfoId
        JOIN FinancieraInfo fi ON ia.PersonalInfoId = fi.PersonalInfoId
        JOIN Tipotrabajos tt ON fi.TipoTrabajoId = tt.TipoTrabajoId
        WHERE ia.PersonalInfoId = :personal_info_id
    """)

    result = connection.execute(sql_query.params(personal_info_id=personal_info_id))
    df = pd.DataFrame(result.fetchall(), columns=result.keys())
    connection.close()

    return df

@app.route('/predict', methods=['GET'])
def predict():
    personal_info_id = request.args.get('id')
    
    if not personal_info_id:
        return jsonify({"error": "No se proporcionó el id"}), 400

    try:
        personal_info_id = int(personal_info_id)
    except ValueError:
        return jsonify({"error": "El id debe ser un número entero"}), 400

    df = obtener_datos(personal_info_id)

    if df.empty:
        return jsonify({"error": "No se encontraron datos para el id proporcionado"}), 404

    # Simular más datos para entrenamiento
    if len(df) < 10:
        df = pd.concat([df]*10, ignore_index=True)

    # Convertir las características categóricas a numéricas usando LabelEncoder
    le = LabelEncoder()
    df['MotivoSolicitud'] = le.fit_transform(df['MotivoSolicitud'])
    df['NivelEducativo'] = le.fit_transform(df['NivelEducativo'])
    df['EstadoCivil'] = le.fit_transform(df['EstadoCivil'])
    df['Tipotrabajos'] = le.fit_transform(df['Tipotrabajos'])

    # Añadir una columna objetivo aleatoria (en un caso real, esta sería proporcionada)
    df["TarjetaCredito"] = np.random.choice([0, 1], size=len(df))

    # Separar características y objetivo
    X = df.drop('TarjetaCredito', axis=1)
    y = df['TarjetaCredito']

    # Dividir en conjunto de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Crear el modelo
    model = RandomForestClassifier(random_state=42)

    # Entrenar el modelo
    model.fit(X_train, y_train)

    # Hacer una predicción con los datos originales
    prediction = model.predict(X.head(1))
    predictBolean = False
    resultado = 'Tarjeta esta aprobada' if prediction[0] == 1 else 'Tarjeta no fue aprobada'
    predictBolean = True if prediction[0] == 1 else False

    return jsonify({
        "personal_info_id": personal_info_id,
        "prediction": resultado,
        "predicBolean": predictBolean
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

