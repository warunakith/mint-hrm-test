import pymysql
import os
from flask import Flask, jsonify

app = Flask(__name__)


def get_customer_list():
    MYSQL_HOST = "localhost"
    MYSQL_DATABASE = "mintdb"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "mint-test-123"

    """
    Connects to a MySQL database using pymysql, retrieves a list of customers,
    and returns it as a list of dictionaries.
    """
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
        print("Error while connecting to MySQL", e)
        return None  # Or raise the exception

    finally:
        if connection:
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

