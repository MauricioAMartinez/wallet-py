from sklearn.model_selection import cross_val_score, LeaveOneOut
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np

# Lee los datos desde tu archivo main.py o donde los tengas almacenados
from sqlalchemy import create_engine, text

engine = create_engine('mysql+mysqlconnector://root:root@localhost/walletApIa')
connection = engine.connect()
personal_info_id = 2 

def obtener_datos(personal_info_id):
    engine = create_engine('mysql+mysqlconnector://root:root@localhost/walletApIa')
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
    print(df)
    # Simular columna "EsApto" con valores aleatorios (0 o 1) para propósitos de prueba
    df['EsApto'] = np.random.randint(2, size=len(df))

    connection.close()

    return df

# Obtener los datos
df = obtener_datos(personal_info_id)