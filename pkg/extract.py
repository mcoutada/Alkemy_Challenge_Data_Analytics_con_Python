import datetime
import locale
import os

import requests

import logger

# Set the logger for this file
log = logger.set_logger(logger_name=logger.get_rel_path(__file__))



def get_abspath(fname):
    r"""Returns the absolute path of the file

    Args:
        fname (str): file name without extension. Example: museos

    Returns:
        tuple of strings: returns the absolute path of the file and the filename
        Example: ("/home/basedir/categoría/año-mes", "/home/basedir/categoría/año-mes/categoria-dia-mes-año.csv")
        Example: ("c:\Users\user1\Alkemy_Challenge_Data_Analytics_con_Python\data\museos\2021-noviembre",
                  "c:\Users\user1\Alkemy_Challenge_Data_Analytics_con_Python\data\museos\2021-noviembre\museos-03-11-2021.csv")
    """

    # Set locale to Spanish Argentina to get the month name in spanish
    # See list https://saimana.com/list-of-country-locale-code/
    locale.setlocale(locale.LC_TIME, "es_AR.UTF-8")

    # Get the current date and format it properly
    # %Y	Full year with century	2021,2022
    # %B	Full month name	January, February,…, December
    # %d	Days with zero padded value	01-31
    # %m	Month with zero padded value	01-12
    # %y	Year without century with zero padded value	00,01,….21,22…,99

    now = datetime.datetime.now()
    yyyy_mon = now.strftime("%Y-%B")
    dd_mm_yyyy = now.strftime("%d-%m-%y")
    
    full_path = os.path.join(os.getcwd(), 'data', fname, yyyy_mon)
    full_fname = os.path.join(full_path, fname + "-" + dd_mm_yyyy + ".csv")

    return full_path, full_fname


def download():

    data = {
        "museos_datosabiertos": "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/4207def0-2ff7-41d5-9095-d42ae8207a5d/download/museos_datosabiertos.csv",
        "cine": "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/392ce1a8-ef11-4776-b280-6f1c7fae16ae/download/cine.csv",
        "biblioteca_popular": "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/01c6c048-dbeb-44e0-8efa-6944f73715d7/download/biblioteca_popular.csv",
    }

    for src_file, url in data.items():
        log.info("Downloading {}".format(src_file))
        
        full_path, full_fname = get_abspath(src_file)

        # Create the directory if it doesn't exist
        # exist_ok = OSError (directory exists) will be ignored and the directory will not be created
        os.makedirs(full_path, exist_ok=True)

        # Downloading the file from the URL. If the response takes more than 5
        # seconds, it will raise a TimeoutError exception.
        r = requests.get(url, timeout=5)

        # Writing the content of the response to a file.
        # "wb" indicates that the file is opened for writing in binary mode
        # r.content is the content of the response content in bytes
        # Therefore, r.content goes along with open(full_fname, "wb")
        # Alternatively, you can use:
        # r.text along with open(full_fname, "wt", encoding=r.encoding)
        # If we use text, we need to enforce to write the file in the same encoding of the request, which is iso-8859-1
        
        with open(full_fname, "wb") as f: 
            f.write(r.content)


if __name__ == "__main__":
    download()
