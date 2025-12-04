import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def crear_base_datos():
    try:
        # Nos conectamos a la base de datos por defecto 'postgres'
        # Usamos tu contraseña proporcionada
        conn = psycopg2.connect(
            user="postgres", 
            password="Cuaderno15", 
            host="localhost", 
            port="5432"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Comando SQL para crear la base de datos
        db_name = "portal_academico"
        cursor.execute(f"CREATE DATABASE {db_name};")
        print(f"✅ ÉXITO: Base de datos '{db_name}' creada correctamente en PostgreSQL.")

    except psycopg2.errors.DuplicateDatabase:
        print(f"⚠️ AVISO: La base de datos '{db_name}' ya existe. Puedes continuar.")
    except Exception as e:
        print(f"❌ ERROR: No se pudo conectar a PostgreSQL. Verifica que esté corriendo.\nDetalle: {e}")
    finally:
        if 'conn' in locals() and conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    crear_base_datos()