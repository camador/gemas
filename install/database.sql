-- Elimina las tablas antes de crearlas
drop table if exists config;
drop table if exists resoluciones;
drop table if exists jugadores;
drop table if exists gemas;
drop table if exists enemigos;
drop table if exists puntuaciones;


--
-- CONFIGURACIÓN GENERAL
--

-- Creación de la tabla
create table config (
  id integer primary key,
  clave varchar(64),
  valor varchar(128),
  descripcion varchar(255)
);

-- Configuración predeterminada
insert into config (clave, valor, descripcion) values ('VENTANA_ANCHO', '1024', 'Ancho de la ventana en pixels ');
insert into config (clave, valor, descripcion) values ('VENTANA_ALTO', '768', 'Alto de la ventana en pixels');

insert into config (clave, valor, descripcion) values ('DIR_IMG', 'imagenes', 'Directorio de las imágenes');
insert into config (clave, valor, descripcion) values ('DIR_SND', 'sonidos', 'Directorio de los sonidos');

insert into config (clave, valor, descripcion) values ('VELOCIDAD_BASE', '1', 'Velocidad base para todos los sprites');

insert into config (clave, valor, descripcion) values ('FRAMERATE', '60', 'Número máximo de frames por segundo');

insert into config (clave, valor, descripcion) values ('JUGADOR_TIPO', '0', 'Tipo de jugador');

insert into config (clave, valor, descripcion) values ('GEMA_MAX_ACTIVAS', '4', 'Número máximo de gemas activas');
insert into config (clave, valor, descripcion) values ('GEMA_RESPAWN', '1800', 'Tiempo (en milisegundos) para el respawn de las gemas');

insert into config (clave, valor, descripcion) values ('ENEMIGO_RESPAWN', '10000', 'Tiempo (en milisegundos) para el respawn de las enemigos');

--
-- RESOLUCIONES
--

-- Creación de la tabla
create table resoluciones (
  id integer primary key,
  descripcion varchar(12),
  ancho varchar(4),
  alto varchar(4)
);

insert into resoluciones (descripcion, ancho, alto) values ('800 x 600', '800', '600');
insert into resoluciones (descripcion, ancho, alto) values ('1024 x 768', '1024', '768');


--
-- JUGADORES
--

-- Creación de la tabla
create table jugadores (
  id integer primary key,
  tipo integer,
  fichero varchar(50),
  gameover varchar(50),
  tamanio_x integer,
  tamanio_y integer,
  factor_velocidad float
);

insert into jugadores (tipo, fichero, gameover, tamanio_x, tamanio_y, factor_velocidad) values (0, 'jugador1.png', 'gameover.ogg', 77, 90, 1);
insert into jugadores (tipo, fichero, gameover, tamanio_x, tamanio_y, factor_velocidad) values (1, 'jugador2.png', 'gameover.ogg', 67, 88, 1);
insert into jugadores (tipo, fichero, gameover, tamanio_x, tamanio_y, factor_velocidad) values (2, 'jugador3.png', 'gameover.ogg', 68, 91, 1);
insert into jugadores (tipo, fichero, gameover, tamanio_x, tamanio_y, factor_velocidad) values (3, 'jugador4.png', 'gameover.ogg', 76, 89, 1);
insert into jugadores (tipo, fichero, gameover, tamanio_x, tamanio_y, factor_velocidad) values (4, 'jugador5.png', 'gameover.ogg', 76, 99, 1);

--
-- GEMAS
--

-- Creación de la tabla
create table gemas (
  id integer primary key,
  tipo integer,
  fichero varchar(50),
  gemarota varchar(50),
  tick varchar(50),
  vida float,
  tamanio_x integer,
  tamanio_y integer,
  indestructible integer,
  descripcion varchar(128),
  probabilidad integer
);

insert into gemas (tipo, fichero, gemarota, tick, vida, tamanio_x, tamanio_y, indestructible, descripcion, probabilidad) values (0, 'gema1.png', 'gemarota.ogg', 'minando.ogg', 2, 95, 111, 0, 'Gema básica', 65);
insert into gemas (tipo, fichero, gemarota, tick, vida, tamanio_x, tamanio_y, indestructible, descripcion, probabilidad) values (1, 'gema2.png', 'gemarota.ogg', 'minando.ogg', 4, 95, 112, 0, 'Gema un poco más duradera', 30);
insert into gemas (tipo, fichero, gemarota, tick, vida, tamanio_x, tamanio_y, indestructible, descripcion, probabilidad) values (2, 'gema3.png', 'gemarota.ogg', 'minando.ogg', 1, 95, 112, 1, 'Gema indestructible', 5);
                                                                                                
--
-- ENEMIGOS
--

-- Creación de la tabla
create table enemigos (
  id integer primary key,
  tipo integer,
  fichero varchar(50),
  tamanio_x integer,
  tamanio_y integer,
  factor_velocidad float,
  descripcion varchar(128),
  probabilidad integer
);

insert into enemigos (tipo, fichero, tamanio_x, tamanio_y, factor_velocidad, descripcion, probabilidad) values (0, 'enemigo.png', 49, 38, 0.5, 'Enemigo rápido', 80);
insert into enemigos (tipo, fichero, tamanio_x, tamanio_y, factor_velocidad, descripcion, probabilidad) values (1, 'roca.png', 48, 49, 0.15, 'Enemigo lento que rompe las gemas', 20);


--
-- PUNTUACIONES
--

-- Creación de la tabla
create table puntuaciones (
  id integer primary key,
  nombre varchar(50),
  puntos integer,
  fecha datetime
);
