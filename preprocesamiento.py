import pandas as pd
from sklearn.preprocessing import StandardScaler

def limpiar_datos(df):
    # Eliminar columnas irrelevantes o duplicadas
    df_cleaned = df.drop(['PersonalInfoId', 'UserId'], axis=1)
    return df_cleaned

def manejar_valores_faltantes(df):
    # Manejar valores faltantes rellenándolos con la media o la mediana
    df_filled = df.fillna(df.mean())
    return df_filled

def normalizar_caracteristicas(df):
    # Normalizar características utilizando la estandarización
    scaler = StandardScaler()
    df_normalized = scaler.fit_transform(df)
    return df_normalized
