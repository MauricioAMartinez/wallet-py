import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import numpy as np
from sqlalchemy import create_engine, text

def obtener_datos(personal_info_id):
    engine = create_engine('mysql+mysqlconnector://root:@localhost/walletApIa')
    connection = engine.connect()

    sql_query = text("""
        SELECT ia.MotivoSolicitud, ia.NivelEducativo, ia.EstadoCivil, ia.DependientesFinancieros,
               hc.Puntuacion, hc.LimiteCredito, hc.NumeroTarjetasPosecion, hc.AntiguedadCuentas,
               fi.IngresosMensuales, tt.Nombre AS TipoTrabajo, fi.AntiguedadEmpleo, fi.GastosMensuales
        FROM InformacionAdicional ia
        JOIN HistorialCrediticio hc ON ia.PersonalInfoId = hc.PersonalInfoId
        JOIN FinancieraInfo fi ON ia.PersonalInfoId = fi.PersonalInfoId
        JOIN TipoTrabajos tt ON fi.TipoTrabajoId = tt.TipoTrabajoId
        WHERE ia.PersonalInfoId = :personal_info_id
    """)

    result = connection.execute(sql_query.params(personal_info_id=personal_info_id))
    df = pd.DataFrame(result.fetchall(), columns=result.keys())
    connection.close()

    return df

# Obtener los datos
personal_info_id = 2
df = obtener_datos(personal_info_id)

# Simular más datos para entrenamiento
if len(df) < 10:
    print("Advertencia: datos insuficientes, simulando datos adicionales para el entrenamiento.")
    df = pd.concat([df]*10, ignore_index=True)

# Convertir las características categóricas a numéricas usando LabelEncoder
le = LabelEncoder()
df['MotivoSolicitud'] = le.fit_transform(df['MotivoSolicitud'])
df['NivelEducativo'] = le.fit_transform(df['NivelEducativo'])
df['EstadoCivil'] = le.fit_transform(df['EstadoCivil'])
df['TipoTrabajo'] = le.fit_transform(df['TipoTrabajo'])

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

# Hacer predicciones
y_pred = model.predict(X_test)

# Evaluar el modelo
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

# Hacer una predicción con los datos originales
prediction = model.predict(X.head(1))
print(f"Predicción para el primer registro: {'Tarjeta aprobada' if prediction[0] == 1 else 'Tarjeta no aprobada'}")
