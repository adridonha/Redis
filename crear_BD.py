import mysql.connector
import psycopg2

# SQL de tablas (MySQL/MariaDB)

SQL_TABLAS = """
CREATE TABLE IF NOT EXISTS Familias (
    id_familia INT AUTO_INCREMENT PRIMARY KEY,
    nombre_tutor VARCHAR(100),
    telefono_contacto VARCHAR(50),
    correo_electronico VARCHAR(100),
    direccion VARCHAR(200),
    situacion_laboral VARCHAR(100),
    nivel_educativo_tutor VARCHAR(100),
    ingresos_aprox DECIMAL(10,2)
);

CREATE TABLE IF NOT EXISTS Profesorado (
    id_profesor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    apellidos VARCHAR(100),
    especialidad VARCHAR(100),
    correo_institucional VARCHAR(100),
    telefono_contacto VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Cursos (
    id_curso INT AUTO_INCREMENT PRIMARY KEY,
    nombre_curso VARCHAR(100),
    nivel_educativo VARCHAR(100),
    tutor INT,
    anio_escolar VARCHAR(20),
    FOREIGN KEY (tutor) REFERENCES Profesorado(id_profesor)
);

CREATE TABLE IF NOT EXISTS Alumnos (
    id_alumno INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    apellidos VARCHAR(100),
    fecha_nacimiento DATE,
    genero VARCHAR(20),
    direccion VARCHAR(200),
    id_familia INT,
    id_curso INT,
    estado_escolar VARCHAR(50),
    FOREIGN KEY (id_familia) REFERENCES Familias(id_familia),
    FOREIGN KEY (id_curso) REFERENCES Cursos(id_curso)
);

CREATE TABLE IF NOT EXISTS Asignaturas (
    id_asignatura INT AUTO_INCREMENT PRIMARY KEY,
    nombre_asignatura VARCHAR(100),
    id_profesor INT,
    id_curso INT,
    horas_semanales INT,
    FOREIGN KEY (id_profesor) REFERENCES Profesorado(id_profesor),
    FOREIGN KEY (id_curso) REFERENCES Cursos(id_curso)
);

CREATE TABLE IF NOT EXISTS Calificaciones (
    id_calificacion INT AUTO_INCREMENT PRIMARY KEY,
    id_alumno INT,
    id_asignatura INT,
    trimestre INT,
    nota DECIMAL(5,2),
    observacion_docente TEXT,
    FOREIGN KEY (id_alumno) REFERENCES Alumnos(id_alumno),
    FOREIGN KEY (id_asignatura) REFERENCES Asignaturas(id_asignatura)
);

CREATE TABLE IF NOT EXISTS Asistencia (
    id_asistencia INT AUTO_INCREMENT PRIMARY KEY,
    id_alumno INT,
    fecha DATE,
    estado VARCHAR(20),
    observacion TEXT,
    FOREIGN KEY (id_alumno) REFERENCES Alumnos(id_alumno)
);

CREATE TABLE IF NOT EXISTS Incidencias (
    id_incidencia INT AUTO_INCREMENT PRIMARY KEY,
    id_alumno INT,
    tipo_incidencia VARCHAR(100),
    descripcion TEXT,
    fecha DATE,
    id_profesor INT,
    FOREIGN KEY (id_alumno) REFERENCES Alumnos(id_alumno),
    FOREIGN KEY (id_profesor) REFERENCES Profesorado(id_profesor)
);

CREATE TABLE IF NOT EXISTS Zonas (
    id_zona INT AUTO_INCREMENT PRIMARY KEY,
    nombre_zona VARCHAR(100),
    nivel_renta_promedio DECIMAL(10,2),
    tasa_desempleo DECIMAL(5,2),
    numero_entidades_apoyo INT
);

CREATE TABLE IF NOT EXISTS Servicios_Sociales (
    id_servicio INT AUTO_INCREMENT PRIMARY KEY,
    nombre_entidad VARCHAR(100),
    tipo_servicio VARCHAR(100),
    contacto VARCHAR(100),
    id_zona INT,
    FOREIGN KEY (id_zona) REFERENCES Zonas(id_zona)
);

CREATE TABLE IF NOT EXISTS Intervenciones (
    id_intervencion INT AUTO_INCREMENT PRIMARY KEY,
    id_alumno INT,
    id_servicio INT,
    tipo_intervencion VARCHAR(100),
    fecha_inicio DATE,
    fecha_fin DATE,
    resultado VARCHAR(100),
    FOREIGN KEY (id_alumno) REFERENCES Alumnos(id_alumno),
    FOREIGN KEY (id_servicio) REFERENCES Servicios_Sociales(id_servicio)
);
"""

# Función para MySQL/MariaDB

def crear_mysql_mariadb(host, port, user, password):
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        port=port
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS absentismo_db;")
    cursor.execute("USE absentismo_db;")
    for stmt in SQL_TABLAS.split(";"):
        if stmt.strip():
            cursor.execute(stmt)
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Base de datos creada en {host}:{port}")

# Función para PostgreSQL

def crear_postgres():
    # Conectamos al servidor para crear DB
    conn = psycopg2.connect(
        host='localhost',
        user='admin',
        password='admin123',
        port=5433,
        database='postgres'
    )
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("DROP DATABASE IF EXISTS absentismo_db;")
    cursor.execute("CREATE DATABASE absentismo_db;")
    cursor.close()
    conn.close()

    # Conectamos a la nueva DB para crear tablas
    conn = psycopg2.connect(
        host='localhost',
        user='admin',
        password='admin123',
        database='absentismo_db',
        port=5433
    )
    cursor = conn.cursor()
    for stmt in SQL_TABLAS.split(";"):
        if stmt.strip():
            # Adaptar AUTO_INCREMENT a SERIAL
            stmt_pg = stmt.replace("INT AUTO_INCREMENT PRIMARY KEY", "SERIAL PRIMARY KEY")
            stmt_pg = stmt_pg.replace("DECIMAL(10,2)", "NUMERIC(10,2)")
            cursor.execute(stmt_pg)
    conn.commit()
    cursor.close()
    conn.close()
    print("Base de datos PostgreSQL creada en localhost:5433")

# Ejecutar todo

if __name__ == "__main__":
    crear_mysql_mariadb('localhost', 3307, 'root', 'admin123')
    crear_mysql_mariadb('localhost', 3308, 'root', 'admin123')
    crear_postgres()
    print("¡Todas las bases de datos creadas correctamente!")