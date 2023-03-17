



--1. Sedes: 
select * from  tickets_sedes;;
create extension dblink;
 
SELECT dblink_connect ('mycon1','host=192.168.0.237 user=postgres password=BD_m3d1c4l dbname=bd_imhotep') ;

insert into tickets_sedes (codreg_sede, nom_sede, codreg_ips,direccion,telefono,departamento, municipio, zona , sede, "estadoReg")
SELECT codreg_sede, translate(btrim(nom_sede::text),'óÓáÁéÉíÍúÚñÑ'::text,'oOaAeEiIuUnN'::text), codreg_ips,translate(btrim(direccion::text),'óÓáÁéÉíÍúÚñÑ'::text,'oOaAeEiIuUnN'::text),translate(btrim(telefono::text),'óÓáÁéÉíÍúÚñÑ'::text,'oOaAeEiIuUnN'::text),translate(btrim(departamento::text),'óÓáÁéÉíÍúÚñÑ'::text,'oOaAeEiIuUnN'::text), translate(btrim(municipio::text),'óÓáÁéÉíÍúÚñÑ'::text,'oOaAeEiIuUnN'::text), translate(btrim(zona::text),'óÓáÁéÉíÍúÚñÑ'::text,'oOaAeEiIuUnN'::text) , sede, 'A'
FROM dblink('mycon1', 'SELECT codreg_sede, nom_sede, codreg_ips,direccion,telefono,departamento, municipio, zona , sede   FROM imhotep_sedes'::text)
 c(codreg_sede character  (10), nom_sede character (30), codreg_ips character (15), direccion character (200),   telefono character (120), departamento character varying (120), municipio character varying (120),zona character varying (120),sede character varying (120) );


update tickets_sedes set direccion = 'Calle 36 Sur No. 77-33 Barrio Kennedy'  where codreg_sede = 'MK' ;
update tickets_sedes set direccion = 'Avenida Carrera 45 # 94 - 31/39 (Autopista Norte)' where codreg_sede = 'MN' ;
update tickets_sedes set direccion = 'Cra 66A #4G-86' where codreg_sede = 'AM' ;
update tickets_sedes set direccion = 'Cl. 1d # 17A - 35' where codreg_sede = 'SJ' ;
update tickets_sedes set direccion = 'Cra 102 # 17-49/57' where codreg_sede = 'SF' ;
update tickets_sedes set direccion = 'Cr 21 No 169 15/25 Bodega 2' where codreg_sede = 'MT' ;

 

-- 2. Areas
-- Otra voz

-- Se crea la nueva tabla de acuerdo a las columnas que se necesiten ...
select  * from tickets_areas;

CREATE TABLE areas_2023 (nombre  character varying(80));

-- Para copiar los datos desde Excel a la Tavbla


COPY areas_2023  FROM '/mnt/sda3/PostgreSQL/9.4/thtickets/AreasSubir.csv' HEADER CSV DELIMITER ';';

select * from areas_2023;


select * from mae_articulos_maestro_2023;  -- 159 reg

-- Se valida

insert into tickets_areas (nombre,"estadoReg") select nombre, 'A' from areas_2023;

--3 UBICACIONES


select  * from tickets_ubicaciones;

CREATE TABLE ubicaciones_2023 (nombre  character varying(80));

-- Para copiar los datos desde Excel a la Tavbla


COPY ubicaciones_2023  FROM '/mnt/sda3/PostgreSQL/9.4/thtickets/UbicacionesSubir.csv' HEADER CSV DELIMITER ';';

select * from ubicaciones_2023;


select * from ubicaciones_2023;  -- 159 reg

-- Se valida

insert into tickets_ubicaciones (nombre,"estadoReg") select nombre, 'A' from ubicaciones_2023;


--4 CARGOS


select  * from tickets_cargos;
delete from tickets_cargos;

CREATE TABLE cargos_2023 (nombre  character varying(80));
 
-- Para copiar los datos desde Excel a la Tavbla


COPY cargos_2023  FROM '/mnt/sda3/PostgreSQL/9.4/thtickets/CargosSubir.csv' HEADER CSV DELIMITER ';';

select * from cargos_2023;


select * from cargos_2023;  -- 159 reg

-- Se valida

insert into tickets_cargos (nombre,"estadoReg") select translate(btrim(nombre::text),'óÓáÁéÉíÍúÚñÑ'::text,'oOaAeEiIuUnN'::text), 'A' from cargos_2023;

select * from tickets_cargos;

 

 