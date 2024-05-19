from sqlalchemy import create_engine, text
import pandas as pd

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
