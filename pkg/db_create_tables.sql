-- public.alk_registros_totales definition
DROP TABLE IF EXISTS public.alk_registros_totales;

CREATE TABLE public.alk_registros_totales (
	categoria text,
	provincia text,
	fuente text,
	cnt int8,
	dt_loaded timestamp
);


-- public.alk_registros_unificados definition
DROP TABLE IF EXISTS public.alk_registros_unificados;

CREATE TABLE public.alk_registros_unificados (
	cod_loc int8,
	id_provincia int8,
	id_departamento int8,
	categoria text,
	provincia text,
	localidad text,
	nombre text,
	domicilio text,
	cp text,
	telefono text,
	mail text,
	web text,
	dt_loaded timestamp
);

-- public.alk_totales_cine definition
DROP TABLE IF EXISTS public.alk_totales_cine;

CREATE TABLE public.alk_totales_cine (
	cod_loc int8,
	id_provincia int8,
	id_departamento int8,
	observaciones float8,
	categoria text,
	provincia text,
	departamento text,
	localidad text,
	nombre text,
	domicilio text,
	piso text,
	cp int8,
	cod_area text,
	telefono text,
	mail text,
	web text,
	info_adicional float8,
	latitud float8,
	longitud float8,
	tipo_latitud_longitud text,
	fuente text,
	tipo_gestion text,
	pantallas int8,
	butacas int8,
	espacio_incaa text,
	ano_actualizacion int8,
	dt_loaded timestamp
);