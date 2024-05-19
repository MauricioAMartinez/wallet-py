import pandas as pd
from sklearn.linear_model import LogisticRegression

# Datos de ejemplo con dos clases
data = {
    "MotivoSolicitud": ["Compras diarias", "Entretenimiento", "Compras diarias", "Entretenimiento"],
    "NivelEducativo": ["Universitario", "Universitario", "Universitario", "Universitario"],
    "EstadoCivil": ["Casado", "Soltero", "Casado", "Soltero"],
    "DependientesFinancieros": [2, 1, 1, 3],
    "Puntuacion": [750, 600, 650, 700],
    "AntiguedadCuentas": [10, 5, 7, 8],
    "IngresosMensuales": [5000, 4000, 3000, 6000],
    "TipoTrabajo": ["Tiempo Completo", "Medio Tiempo", "Tiempo Completo", "Tiempo Completo"],
    "AntiguedadEmpleo": [10, 3, 5, 8],
    "GastosMensuales": [2000, 1500, 3000, 2500],
    "EsApto": [1, 0, 0, 0]  # Dos clases: 1 para apto, 0 para no apto
}

# Convierte los datos en un DataFrame
df = pd.DataFrame(data)

# Características (X) y etiqueta (y)
X = df[["IngresosMensuales", "GastosMensuales"]]
y = df["EsApto"]

# Inicializa el modelo
modelo = LogisticRegression()

# Ajusta el modelo a los datos
modelo.fit(X, y)

# Realiza una predicción para determinar si es apto o no
prediccion = modelo.predict(X)

# Imprime la predicción
print("Predicción:", prediccion)
# Mapeo de etiquetas predichas a texto
prediccion_texto = ["No Apto" if p == 0 else "Apto" for p in prediccion]
# Mapeo de etiquetas predichas a texto
prediccion_texto = ["No Apto" if p == 0 else "Apto" for p in prediccion]

# Imprimir resultados
aptos = sum(1 for p in prediccion if p == 1)

print("Cantidad de instancias aptas:", aptos)

if aptos >= 3:
    print("Es viable que acceda a una tarjeta.")
else:
    print("No es viable que acceda a una tarjeta.")
