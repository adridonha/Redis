"""
Providers de Faker usados:
1. name() -> nombres completos
2. first_name() -> nombres
3. last_name() -> apellidos
4. date_of_birth() -> fecha de nacimiento
5. address() -> dirección completa
6. phone_number() -> teléfono
7. email() -> correo electrónico
8. job() -> ocupación / especialidad
9. company() -> empresa
10. random_int() -> números aleatorios
11. random_element() -> elección aleatoria de listas
12. sentence() -> frases cortas para observaciones
"""

from faker import Faker
import mysql.connector
import psycopg2
import random
from datetime import timedelta

fake = Faker()

# Configuración de conexiones

# MySQL
mysql_conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='admin123',
    database='absentismo_db',
    port=3307
)
mysql_cursor = mysql_conn.cursor()

# MariaDB
mariadb_conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='admin123',
    database='absentismo_db',
    port=3308
)
mariadb_cursor = mariadb_conn.cursor()

# PostgreSQL
pg_conn = psycopg2.connect(
    host='localhost',
    user='admin',
    password='admin123',
    database='absentismo_db',
    port=5433
)
pg_cursor = pg_conn.cursor()

# Funciones para insertar datos

def generar_familia(cursor, es_postgres=False):
    nombre = fake.name()
    telefono = fake.phone_number()
    correo = fake.email()
    direccion = fake.address().replace("\n", ", ")
    situacion = fake.job()
    nivel = random.choice(["Primaria", "Secundaria", "Universidad"])
    ingresos = round(random.randint(10000,50000),2)
    query = """INSERT INTO Familias (nombre_tutor, telefono_contacto, correo_electronico, direccion, situacion_laboral, nivel_educativo_tutor, ingresos_aprox)
               VALUES (%s,%s,%s,%s,%s,%s,%s)"""
    cursor.execute(query,(nombre,telefono,correo,direccion,situacion,nivel,ingresos))
    if es_postgres:
        cursor.execute("SELECT currval(pg_get_serial_sequence('Familias','id_familia'));")
        return cursor.fetchone()[0]
    return cursor.lastrowid

def generar_profesor(cursor, es_postgres=False):
    nombre = fake.first_name()
    apellidos = fake.last_name()
    especialidad = fake.job()
    correo = fake.email()
    telefono = fake.phone_number()
    query = """INSERT INTO Profesorado (nombre, apellidos, especialidad, correo_institucional, telefono_contacto)
               VALUES (%s,%s,%s,%s,%s)"""
    cursor.execute(query,(nombre,apellidos,especialidad,correo,telefono))
    if es_postgres:
        cursor.execute("SELECT currval(pg_get_serial_sequence('Profesorado','id_profesor'));")
        return cursor.fetchone()[0]
    return cursor.lastrowid

def generar_curso(cursor, profesor_id, es_postgres=False):
    nombre_curso = random.choice(["Curso A","Curso B","Curso C"])
    nivel = random.choice(["Primaria","Secundaria","Bachillerato"])
    anio = f"{random.randint(2020,2024)}-{random.randint(2021,2025)}"
    query = """INSERT INTO Cursos (nombre_curso, nivel_educativo, tutor, anio_escolar)
               VALUES (%s,%s,%s,%s)"""
    cursor.execute(query,(nombre_curso,nivel,profesor_id,anio))
    if es_postgres:
        cursor.execute("SELECT currval(pg_get_serial_sequence('Cursos','id_curso'));")
        return cursor.fetchone()[0]
    return cursor.lastrowid

