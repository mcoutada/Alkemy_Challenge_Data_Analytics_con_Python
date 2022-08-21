import datetime as dt
import re

import pandas as pd
import unidecode as un


def transform(csvs_dic):
    """Main function to transform data

    Args:
        csvs_dic (dict): Dictionary with all csv files to be transformed (key: category, value: csv file path)

    Returns:
        dict: Dictionary with all csv files to be transformed (key: category, value: DataFrames to be upladed to the DB)
    """

    dfs_dic = {}
    for category, csv_file in csvs_dic.items():
        df = pd.read_csv(csv_file)
        df = df.rename(columns=lambda x: standarize_header(x))
        dfs_dic[category] = df

    dfs_dic = standarize_data(dfs_dic)
    dfs_dic["registros_unificados"] = set_t1_registros_unificados(
        list(dfs_dic.values())
    )
    dfs_dic["registros_totales"] = set_t2_registros_totales(
        list(dfs_dic.values()))
    dfs_dic["totales_cine"] = set_t3_totales_cine(dfs_dic["cine"])

    now = dt.datetime.now()

    for cat in dfs_dic.keys():
        dfs_dic[cat]["dt_loaded"] = now

    return dfs_dic


def set_t1_registros_unificados(dfs_lst):
    """
    Normalizar toda la información de Museos, Salas de Cine y Bibliotecas
    Populares, para crear una única tabla que contenga:

    Pedido por enunciado     Normalizado
    cod_localidad        --> cod_loc
    id_provincia         --> id_provincia
    id_departamento      --> id_departamento
    categoría            --> categoria
    provincia            --> provincia
    localidad            --> localidad
    nombre               --> nombre
    domicilio            --> domicilio
    código postal        --> cp
    número de teléfono   --> telefono
    mail                 --> mail
    web                  --> web

    It takes a list of dataframes, drops all columns that are not in the list `wk_cols`, and then
    concatenates the dataframes into one

    :param dfs_lst: a list of dataframes
    :return: A dataframe with the columns specified in the wk_cols list.
    """

    wk_cols = [
        "cod_loc",
        "id_provincia",
        "id_departamento",
        "categoria",
        "provincia",
        "localidad",
        "nombre",
        "domicilio",
        "cp",
        "telefono",
        "mail",
        "web",
    ]

    # Drop non-relevant columns
    for idx, df in enumerate(dfs_lst):
        dfs_lst[idx] = df.drop(
            columns=[col for col in df.columns if col not in wk_cols]
        )

    return pd.concat(dfs_lst)


def set_t2_registros_totales(dfs_lst):
    """
    ● Procesar los datos conjuntos para poder generar una tabla con la siguiente
    información:
    o Cantidad de registros totales por categoría
    o Cantidad de registros totales por fuente
    o Cantidad de registros por provincia y categoría

    Pedido por enunciado     Normalizado
    categoría            --> categoria
    provincia            --> provincia
    fuente               --> fuente

    It takes a list of dataframes, drops all columns except the ones you want to group by, concatenates
    the dataframes, adds a column with a constant value, groups by the columns you want to group by,
    adds a column with the count of rows, concatenates the dataframes with the grouped data, and
    reorders the columns

    :param dfs_lst: a list of dataframes to be processed
    :return: A dataframe with the following columns:
    """

    wk_cols = ["categoria", "provincia", "fuente"]

    # Drop non-relevant columns
    for idx, df in enumerate(dfs_lst):
        dfs_lst[idx] = df.drop(
            columns=[col for col in df.columns if col not in wk_cols]
        )

    big_df = pd.concat(dfs_lst)

    # Add auxiliary not null column to count rows
    big_df["aux"] = 1

    groupby_lst = [["categoria"], ["fuente"], ["provincia", "categoria"]]
    grouped_dfs_lst = [None] * len(groupby_lst)

    # Group records and add aggregated column
    for idx, cat in enumerate(groupby_lst):
        # as_index=False means you indicate to groupby() that you don't want to
        # set the aggregated column as the index. It's equivalent to add at the
        # end .reset_index()
        grouped_dfs_lst[idx] = big_df.groupby(by=cat, as_index=False).agg(
            totals_cnt=("aux", "count")
        )

    # Concat dataframes and reorder columns
    out_df = pd.concat(grouped_dfs_lst).reindex(
        columns=wk_cols + ["totals_cnt"])

    return out_df


