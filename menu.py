#!/usr/bin/env python3
"""
Author: Joshua Singh

"""

from flask import Flask, render_template, request, redirect
import argparse
import sqlite3
import csv

app = Flask(__name__)
DB_FILE = 'data.csv'
data = {}

debug = False
verbose = False

def load_data_sql():
    try:
        # Connect to DB and create a cursor
        sqliteConnection = sqlite3.connect('sql.db')
        cursor = sqliteConnection.cursor()
        print('DB Init')
    
        # Write a query and execute it with cursor
        query = 'select sqlite_version();'
        cursor.execute(query)
    
        # Fetch and output result
        result = cursor.fetchall()
        print('SQLite Version is {}'.format(result))
    
        # Close the cursor
        cursor.close()
    
    # Handle errors
    except sqlite3.Error as error:
        print('Error occurred - ', error)
    
    # Close DB Connection irrespective of success
    # or failure
    finally:
    
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection closed')

def load_data_csv():
  global data
  with open(DB_FILE, 'r') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames

    none_text = ('section', 'item_name')

    for row in reader:
        if verbose:
           print(headers)
           print(row)
        section = row['section'].lower()
        if section not in data:
            data[section] = {
               "items": [],
                "price_header": []
                }
            #data[section]['price_header'] = [[h for h in headers if h not in none_text]]
        item = {}


        for entry in row:
            if entry == 'section':
                continue
            if row[entry]:
                item[entry] = row[entry]
                
                if entry == 'second_text':
                   entry = " "

                if entry not in none_text and entry not in data[section]['price_header']:
                   data[section]['price_header'].append(entry)
            


        data[section]["items"].append(item)

def data_dump():
  global data
  with open(DB_FILE, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "ID", "URL"])
    for id, entry in data.items():
      writer.writerow([entry["name"], id, entry.get("URL", "")])


@app.route('/')
def customer_display():
    return render_template('display.html', data=data, debug=debug)

@app.route('/admin')
def admin_page():
    return render_template('admin.html', data=data)

@app.route('/update_item', methods=["POST"])
def update_item():
    item = request.form

    print(item)
    return redirect('/admin')

def main():

    parser = argparse.ArgumentParser(description='Cool script description here.')
    parser.add_argument("-v", "--verbose", action="count", default=0, help="increase output verbosity")

    parser.add_argument("-d", "--debug", action="count", default=0, help="Add debug content to webpage")

    args = parser.parse_args()

    if args.debug > 0:
       global debug 
       debug = True
    
    if args.verbose > 0:
       global verbose
       verbose = True
    
    load_data_csv()
    #print(data)
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()