# Alkemy - Challenge Data Analytics con Python

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
:: Para desactivarlo, escribir:
deactivate
:: o correr:
.\alkemy_mcoutada_venv\Scripts\deactivate.bat
```
Instalar las dependencias:
```bat
pip install -r requirements.txt
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

# Otros comandos útiles:
Armar requirements.txt:
```bat
pip freeze >> requirements.txt
```

