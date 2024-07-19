# myproject

CRUD realizado en python con flask y conectadoa una base de datos por mysql
Este proyecto se trata de una aplicacion de gestin de stock a travez de bases de datos relacionales, con una interfaz web para el uso del usuario



APLICACION CLIENTE SERVIDOR PARA PARCIAL EN JULIO




PARTE MIGRATE

flask db init
flask db migrate -m "Create Productos and Marcas tables"
flask db upgrade


SQL
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    precio FLOAT NOT NULL
);


CREATE TABLE marcas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    cant_art INT NOT NULL
);

-- Crear índice en la columna 'nombre' de la tabla 'marcas'
CREATE INDEX idx_marcas_nombre ON marcas (nombre);

-- Agregar columna 'marca' a la tabla 'productos' y definir la restricción de clave foránea
ALTER TABLE productos
ADD COLUMN marca VARCHAR(100),
ADD CONSTRAINT fk_marca
FOREIGN KEY (marca) REFERENCES marcas(nombre);
