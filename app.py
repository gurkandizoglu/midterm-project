from flask import Flask, jsonify
import os
import psycopg2
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app = Flask(__name__)


VAULT_URL = "https://kv-midterm-g5-124273.vault.azure.net/"
DB_HOST = "gvo14-mid.postgres.database.azure.com"
DB_NAME = "postgres"
DB_USER = "psqladmin"

@app.route('/hello', methods=['GET'])
def hello():
    try:
        
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=VAULT_URL, credential=credential)
        db_password = client.get_secret("db-password").value

        
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=db_password,
            sslmode='require'
        )
        
        
        cur = conn.cursor()
        cur.execute('SELECT version();')
        db_version = cur.fetchone()
        cur.close()
        conn.close()

        return jsonify({
            "message": "Hello! Veritabanına KeyVault şifresiyle başarıyla bağlanıldı.",
            "db_version": db_version[0]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)