# SQL Environment Processor

Script para ejecutar archivos SQL en diferentes entornos

## Instalación

```bash
git clone https://github.com/alvarova/envSqlProcesor.git
cd envSqlProcesor
pip install -r requirements.txt

##Crea archivos de entorno:

cp .env.example .env.desarrollo
cp .env.example .env.produccion
cp .env.example .env.local


# Mostrar ayuda
python run_sql.py

# Ejecutar en entorno local
python run_sql.py --env local

# Ejecutar en producción
python run_sql.py --env produccion



## Estructura de archivos
tareasSql/: Directorio con scripts SQL a ejecutar

.env.[ambiente]: Configuración por entorno

registro.log: Log de ejecuciones (se crea automáticamente)