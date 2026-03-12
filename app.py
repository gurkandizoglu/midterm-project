from flask import Flask, jsonify
import os
import psycopg2
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    # Azure KeyVault ve PostgreSQL bağlantı kodları sonraki adımlarda buraya eklenecek 
    return jsonify({"message": "Hello! Altyapı kurulumları bekleniyor."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)