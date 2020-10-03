import sqlite3

conn = sqlite3.connect('icacard.db')

cur = conn.cursor()

cur.execute("""
        CREATE TABLE students(
            Nom text,
            Prénom text,
            Code text no null primary key,
            Tel integer,
            code_affilié text,
            FOREIGN KEY(code_affilié) REFERENCES users(code)
        )
""")

cur.execute("INSERT INTO students VALUES ('haitam','aouad','E-123',45646,'E-123')")
cur.execute("INSERT INTO students VALUES ('haitam','aouad','E-125',45646,'E-123')")
cur.execute("INSERT INTO students VALUES ('haitam','aouad','E-124',45646,'E-123')")
cur.execute("INSERT INTO students VALUES ('haitam','aouad','E-143',45646,'E-123')")
cur.execute("INSERT INTO students VALUES ('haitam','aouad','E-183',45646,'E-123')")
cur.execute("INSERT INTO students VALUES ('haitam','aouad','E-193',45646,'E-123')")
cur.execute("INSERT INTO students VALUES ('haitam','aouad','E-163',45646,'E-123')")
cur.execute("INSERT INTO students VALUES ('haitam','aouad','E-173',45646,'E-123')")



cur.execute("SELECT * FROM students")
print(cur.fetchall())

conn.commit()
conn.close()