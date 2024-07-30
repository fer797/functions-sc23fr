from flask import Flask, jsonify, request
import pandas as pd
from io import StringIO
from azure.storage.blob import BlobServiceClient
import psycopg2
import os
import json
import requests

app = Flask(__name__)

# Azure Blob Storage configuration
AZURE_STORAGE_CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName=functionssc23fjrl;AccountKey=vMhorVuGfhNEcgMrvqBahCqK7sghX9R/8d6dJXRYpATK0QCheJK+XMfWpTxAco1We9OgJ4q09T2G+AStK9NS3A==;EndpointSuffix=core.windows.net'
AZURE_CONTAINER_NAME = 'datasets'
AZURE_BLOB_NAME = 'dataset.csv'

# PostgreSQL configuration
POSTGRES_HOST = 'sc23fjrl.postgres.database.azure.com'
POSTGRES_DB = 'postgres'
POSTGRES_USER = 'sc23fjrl'
POSTGRES_PASSWORD = 'Recordar$1'
POSTGRES_TABLE = 'Medications'


def get_db_connection():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )


@app.route('/medications', methods=['GET', 'POST', 'PUT', 'DELETE'])
def medications():
    if request.method == 'GET':
        return get_medications()
    elif request.method == 'POST':
        return create_medication()
    elif request.method == 'PUT':
        return update_medication()
    elif request.method == 'DELETE':
        return delete_medication()


def get_medications():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {POSTGRES_TABLE}')
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        medications = [dict(zip(columns, row)) for row in rows]
        
        cursor.close()
        conn.close()
        
        return jsonify(medications), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def create_medication():
    try:
        medication = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        insert_query = f"""
        INSERT INTO {POSTGRES_TABLE} (
            name, substitute0, substitute1, substitute2, substitute3, substitute4,
            sideEffect0, sideEffect1, sideEffect2, sideEffect3, sideEffect4, sideEffect5,
            sideEffect6, sideEffect7, sideEffect8, sideEffect9, sideEffect10, sideEffect11,
            sideEffect12, sideEffect13, use0, use1, use2, use3, use4, Chemical_Class,
            Habit_Forming, Therapeutic_Class, Action_Class
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(insert_query, (
            medication['name'], medication.get('substitute0'), medication.get('substitute1'),
            medication.get('substitute2'), medication.get('substitute3'), medication.get('substitute4'),
            medication.get('sideEffect0'), medication.get('sideEffect1'), medication.get('sideEffect2'),
            medication.get('sideEffect3'), medication.get('sideEffect4'), medication.get('sideEffect5'),
            medication.get('sideEffect6'), medication.get('sideEffect7'), medication.get('sideEffect8'),
            medication.get('sideEffect9'), medication.get('sideEffect10'), medication.get('sideEffect11'),
            medication.get('sideEffect12'), medication.get('sideEffect13'), medication.get('use0'),
            medication.get('use1'), medication.get('use2'), medication.get('use3'), medication.get('use4'),
            medication.get('Chemical Class'), medication.get('Habit Forming'),
            medication.get('Therapeutic Class'), medication.get('Action Class')
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Medication created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def update_medication():
    try:
        medication = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        update_query = f"""
        UPDATE {POSTGRES_TABLE} SET
            name = %s, substitute0 = %s, substitute1 = %s, substitute2 = %s, substitute3 = %s, substitute4 = %s,
            sideEffect0 = %s, sideEffect1 = %s, sideEffect2 = %s, sideEffect3 = %s, sideEffect4 = %s, sideEffect5 = %s,
            sideEffect6 = %s, sideEffect7 = %s, sideEffect8 = %s, sideEffect9 = %s, sideEffect10 = %s, sideEffect11 = %s,
            sideEffect12 = %s, sideEffect13 = %s, use0 = %s, use1 = %s, use2 = %s, use3 = %s, use4 = %s, Chemical_Class = %s,
            Habit_Forming = %s, Therapeutic_Class = %s, Action_Class = %s
        WHERE id = %s
        """
        
        cursor.execute(update_query, (
            medication['name'], medication.get('substitute0'), medication.get('substitute1'),
            medication.get('substitute2'), medication.get('substitute3'), medication.get('substitute4'),
            medication.get('sideEffect0'), medication.get('sideEffect1'), medication.get('sideEffect2'),
            medication.get('sideEffect3'), medication.get('sideEffect4'), medication.get('sideEffect5'),
            medication.get('sideEffect6'), medication.get('sideEffect7'), medication.get('sideEffect8'),
            medication.get('sideEffect9'), medication.get('sideEffect10'), medication.get('sideEffect11'),
            medication.get('sideEffect12'), medication.get('sideEffect13'), medication.get('use0'),
            medication.get('use1'), medication.get('use2'), medication.get('use3'), medication.get('use4'),
            medication.get('Chemical Class'), medication.get('Habit Forming'),
            medication.get('Therapeutic Class'), medication.get('Action Class'),
            medication['id']
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Medication updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def delete_medication():
    try:
        medication_id = request.json['id']
        conn = get_db_connection()
        cursor = conn.cursor()
        
        delete_query = f"DELETE FROM {POSTGRES_TABLE} WHERE id = %s"
        
        cursor.execute(delete_query, (medication_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Medication deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))