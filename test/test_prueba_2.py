import sqlite3
import pytest



def alta_registro(material, descripcion, precio_venta, precio_costo, stock, proveedor, nombre_bd='../basededatos.db'):
    """
    Inserta un nuevo registro en la base de datos.
    """
    try:
        conexion = sqlite3.connect('../basededatos.db')
        cursor = conexion.cursor()

        cursor.execute("INSERT INTO materiales (material, descripcion, precio_venta, precio_costo, stock, proveedor) VALUES (?, ?, ?, ?, ?, ?)",
                    (material, descripcion, precio_venta, precio_costo, stock, proveedor))

        conexion.commit()
        conexion.close()
        return "Registro agregado correctamente"
    except Exception as e:
        return f"No se pudo agregar el registro: {e}"


# Prueba unitaria para la función alta_registro()
def test_alta_registro():
    # Datos de prueba
    material = 1
    descripcion = "Producto de prueba"
    precio_venta = 10.0
    precio_costo = 5.0
    stock = 100
    proveedor = "Proveedor de prueba"

    # Agregar el registro
    assert alta_registro(material, descripcion, precio_venta, precio_costo, stock, proveedor) == "Registro agregado correctamente"

    # Verificar si el registro se agregó correctamente consultando la base de datos
    conexion = sqlite3.connect('test.db')  # Conectar a la base de datos de prueba
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM materiales WHERE material = ?", (material,))
    registro = cursor.fetchone()
    conexion.close()

    # Verificar si se encontró el registro en la base de datos
    assert registro is not None
    assert registro[1] == material
    assert registro[2] == descripcion
    assert registro[3] == precio_venta
    assert registro[4] == precio_costo
    assert registro[5] == stock
    assert registro[6] == proveedor

# Ejecutar las pruebas con pytest
if __name__ == "__main__":
    import pytest
    pytest.main([__file__, '-vv'])
