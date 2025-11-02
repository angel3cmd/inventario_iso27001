import sqlite3

conn = sqlite3.connect("data/inventario.db")
cursor = conn.cursor()

print("🔗 Relaciones entre elementos de configuración (CIs):\n")

cursor.execute("""
    SELECT r.id, r.origen_tipo, r.origen_id, r.destino_tipo, r.destino_id, r.tipo_relacion, r.descripcion,
           ao.nombre AS origen_nombre, ad.nombre AS destino_nombre
    FROM relaciones_ci r
    LEFT JOIN activos ao ON r.origen_tipo = 'activo' AND r.origen_id = ao.id
    LEFT JOIN activos ad ON r.destino_tipo = 'activo' AND r.destino_id = ad.id
    ORDER BY r.id
""")

relaciones = cursor.fetchall()

for rel in relaciones:
    rel_id, origen_tipo, origen_id, destino_tipo, destino_id, tipo_relacion, descripcion, origen_nombre, destino_nombre = rel
    print(f"[{rel_id}] {origen_tipo}({origen_id}) ➜ {tipo_relacion} ➜ {destino_tipo}({destino_id})")
    print(f"     ↳ {descripcion}")
    if origen_nombre:
        print(f"     ↳ Origen: {origen_nombre}")
    if destino_nombre:
        print(f"     ↳ Destino: {destino_nombre}")
    print()

conn.close()
