from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
DATABASE = 'mice.db'  # Ensure this path is correct

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mice")
    columns = [column[0] for column in cursor.description]
    conn.close()
    return render_template('upload.html', columns=columns)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    conn = get_db()
    cursor = conn.cursor()
    sort_by = request.args.get('sort_by')
    print(f"sort_by value: {sort_by}") # Debugging print
    
    sql = "SELECT * FROM mice"
    if sort_by:
        try:
            # Map the display values to actual column names
            column_map = {
                "сила_кнопки": "button_force",  # Replace with your actual column name
                "макс_dpi": "max_dpi",  # Replace with your actual column name
                "макс_частота": "max_polling_rate"  # Replace with your actual column name
            }
            print(f"column_map: {column_map}") # Debugging print
            sort_column = column_map.get(sort_by)
            if sort_column:
                sql += f" ORDER BY {sort_column}"
                cursor.execute(sql)
            else:
                return render_template('upload.html', error="Invalid sort column.")
        except sqlite3.OperationalError as e:
            print(f"SQL Error: {e}")
            return render_template('upload.html', error="Invalid sort column.")
        except Exception as e:
            print(f"Error: {e}")
            return render_template('upload.html', error="An error occurred during sorting.")
    else:
        cursor.execute(sql)

    mice = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    conn.close()
    return render_template('upload.html', mice=mice, columns=columns)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
