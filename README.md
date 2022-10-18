# Alkemy - Challenge Data Analytics con Python

## English description:
# Admission challenge ad Alkemy.org for Python + Data Analytics:
Extract CSV files from different sources using Python's Requests library.<br>
Transform the data using Python's Pandas library.<br>
Load the data frames to a PostgreSQL database using SQLAlchemy.<br>
Set the project into a Virtual Environment (venv) and generate a proper requirements.txt.<br>
Generate a log of the process using Python's logging library.<br>
The DB config is taken from a .env file using Python's decouple library.<br>

## Pasos a seguir: 
Abrir una ventana de CMD en una carpeta de trabajo a eleccion y correr:

Clonar el repositorio:
```bat
git clone https://github.com/mcoutada/Alkemy_Challenge_Data_Analytics_con_Python.git
```
Generar un entorno virtual:
```bat
cd Alkemy_Challenge_Data_Analytics_con_Python
python -m venv alkemy_mcoutada_venv
:: Activar el entorno (el comando de abajo cambia si no es Windows)
.\alkemy_mcoutada_venv\Scripts\activate.bat
```
Instalar las dependencias:
```bat
pip install -r requirements.txt
```
Setear la conexion a la DB en el archivo `.env`

Correr el proyecto:
```bat
python app.py
```

## Logs:
Se generan en la carpeta /logs del proyecto

## Modo DEBUG:
```bat
python app.py DEBUG
```
Permite que, para todas las funciones, se generen mensajes de log de:
* Llamada y parámetros de entrada
* Finalización, valor de retorno y tiempo transcurrido

Un fallo inesperado será logueado automáticamente.

## Otros comandos útiles:
Armar requirements.txt:
```bat
pip freeze > requirements.txt
```
Que se ha generado al instalar los siguientes paquetes:
```bat
pip install requests
pip install pandas
pip install unidecode
pip install sqlalchemy
pip install python-decouple
pip install psycopg2-binary
```
python-decouple fue necesario instalarlo tambien fuera del virtual env para hacerlo andar

Desactivar el entorno virtual:
```bat
:: Para desactivarlo, escribir:
deactivate
:: o correr:
.\alkemy_mcoutada_venv\Scripts\deactivate.bat
```
