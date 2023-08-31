import pandas as pd
import sqlite3

# db에 csv 파일 저장
df = pd.read_csv("./exercise/machine_learning/exercise.csv", encoding='CP949')

database = "db.sqlite3"
conn = sqlite3.connect(database)
dtype = {
    'ex_name' : "CharField",
    'ex_part' : "CharField",
    'ex_method' : "TextField",
    'ex_video1' : "TextField",
    'ex_video2' : "TextField",
}

df.to_sql(name="exercise_exercise", con=conn, if_exists='replace', dtype=dtype, index=True, index_label="id")
conn.close()
