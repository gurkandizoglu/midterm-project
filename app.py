from flask import Flask, jsonify
import os
import psycopg2
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app = Flask(__name__)

VAULT_URL = os.environ["VAULT_URL"]

@app.route('/hello', methods=['GET'])
def hello():
    try:
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=VAULT_URL, credential=credential)

        db_host = client.get_secret("db-host").value
        db_name = client.get_secret("db-name").value
        db_user = client.get_secret("db-user").value
        db_password = client.get_secret("db-password").value

        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            sslmode='require'
        )
        
        
        cur = conn.cursor()
        cur.execute('SELECT version();')
        db_version = cur.fetchone()
        cur.close()
        conn.close()

        return jsonify({
            "message": "Hello! Connection is Successfull to database via KeyVault password.",
            "db_version": db_version[0]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)