def set_t3_totales_cine(df_cine):
    """

    Procesar la información de cines para poder crear una tabla que contenga:
    Pedido por enunciado             Normalizado
    o Provincia                  --> provincia
    o Cantidad de pantallas      --> pantallas
    o Cantidad de butacas        --> butacas
    o Cantidad de espacios INCAA --> espacio_incaa

    It takes a dataframe, drops all columns that are not in the list wk_cols, groups by provincia, and
    then aggregates the sum of pantallas, sum of butacas, and count of espacio_incaa.

    :param df_cine: the dataframe that contains the information about the cinemas
    :return: A dataframe with the following columns:
        provincia
        sum_pantallas
        sum_butacas
        cnt_espacio_incaa
    """

    wk_cols = ["provincia", "pantallas", "butacas", "espacio_incaa"]

    # Drop non-relevant columns
    df_cine.drop(
        columns=[
            col for col in df_cine.columns if col not in wk_cols])

    df_cine = df_cine.groupby("provincia", as_index=False).agg(
        sum_pantallas=("pantallas", "sum"),
        sum_butacas=("butacas", "sum"),
        cnt_espacio_incaa=("espacio_incaa", "count"),
    )
    return df_cine


def standarize_data(dfs_dic):
    """
    Perform some data cleanup and standarization

    Args:
        dfs_dic (dict): Dictionary of all dataframes to be transformed (key: category, value: category dataframes)

    Returns:
        dict: Dictionary of transformed dataframes (key: category, value: category dataframes)
    """

    def clean_up(x): return un.unidecode(str(x).upper().strip())

    for wk_cat, wk_df in dfs_dic.items():
        # Fix data inconsistencies
        # "Neuquén " --> "NEUQUEN"
        # "Santa Fé" --> "SANTA FE"
        # "Tierra del Fuego, Antártida e Islas del Atlántico Sur" --> "TIERRA DEL FUEGO"

        # Apply clean_up to all cells in the column list
        wk_df[["provincia", "fuente"]] = wk_df[[
            "provincia", "fuente"]].applymap(clean_up)

        if wk_cat == "cine":
            wk_df["espacio_incaa"] = wk_df["espacio_incaa"].apply(
                lambda x: "SI" if clean_up(str(x)) == "SI" else None
            )

        # Manual adjustments
        wk_df["provincia"] = wk_df["provincia"].replace(
            "TIERRA DEL FUEGO, ANTARTIDA E ISLAS DEL ATLANTICO SUR", "TIERRA DEL FUEGO")
        wk_df["fuente"] = wk_df["fuente"].replace(
            "GOB. PCIA.", "GOBIERNO DE LA PROVINCIA"
        )

    return dfs_dic


