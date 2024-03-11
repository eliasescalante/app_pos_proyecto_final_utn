import os
import sqlite3

#modifique la funcion para que pueda funcionar sin los get()
#de esta forma pude testear esta funcion
def crear_base_datos(nombre_bd):
    """
    Crea la base de datos si no existe.
    Devuelve un mensaje indicando si la base de datos se creó correctamente o si ya existe.
    """
    if os.path.exists(nombre_bd):
        return "La base de datos ya existe"
    else:
        try:
            conexion = sqlite3.connect(nombre_bd)
            cursor = conexion.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS materiales (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                material INTEGER NOT NULL,
                                descripcion TEXT NOT NULL,
                                precio_venta REAL NOT NULL,
                                precio_costo REAL NOT NULL,
                                stock INTEGER NOT NULL,
                                proveedor TEXT NOT NULL)''')

            conexion.commit()
            conexion.close()
            return "Base de datos creada correctamente"
        except Exception as e:
            return f"No se pudo crear la base de datos: {e}"

# Prueba unitaria para la función crear_base_datos()
def test_crear_base_datos():
    nombre_bd = 'test.db'
    assert crear_base_datos(nombre_bd) == "Base de datos creada correctamente"
    assert crear_base_datos(nombre_bd) == "La base de datos ya existe"

    # Limpieza después de la prueba
    os.remove(nombre_bd)

# Ejecutar las pruebas con pytest
if __name__ == "__main__":
    import pytest
    pytest.main([__file__, '-vv'])
