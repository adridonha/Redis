import mysql.connector
import redis
import json

# Conexión Redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Conexión MySQL / MariaDB
conn = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="root",
    password="admin123",
    database="absentismo_db"
)
cursor = conn.cursor(dictionary=True)

print("\n21. Obtener datos desde SQL e incluirlos en Redis")

# Consulta SQL: alumnos con número de faltas
consulta = """
SELECT 
    a.id_alumno,
    a.nombre,
    a.apellidos,
    c.nombre_curso,
    COUNT(s.id_asistencia) AS faltas
FROM Alumnos a
JOIN Cursos c ON a.id_curso = c.id_curso
JOIN Asistencia s ON a.id_alumno = s.id_alumno
WHERE s.estado = 'FALTA'
GROUP BY a.id_alumno
"""

cursor.execute(consulta)
resultados = cursor.fetchall()

for alumno in resultados:
    clave = f"sql_alumno:{alumno['id_alumno']}"
    r.set(clave, json.dumps(alumno))
    print("Insertado en Redis:", clave, alumno)

cursor.close()
conn.close()
