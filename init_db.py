import sqlite3

def crear_base_de_datos():
    conn = sqlite3.connect('usuarios_biometria.db')
    cursor = conn.cursor()

    print("Sincronizando tablas para GPU...")

    # 1. Tabla de Rostros (PyTorch usa BLOB para tensores)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rostros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            encoding BLOB NOT NULL
        )
    ''')

    # 2. Tabla de Historial (Sincronizada con main_access_gpu.py)
    # Cambiamos 'fecha_hora' por 'fecha' para que coincida
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historial_accesos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            fecha TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("¡Base de datos lista para la RTX 3050!")

if __name__ == "__main__":
    crear_base_de_datos()