import redis
import json

# Conectar a Redis
conexionRedis = redis.ConnectionPool(host='localhost',
                                    port=6379,
                                    db=0,
                                    decode_responses=True)
baseDatosRedis = redis.Redis(connection_pool=conexionRedis)

# 1. Crear registros clave-valor
print("\n1. Creando claves...")
for i in range(1, 16):
    clave = f"alumno:{i}"

    alumno = {
        "nombre": f"Alumno{i}",
        "apellido": f"Apellido{i}",
        "curso": "5A" if i <= 7 else "6B",
        "faltas": i % 4,  # número de faltas
        "edad": 10 + (i % 3)  # 10, 11 o 12 años
    }

    # Guardamos el diccionario convertido a JSON
    baseDatosRedis.set(clave, json.dumps(alumno))
# 2. Número de claves
claves = baseDatosRedis.keys("alumno:*")
print("\n2. Número de claves:", len(claves))

# 3. Obtener un registro por clave
print("\n3. Mostrar alumno:2")
print(baseDatosRedis.get("alumno:2"))

# 4. Actualizar un valor
print("\n4. Actualizando faltas del alumno:1 a 4...")
data = json.loads(baseDatosRedis.get("alumno:1"))
data["faltas"] = 4
baseDatosRedis.set("alumno:1", json.dumps(data))
print("Nuevo valor:", baseDatosRedis.get("alumno:1"))

# 5. Eliminar un registro
print("\n5. Eliminando alumno:3")
valor_eliminado = baseDatosRedis.get("alumno:3")
baseDatosRedis.delete("alumno:3")
print("Eliminado:", valor_eliminado)

# 6. Mostrar todas las claves
print("\n6. Claves actuales:", baseDatosRedis.keys("alumno:*"))

# 7. Mostrar todos los valores guardados
print("\n7. Valores guardados:")
for k in baseDatosRedis.keys("alumno:*"):
    print(baseDatosRedis.get(k))

# 8. Mostrar varios registros con una clave que cumpla un patrón
print("\n8. Buscar con * (alumno:1*)")
print(baseDatosRedis.keys("alumno:1*"))

# 9. Buscar con [] (ejemplo)
print("\n9. Buscar con [] (alumno:[12]) -> busca alumno:1 o alumno:2")
print(baseDatosRedis.keys("alumno:[1245]"))

# 10. Buscar con ?
print("\n10. Buscar con ? (alumno:?2) -> por ejemplo alumno:12 o alumno:22")
print(baseDatosRedis.keys("alumno:?2"))

# 11. Filtrar alumnos
print("\n11. Filtrar alumnos con 3 o más faltas (riesgo de absentismo)")
for k in baseDatosRedis.keys("alumno:*"):
    alumno = json.loads(baseDatosRedis.get(k))
    if alumno["faltas"] >= 3:
        print(k, alumno)

# 12. Actualizar varios registros
print("\n12. Aumentar faltas +1 a alumnos del curso 6B")
for k in baseDatosRedis.keys("alumno:*"):
    alumno = json.loads(baseDatosRedis.get(k))
    if alumno["curso"] == "6B":
        alumno["faltas"] += 1
        baseDatosRedis.set(k, json.dumps(alumno))
        print(k, alumno)


# 13. Eliminar varios registros según filtros
print("\n13. Eliminar alumnos sin faltas")
for k in baseDatosRedis.keys("alumno:*"):
    alumno = json.loads(baseDatosRedis.get(k))
    if alumno["faltas"] == 0:
        baseDatosRedis.delete(k)
        print("Eliminado:", k)


# 14. Crear una estructura JSON en forma de array
print("\n14. Crear array JSON de alumnos")
lista_alumnos = []
for k in baseDatosRedis.keys("alumno:*"):
    lista_alumnos.append(json.loads(baseDatosRedis.get(k)))

baseDatosRedis.set("alumnos_array", json.dumps(lista_alumnos))
print("Array guardado en Redis")


# 15. Filtrar por cada atributo del JSON
print("\n15. Filtrar alumnos por edad = 11")
alumnos = json.loads(baseDatosRedis.get("alumnos_array"))
for a in alumnos:
    if a["edad"] == 11:
        print(a)


# 16. Crear una lista en REDIS
print("\n16. Crear lista Redis de alumnos en riesgo")
baseDatosRedis.delete("lista_riesgo")

for k in baseDatosRedis.keys("alumno:*"):
    alumno = json.loads(baseDatosRedis.get(k))
    if alumno["faltas"] >= 3:
        baseDatosRedis.rpush("lista_riesgo", alumno["nombre"])

print("Lista creada:", baseDatosRedis.lrange("lista_riesgo", 0, -1))


# 17. Obtener elementos de una lista con filtro
print("\n17. Filtrar lista por nombre que contenga '5'")
for nombre in baseDatosRedis.lrange("lista_riesgo", 0, -1):
    if "5" in nombre:
        print(nombre)


# 18. Crear datos con índices
print("\n18. Crear alumnos con índices (hash)")
baseDatosRedis.hset("alumno_indexado:1", mapping={
    "nombre": "AlumnoIndex1",
    "curso": "5A",
    "faltas": 4
})

baseDatosRedis.hset("alumno_indexado:2", mapping={
    "nombre": "AlumnoIndex2",
    "curso": "6B",
    "faltas": 2
})


# 19. Búsqueda usando índices
print("\n19. Buscar alumnos indexados del curso 5A")
for key in baseDatosRedis.keys("alumno_indexado:*"):
    if baseDatosRedis.hget(key, "curso") == "5A":
        print(key, baseDatosRedis.hgetall(key))


# 20. Group By usando índices
print("\n20. Group By curso")
group = {}

for key in baseDatosRedis.keys("alumno_indexado:*"):
    curso = baseDatosRedis.hget(key, "curso")
    group.setdefault(curso, []).append(baseDatosRedis.hget(key, "nombre"))

for curso, alumnos in group.items():
    print(curso, "->", alumnos)
