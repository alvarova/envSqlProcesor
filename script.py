import os
from dotenv import load_dotenv
import pymysql
import pymysql.constants.CLIENT as CLIENT
from datetime import datetime
import glob
import argparse
import sys

def main(env):
    # Cargar variables de entorno según el ambiente especificado
    env_file = f".env.{env}" if env else ".env"
    if not os.path.exists(env_file):
        raise FileNotFoundError(f"No se encontró el archivo de configuración: {env_file}")
    
    load_dotenv(env_file)
    
    # Configuración de la base de datos (igual que antes)
    required_vars = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']
    config = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME'),
        'port': int(os.getenv('DB_PORT', '3306')),
        'client_flag': CLIENT.MULTI_STATEMENTS
    }
    
    # Validar variables requeridas
    for var in required_vars:
        if not config.get(var.lower()):
            raise ValueError(f"Variable faltante en {env_file}: {var}")

    # Resto del código de conexión y ejecución igual que antes...
    # (Mantener todo el código de procesamiento SQL y logging)

if __name__ == '__main__':
    # Configurar el sistema de argumentos
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-e', '--env', help='Especifica el entorno a utilizar')
    
    # Mostrar ayuda si no se especifican argumentos
    if not len(sys.argv) > 1:
        print("Script para ejecutar tareas SQL en diferentes entornos\n")
        print("Uso: python script.py --env [nombre_entorno]")
        print("\nEntornos disponibles:")
        print(" - local (usa .env.local)")
        print(" - produccion (usa .env.produccion)")
        print(" - test (usa .env.test)")
        print("\nEjemplos:")
        print("  python script.py --env local")
        print("  python script.py --env produccion")
        sys.exit(0)
    
    args = parser.parse_args()
    
    try:
        main(args.env)
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        sys.exit(1)