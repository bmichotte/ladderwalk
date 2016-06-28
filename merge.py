import sqlite3 
import glob

con = sqlite3.connect("merged.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS grid(target_rank INT, winp REAL, stars INT, bonus INT, games REAL, sem REAL)")

for path in glob.glob('*/*/grid.db'):
    con_i = sqlite3.connect(path)
    cur_i = con_i.cursor()
    
    cur_i.execute("SELECT target_rank,winp,stars,bonus,games,sem FROM grid")
    for line in cur_i.fetchall():
        target_rank, winp, star, bonus, games, sem = line

        cur.execute("INSERT INTO grid VALUES(?, ?, ?, ?, ?, ?)", (target_rank, winp, star, bonus, games,sem))

    con_i.close()

con.commit()
con.close()

