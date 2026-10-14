from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

db_config = {
   'host': 'python312-flask30-mariadb-mariadb.internal',
   'user': 'root',
   'password': 'unikraft',
   'database': 'mysql'
}

def get_data_from_database():
   try:
       connection = mysql.connector.connect(**db_config)
       cursor = connection.cursor()

       # Replace this query with your actual SQL query
       query = "SELECT count(*) FROM user;"
       cursor.execute(query)

       data = cursor.fetchall()

       return data

   except Exception as e:
       print(f"Error: {e}")
       return None

   finally:
       if connection.is_connected():
           cursor.close()
           connection.close()

@app.route('/')
def get_data():
   data = get_data_from_database()

   if data is not None:
       return jsonify({'data': data})
   else:
       return jsonify({'error': 'Failed to retrieve data from the database'})

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8080)
