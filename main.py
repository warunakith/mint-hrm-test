import pymysql
import os
from flask import Flask, jsonify

app = Flask(__name__)

# Get database credentials from environment variables (for Docker compatibility)
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysqlCon")  # Use the container name as the hostname
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "mintdb")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "mint-test-123")

def get_customer_list():
    """
    Connects to a MySQL database using pymysql, retrieves a list of customers,
    and returns it as a list of dictionaries.
    """
    connection = None  # Initialize connection variable

    try:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            db=MYSQL_DATABASE,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            cursorclass=pymysql.cursors.DictCursor  # Crucial: Return results as dictionaries
        )

        with connection.cursor() as cursor:  # Use "with" for automatic connection closing
            cursor.execute("SELECT * FROM Customers")  # Replace "Customers" with your table name
            customers = cursor.fetchall()  # Returns a list of dictionaries

        return customers

    except pymysql.MySQLError as e:
        print("Error while connecting to MySQL:", e)
        return None  # Or raise the exception

    finally:
        if connection is not None:  # Ensure connection exists before closing
            connection.close()
            print("MySQL connection is closed")



@app.route('/customers', methods=['GET'])
def list_customers():
    """
    API endpoint to retrieve the customer list.
    """
    customers = get_customer_list()
    if customers:
        return jsonify(customers)  # Return as JSON
    else:
        return jsonify({"message": "Could not retrieve customers"}), 500  # Error response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 8000)))