def generar_alumno(cursor,familia_id,curso_id,es_postgres=False):
    nombre = fake.first_name()
    apellidos = fake.last_name()
    fecha = fake.date_of_birth(minimum_age=6, maximum_age=18)
    genero = random.choice(["Masculino","Femenino"])
    direccion = fake.address().replace("\n",", ")
    estado = random.choice(["Activo","Baja temporal","Retirado"])
    query = """INSERT INTO Alumnos (nombre,apellidos,fecha_nacimiento,genero,direccion,id_familia,id_curso,estado_escolar)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
    cursor.execute(query,(nombre,apellidos,fecha,genero,direccion,familia_id,curso_id,estado))
    if es_postgres:
        cursor.execute("SELECT currval(pg_get_serial_sequence('Alumnos','id_alumno'));")
        return cursor.fetchone()[0]
    return cursor.lastrowid

def generar_asignatura(cursor, profesor_id, curso_id, es_postgres=False):
    nombre = random.choice(["Matemáticas","Lengua","Historia","Ciencias","Inglés"])
    horas = random.randint(2,5)
    query = """INSERT INTO Asignaturas (nombre_asignatura,id_profesor,id_curso,horas_semanales)
               VALUES (%s,%s,%s,%s)"""
    cursor.execute(query,(nombre,profesor_id,curso_id,horas))
    if es_postgres:
        cursor.execute("SELECT currval(pg_get_serial_sequence('Asignaturas','id_asignatura'));")
        return cursor.fetchone()[0]
    return cursor.lastrowid

def generar_calificacion(cursor, alumno_id, asignatura_id):
    trimestre = random.randint(1,3)
    nota = round(random.uniform(1,10),2)
    observacion = fake.sentence()
    query = """INSERT INTO Calificaciones (id_alumno,id_asignatura,trimestre,nota,observacion_docente)
               VALUES (%s,%s,%s,%s,%s)"""
    cursor.execute(query,(alumno_id,asignatura_id,trimestre,nota,observacion))

def generar_asistencia(cursor, alumno_id):
    fecha = fake.date_between(start_date='-1y', end_date='today')
    estado = random.choice(["Presente","Ausente","Tarde"])
    observacion = fake.sentence()
    query = """INSERT INTO Asistencia (id_alumno,fecha,estado,observacion)
               VALUES (%s,%s,%s,%s)"""
    cursor.execute(query,(alumno_id,fecha,estado,observacion))

def generar_incidencia(cursor, alumno_id, profesor_id):
    tipo = random.choice(["Falta leve","Falta grave","Retardo"])
    descripcion = fake.sentence()
    fecha = fake.date_between(start_date='-1y', end_date='today')
    query = """INSERT INTO Incidencias (id_alumno,tipo_incidencia,descripcion,fecha,id_profesor)
               VALUES (%s,%s,%s,%s,%s)"""
    cursor.execute(query,(alumno_id,tipo,descripcion,fecha,profesor_id))

def generar_zona(cursor, es_postgres=False):
    nombre = fake.city()
    renta = round(random.randint(15000,70000),2)
    desempleo = round(random.uniform(3,20),2)
    num = random.randint(1,10)
    query = """INSERT INTO Zonas (nombre_zona,nivel_renta_promedio,tasa_desempleo,numero_entidades_apoyo)
               VALUES (%s,%s,%s,%s)"""
    cursor.execute(query,(nombre,renta,desempleo,num))
    if es_postgres:
        cursor.execute("SELECT currval(pg_get_serial_sequence('Zonas','id_zona'));")
        return cursor.fetchone()[0]
    return cursor.lastrowid

def generar_servicio(cursor,zona_id,es_postgres=False):
    nombre = fake.company()
    tipo = random.choice(["Psicológico","Educativo","Social","Salud"])
    contacto = fake.email()
    query = """INSERT INTO Servicios_Sociales (nombre_entidad,tipo_servicio,contacto,id_zona)
               VALUES (%s,%s,%s,%s)"""
    cursor.execute(query,(nombre,tipo,contacto,zona_id))
    if es_postgres:
        cursor.execute("SELECT currval(pg_get_serial_sequence('Servicios_Sociales','id_servicio'));")
        return cursor.fetchone()[0]
    return cursor.lastrowid

def generar_intervencion(cursor,alumno_id,servicio_id):
    tipo = random.choice(["Asesoría","Terapia","Seguimiento"])
    inicio = fake.date_between(start_date='-1y', end_date='today')
    fin = inicio + timedelta(days=random.randint(10,100))
    resultado = random.choice(["Exitoso","Pendiente","Fallido"])
    query = """INSERT INTO Intervenciones (id_alumno,id_servicio,tipo_intervencion,fecha_inicio,fecha_fin,resultado)
               VALUES (%s,%s,%s,%s,%s,%s)"""
    cursor.execute(query,(alumno_id,servicio_id,tipo,inicio,fin,resultado))


# Insertar datos

NUM_REG = 5

for i in range(NUM_REG):
    # Familias
    fam_mysql = generar_familia(mysql_cursor)
    fam_maria = generar_familia(mariadb_cursor)
    fam_pg = generar_familia(pg_cursor, es_postgres=True)

    # Profesorado
    prof_mysql = generar_profesor(mysql_cursor)
    prof_maria = generar_profesor(mariadb_cursor)
    prof_pg = generar_profesor(pg_cursor, es_postgres=True)

    # Cursos
    curso_mysql = generar_curso(mysql_cursor, prof_mysql)
    curso_maria = generar_curso(mariadb_cursor, prof_maria)
    curso_pg = generar_curso(pg_cursor, prof_pg, es_postgres=True)

    # Alumnos
    alum_mysql = generar_alumno(mysql_cursor, fam_mysql, curso_mysql)
    alum_maria = generar_alumno(mariadb_cursor, fam_maria, curso_maria)
    alum_pg = generar_alumno(pg_cursor, fam_pg, curso_pg, es_postgres=True)

    # Asignaturas
    asign_mysql = generar_asignatura(mysql_cursor, prof_mysql, curso_mysql)
    asign_maria = generar_asignatura(mariadb_cursor, prof_maria, curso_maria)
    asign_pg = generar_asignatura(pg_cursor, prof_pg, curso_pg, es_postgres=True)

    # Calificaciones
    generar_calificacion(mysql_cursor, alum_mysql, asign_mysql)
    generar_calificacion(mariadb_cursor, alum_maria, asign_maria)
    generar_calificacion(pg_cursor, alum_pg, asign_pg)

    # Asistencia
    generar_asistencia(mysql_cursor, alum_mysql)
    generar_asistencia(mariadb_cursor, alum_maria)
    generar_asistencia(pg_cursor, alum_pg)

    # Incidencias
    generar_incidencia(mysql_cursor, alum_mysql, prof_mysql)
    generar_incidencia(mariadb_cursor, alum_maria, prof_maria)
    generar_incidencia(pg_cursor, alum_pg, prof_pg)

    # Zonas y Servicios
    zona_mysql = generar_zona(mysql_cursor)
    zona_maria = generar_zona(mariadb_cursor)
    zona_pg = generar_zona(pg_cursor, es_postgres=True)

    serv_mysql = generar_servicio(mysql_cursor, zona_mysql)
    serv_maria = generar_servicio(mariadb_cursor, zona_maria)
    serv_pg = generar_servicio(pg_cursor, zona_pg, es_postgres=True)

    # Intervenciones
    generar_intervencion(mysql_cursor, alum_mysql, serv_mysql)
    generar_intervencion(mariadb_cursor, alum_maria, serv_maria)
    generar_intervencion(pg_cursor, alum_pg, serv_pg)

# Confirmar cambios
mysql_conn.commit()
mariadb_conn.commit()
pg_conn.commit()

# Cerrar conexiones
mysql_cursor.close()
mysql_conn.close()
mariadb_cursor.close()
mariadb_conn.close()
pg_cursor.close()
pg_conn.close()

print("Datos insertados correctamente en MySQL(3306), MariaDB(3307) y PostgreSQL(5433)")