def standarize_header(col_name):
    """Sets a standarized column name

    Args:
        col_name (str): Colun name

    Returns:
        str: Standarized column name (ASCII characters + snake case)


    biblioteca_popular:
    original:     Cod_Loc,IdProvincia ,IdDepartamento ,Observacion,Categoría,Subcategoria,Provincia,Departamento,Localidad,Nombre,Domicilio,Piso,CP,Cod_tel,Teléfono,Mail,Web,Información adicional,Latitud,Longitud,TipoLatitudLongitud  ,Fuente,Tipo_gestion,año_inicio,Año_actualizacion
    standarized:  cod_loc,id_provincia,id_departamento,observacion,categoria,subcategoria,provincia,departamento,localidad,nombre,domicilio,piso,cp,cod_tel,telefono,mail,web,informacion_adicional,latitud,longitud,tipo_latitud_longitud,fuente,tipo_gestion,ano_inicio,ano_actualizacion

    cine:
    original:     Cod_Loc,IdProvincia ,IdDepartamento ,Observaciones,Categoría,Provincia,Departamento,Localidad,Nombre,Dirección,Piso,CP,cod_area,Teléfono,Mail,Web,Información adicional,Latitud,Longitud,TipoLatitudLongitud  ,Fuente,tipo_gestion,Pantallas,Butacas,espacio_INCAA,año_actualizacion
    standarized:  cod_loc,id_provincia,id_departamento,observaciones,categoria,provincia,departamento,localidad,nombre,domicilio,piso,cp,cod_area,telefono,mail,web,info_adicional,latitud,longitud,tipo_latitud_longitud,fuente,tipo_gestion,pantallas,butacas,espacio_incaa,ano_actualizacion

    museos_datosabiertos:
    original:     Cod_Loc,IdProvincia ,IdDepartamento ,Observaciones,categoria,subcategoria,provincia,localidad,nombre,direccion,piso,CP,cod_area,telefono,Mail,Web,Latitud,Longitud,TipoLatitudLongitud  ,Info_adicional,fuente,jurisdiccion,año_inauguracion,actualizacion
    standarized:  cod_loc,id_provincia,id_departamento,observaciones,categoria,subcategoria,provincia,localidad,nombre,domicilio,piso,cp,cod_area,telefono,mail,web,latitud,longitud,tipo_latitud_longitud,info_adicional,fuente,jurisdiccion,ano_inauguracion,actualizacion

    All standarized:
    biblioteca_popular:   cod_loc,id_provincia,id_departamento,observaciones,categoria,subcategoria,provincia             ,localidad,nombre,domicilio,piso,cp,cod_area,telefono,mail,web,info_adicional,latitud,longitud,tipo_latitud_longitud,fuente,jurisdiccion,ano_inauguracion,actualizacion
    cine:                 cod_loc,id_provincia,id_departamento,observaciones,categoria             ,provincia,departamento,localidad,nombre,domicilio,piso,cp,cod_area,telefono,mail,web,info_adicional,latitud,longitud,tipo_latitud_longitud,fuente                              ,pantallas,butacas,espacio_incaa,ano_actualizacion
    museos_datosabiertos: cod_loc,id_provincia,id_departamento,observaciones,categoria,subcategoria,provincia             ,localidad,nombre,domicilio,piso,cp,cod_area,telefono,mail,web,info_adicional,latitud,longitud,tipo_latitud_longitud,fuente,jurisdiccion,ano_inauguracion,actualizacion
    """

    # Remove spaces and replace accented or special characters with their
    # ASCII equivalent
    col_name = un.unidecode(col_name.strip().replace(" ", "_"))

    # Convert to Snake Case
    re_compiled = re.compile("((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))")
    col_name = re_compiled.sub(r"_\1", col_name).lower().replace("__", "_")

    # Manual adjustments:

    manual_adjustments = {
        "direccion": "domicilio",
        "informacion_adicional": "info_adicional",
        "cod_tel": "cod_area",
    }

    if col_name in manual_adjustments.keys():
        col_name = manual_adjustments[col_name]

    return col_name


if __name__ == "__main__":

    pass

    ################# Test transform() #################

    # prj =r"c:\Users\asd\Desktop\alkemy\Alkemy_Challenge_Data_Analytics_con_Python"
    # prj = prj + r"\data"
    # yyyy_mon = "2022-agosto"
    # dd_mm_yyyy = "18-08-2022"
    # cats = ['museos_datosabiertos', 'cine', 'biblioteca_popular']
    # csvs_dic = {cat: f'{prj}\\{cat}\\{yyyy_mon}\\{cat}-{dd_mm_yyyy}.csv' for cat in cats}
    # dfs_dic = transform(csvs_dic)

    # import load as l
    # l.load(dfs_dic)

    ################# Test standarize_header() #################
    # in_headers = {
    #     "biblioteca_popular": "Cod_Loc,IdProvincia,IdDepartamento,Observacion,Categoría,Subcategoria,Provincia,Departamento,Localidad,Nombre,Domicilio,Piso,CP,Cod_tel,Teléfono,Mail,Web,Información adicional,Latitud,Longitud,TipoLatitudLongitud,Fuente,Tipo_gestion,año_inicio,Año_actualizacion",
    #     "cine": "Cod_Loc,IdProvincia,IdDepartamento,Observaciones,Categoría,Provincia,Departamento,Localidad,Nombre,Dirección,Piso,CP,cod_area,Teléfono,Mail,Web,Información adicional,Latitud,Longitud,TipoLatitudLongitud,Fuente,tipo_gestion,Pantallas,Butacas,espacio_INCAA,año_actualizacion",
    #     "museos_datosabiertos": "Cod_Loc,IdProvincia,IdDepartamento,Observaciones,categoria,subcategoria,provincia,localidad,nombre,direccion,piso,CP,cod_area,telefono,Mail,Web,Latitud,Longitud,TipoLatitudLongitud,Info_adicional,fuente,jurisdiccion,año_inauguracion,actualizacion"
    # }

    # out_headers = set()

    # for hdr in in_headers.values():
    #     out_str=[]
    #     for col_name in hdr.split(","):
    #         new_col_name = standarize_header(col_name)
    #         out_headers.add(col_name+":"+ new_col_name)
    #         out_str.append(new_col_name)

    #     print(",".join(out_str),'\n')

    # for val in sorted(out_headers, key=str.lower):
    #     print(val)
