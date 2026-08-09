from flask import Flask, jsonify
import os
import psycopg2

# TODO: Import your database connector here - DONE

app = Flask(__name__)

# TODO: Configure database connection using os.getenv('DATABASE_URL') - DONE
def get_db_connection():
    return psycopg2.connect(os.getenv('DATABASE_URL'))

@app.route('/api/inventory/alerts', methods=['GET'])
def get_alerts():
    """
    Return all inventory products where quantity is less than
    or equal to the reorder level.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id, product_name, quantity, reorder_level
            FROM inventory
            WHERE quantity <= reorder_level
        """)

        rows = cursor.fetchall()

        alerts = [
            {
                "id": str(row[0]),
                "product_name": row[1],
                "quantity": row[2],
                "reorder_level": row[3]
            }
            for row in rows
        ]

        return jsonify(alerts), 200

    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
