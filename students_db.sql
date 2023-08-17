create database if not exists students_db;
use students_db;
drop TABLE if exists materias;
drop TABLE if exists estudiantes;
drop table if exists maestro;
CREATE TABLE estudiantes (
    numero_control INT PRIMARY KEY,
    nombre VARCHAR (1000) NULL,
    username VARCHAR (1000) NULL,
    contraseña VARCHAR(1000) NULL
);
CREATE TABLE maestro (
    cve_maestro INT PRIMARY KEY,
    nombre VARCHAR (1000) NULL,
    apellido VARCHAR (1000) NULL,
    correo varchar (100) null,
    edificio varchar (100) null,
    telefono varchar (100) null,
    cubiculo INT null,
    direccion varchar (100) null
);
CREATE TABLE materias (
    cve_mat INT PRIMARY KEY,
    nombre varchar (50) not null,
    horas_practicas varchar (100) null,
    horas_teoricas varchar (100) null,
    carrera varchar (100) null,
    unidades INT null,
	cve_maestro int not NULL,
    numero_control int not null,
    foreign key (numero_control) 
    references estudiantes (numero_control),
    foreign key (cve_maestro) 
    references maestro (cve_maestro)
);

