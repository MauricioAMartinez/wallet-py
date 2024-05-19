from sqlalchemy import create_engine, text
import pandas as pd

# Establece la conexión a la base de datos
engine = create_engine('mysql+mysqlconnector://root:@localhost/walletApIa')

# Conecta y obtén una conexión
connection = engine.connect()


# Consulta para obtener los datos de la tabla PersonalInfo
sql_query_personal_info = text("SELECT * FROM PersonalInfos")
result_personal_info = connection.execute(sql_query_personal_info)
df_personal_info = pd.DataFrame(result_personal_info.fetchall(), columns=result_personal_info.keys())


# Consulta para obtener los datos de la tabla FinancieraInfo
sql_query_financiera_info = text("SELECT * FROM FinancieraInfo")
result_financiera_info = connection.execute(sql_query_financiera_info)
df_financiera_info = pd.DataFrame(result_financiera_info.fetchall(), columns=result_financiera_info.keys())

# Consulta para obtener los datos de la tabla HistorialCrediticio
sql_query_historial_crediticio = text("SELECT * FROM HistorialCrediticio")
result_historial_crediticio = connection.execute(sql_query_historial_crediticio)
df_historial_crediticio = pd.DataFrame(result_historial_crediticio.fetchall(), columns=result_historial_crediticio.keys())

# Consulta para obtener los datos de la tabla InformacionAdicional
sql_query_informacion_adicional = text("SELECT * FROM InformacionAdicional")
result_informacion_adicional = connection.execute(sql_query_informacion_adicional)
df_informacion_adicional = pd.DataFrame(result_informacion_adicional.fetchall(), columns=result_informacion_adicional.keys())



# Consulta para obtener los datos de la tabla CardsUser
sql_query_cards_user = text("SELECT * FROM CardsUser")
result_cards_user = connection.execute(sql_query_cards_user)
df_cards_user = pd.DataFrame(result_cards_user.fetchall(), columns=result_cards_user.keys())


print("Datos de la tabla PersonalInfo:")
print(df_personal_info)

print("Datos de la tabla FinancieraInfo:")
print(df_financiera_info)

print("Datos de la tabla HistorialCrediticio:")
print(df_historial_crediticio)

print("Datos de la tabla InformacionAdicional:")
print(df_informacion_adicional)


print("Datos de la tabla CardsUser:")
print(df_cards_user)

# Cierra la conexión
connection.close()
