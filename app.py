import logging
import os

import pymysql
from flask import Flask, request

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASS = os.getenv("DB_PASS", "")
DB_NAME = os.getenv("DB_NAME", "legacydb")


@app.route("/")
def home():
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
        )
        conn.close()

        return "<h1>API TechNova - Funcionando</h1>"

    except Exception:
        app.logger.exception("Error al conectar con la base de datos")
        return "<h1>Servicio temporalmente no disponible</h1>", 500


@app.route("/buscar")
def buscar_usuario():
    usuario_id = request.args.get("id", "1")

    try:
        usuario_id = int(usuario_id)
    except ValueError:
        return {"error": "ID inválido"}, 400

    query = "SELECT * FROM usuarios WHERE id = %s"

    return {
        "mensaje": "Consulta preparada correctamente",
        "query": query,
        "id": usuario_id,
    }


@app.route("/health")
def health_check():
    return {"status": "healthy"}, 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=False)