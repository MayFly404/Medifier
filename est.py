@app.route('/proccess_feeling', methods=['POST'])
def feeling():
    feeling = request.form['feeling']
    database = "databases/users.db"
    conn = create_connection(database)
    if conn is not None:
        create_table(conn)
    else:
        entry_text = input("Enter your journal entry for today: ")
        try:
            response = model.generate_content(f"If {feeling} is considered bad or vulgar, output the word 'flagged'. If not, output the word 'pass'.")
            flag_or_not = response.text
        except:
            flag_or_not = "flagged"

    write_entry(conn, feeling, entry_text)

    print("Journal entry added successfully.")

    print("Previous Entries:")
    read_entries(conn, feeling)

    conn.close()

    return render_template("feelings_response.html")
