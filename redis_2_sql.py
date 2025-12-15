import mysql.connector
import redis
import json
from datetime import date

# Redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# MySQL / MariaDB
conn = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="root",
    password="admin123",
    database="absentismo_db"
)
cursor = conn.cursor()

print("\n22. Obtener datos desde Redis e incluirlos en SQL")

# Crear tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS Riesgo_Absentismo (
    id_riesgo INT AUTO_INCREMENT PRIMARY KEY,
    id_alumno INT,
    nombre VARCHAR(100),
    apellidos VARCHAR(100),
    curso VARCHAR(100),
    faltas INT,
    fecha_registro DATE
)
""")

# Leer Redis
for key in r.keys("sql_alumno:*"):
    alumno = json.loads(r.get(key))

    cursor.execute("""
    INSERT INTO Riesgo_Absentismo 
    (id_alumno, nombre, apellidos, curso, faltas, fecha_registro)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        alumno["id_alumno"],
        alumno["nombre"],
        alumno["apellidos"],
        alumno["nombre_curso"],
        alumno["faltas"],
        date.today()
    ))

    print("Insertado en SQL:", alumno)

conn.commit()
cursor.close()
conn.close()
