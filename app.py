from pathlib import Path

import joblib
from flask import Flask, render_template, request

app = Flask(__name__)

ruta_modelo = Path(__file__).with_name("studybot_model.joblib")
archivo = joblib.load(ruta_modelo)
columnas = archivo["columnas"]


def predecir_apto(valores):
    fila = [valores[columna] for columna in columnas]
    clase = int(archivo["modelo"].predict([fila])[0])
    return {0: "NO APTO", 1: "APTO"}[clase]


@app.route("/", methods=["GET", "POST"])
def inicio():
    entradas = {}
    resultado = None
    error = None

    if request.method == "POST":
        entradas = {
            columna: request.form.get(columna, "").strip()
            for columna in columnas
        }

        if any(valor not in ("0", "1") for valor in entradas.values()):
            error = "Ingresa 0 o 1 en cada campo."
        else:
            valores = {columna: int(valor) for columna, valor in entradas.items()}
            resultado = predecir_apto(valores)

    return render_template(
        "index.html",
        columnas=columnas,
        entradas=entradas,
        resultado=resultado,
        error=error,
    )