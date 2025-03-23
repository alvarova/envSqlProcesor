import os
import sys
import glob
import argparse
from datetime import datetime
from dotenv import load_dotenv
import pymysql
import pymysql.constants.CLIENT as CLIENT

def ejecutar_archivos_sql(connection, sql_dir):
    archivos_sql = glob.glob(os.path.join(sql_dir, '*.sql'))
    archivos_sql.sort()
    
    for file_path in archivos_sql:
        nombre_archivo = os.path.basename(file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                sql = f.read()
        except Exception as e:
            mensaje_error = f"[{datetime.now()}] {nombre_archivo} - ERROR LECTURA: {str(e)}\n"
            with open('registro.log', 'a') as log_file:
                log_file.write(mensaje_error)
            continue

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                while cursor.nextset():
                    pass
            connection.commit()
            mensaje_log = f"[{datetime.now()}] {nombre_archivo} - EJECUTADO CORRECTAMENTE\n"
        except Exception as e:
            connection.rollback()
            mensaje_log = f"[{datetime.now()}] {nombre_archivo} - ERROR EJECUCIÓN: {str(e)}\n"
        
        with open('registro.log', 'a') as log_file:
            log_file.write(mensaje_log)

def main(ambiente):
    # Configurar archivo .env
    env_file = f".env.{ambiente}" if ambiente else ".env"
    
    if not os.path.exists(env_file):
        raise FileNotFoundError(f"Archivo de configuración no encontrado: {env_file}")
    
    load_dotenv(env_file)
    
    # Validar variables de entorno
    config = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME'),
        'port': int(os.getenv('DB_PORT', '3306')),
        'client_flag': CLIENT.MULTI_STATEMENTS
    }
    
    for var in ['host', 'user', 'password', 'database']:
        if not config[var]:
            raise ValueError(f"Variable faltante en {env_file}: DB_{var.upper()}")

    # Conectar a la base de datos
    try:
        conexion = pymysql.connect(**config)
    except Exception as e:
        with open('registro.log', 'a') as log_file:
            log_file.write(f"[{datetime.now()}] ERROR CONEXIÓN: {str(e)}\n")
        raise

    # Ejecutar scripts SQL
    try:
        ejecutar_archivos_sql(conexion, 'tareasSql')
    finally:
        conexion.close()

if __name__ == '__main__':
    # Configurar argumentos de línea de comandos
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-e', '--env', help='Especificar ambiente (ej: produccion, desarrollo)')

    # Mostrar ayuda si no hay argumentos
    if len(sys.argv) == 1:
        print("\nSQL Processor - Ejecutor de scripts SQL para diferentes ambientes\n")
        print("Uso:")
        print("  python run_sql.py --env [nombre_ambiente]")
        print("\nAmbientes disponibles:")
        print("  - desarrollo (.env.desarrollo)")
        print("  - produccion (.env.produccion)")
        print("  - testing (.env.testing)")
        print("\nEjemplos:")
        print("  python run_sql.py --env desarrollo")
        print("  python run_sql.py --env produccion\n")
        sys.exit(0)

    args = parser.parse_args()

    try:
        main(args.env)
        print("\nProceso completado. Revisar registro.log para detalles.\n")
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        sys.exit(1)