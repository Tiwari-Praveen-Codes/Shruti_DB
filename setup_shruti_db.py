import mysql.connector

def setup_mysql_shruti():
    conn = mysql.connector.connect(host='localhost', user='root', password='Pravin@_123')
    cur = conn.cursor()

    # 1. Create database Shruti_41
    cur.execute("CREATE DATABASE IF NOT EXISTS `Shruti_41` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print("Database `Shruti_41` created/verified.")

    # 2. Create user Shruti_41 with password Pravin@_123
    try:
        cur.execute("CREATE USER IF NOT EXISTS 'Shruti_41'@'localhost' IDENTIFIED BY 'Pravin@_123'")
        cur.execute("GRANT ALL PRIVILEGES ON `Shruti_41`.* TO 'Shruti_41'@'localhost'")
        cur.execute("GRANT ALL PRIVILEGES ON `Shruti_41`.* TO 'root'@'localhost'")
        cur.execute("FLUSH PRIVILEGES")
        print("User 'Shruti_41'@'localhost' created and granted all privileges on `Shruti_41`.*")
    except Exception as e:
        print("User creation note:", e)

    conn.commit()
    conn.close()

    # 3. Initialize all 10 tables in Shruti_41
    with open('schema_mysql.sql', 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # Replace scholartrack_db with Shruti_41
    sql_content = sql_content.replace('scholartrack_db', 'Shruti_41')

    conn_db = mysql.connector.connect(host='localhost', user='root', password='Pravin@_123', database='Shruti_41')
    cur_db = conn_db.cursor()
    for stmt in sql_content.split(';'):
        s = stmt.strip()
        if s:
            cur_db.execute(s)
    conn_db.commit()

    cur_db.execute("SHOW TABLES")
    tables = [t[0] for t in cur_db.fetchall()]
    print(f"All {len(tables)} tables created in `Shruti_41`:")
    for t in tables:
        print(f"  - {t}")

    conn_db.close()

    # 4. Verify connection using user Shruti_41
    conn_user = mysql.connector.connect(host='localhost', user='Shruti_41', password='Pravin@_123', database='Shruti_41')
    cur_user = conn_user.cursor()
    cur_user.execute("SELECT DATABASE(), USER()")
    print("Verification via user Shruti_41:", cur_user.fetchone())
    conn_user.close()

if __name__ == '__main__':
    setup_mysql_shruti()
