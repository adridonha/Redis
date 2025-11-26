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

# 11. Filtrar por un valor
print("\n11. Filtrar alumnos del curso 5A")
for k in r.keys("alumno:*"):
    obj = json.loads(r.get(k))
    if obj["curso"] == "5A":
        print(k, obj)