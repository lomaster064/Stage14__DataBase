import sqlite3

connection = sqlite3.connect("not_telegram.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER,
    balance INTEGER NOT NULL)
''')

# for i in range(1, 11):
#     cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?,?,?,?)", (f"User{i}", f"example{i}@gmail.com", i*10, 1000))

# cursor.execute("UPDATE Users set balance = 500 where id % 2 = ?", (1,))

# cursor.execute("DELETE FROM Users WHERE id % 3 = ?", (1,))

# cursor.execute('SELECT * FROM Users WHERE age != ?', (60,))
#
# data = cursor.fetchall()
#
# for row in data:
#     print(f'Имя: {row[1]} | Почта: {row[2]} | Возраст: {row[3]} | Баланс: {row[4]}')

cursor.execute('DELETE FROM Users WHERE id = ?', (6,))

cursor.execute('SELECT COUNT(*) FROM Users')
# print(f'Общее количество записей: {cursor.fetchone()[0]}')

cursor.execute('SELECT SUM(balance) FROM Users')
# print(f'Сумма всех балансов: {cursor.fetchone()[0]}')

cursor.execute('SELECT AVG(balance) FROM Users')
print(f'Средний баланс: {cursor.fetchone()[0]}')

connection.commit()
connection.close()