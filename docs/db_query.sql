-- Tabla 'products'
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL
);

-- Tabla 'brands'
CREATE TABLE brands (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    amount_art INT NOT NULL
);

-- Crear índice en la columna 'name' de la tabla 'brands'

CREATE INDEX idx_brands_name ON brands (name);

-- Agregar columna 'brand' a la tabla 'products' y definir la restricción de clave foránea

ALTER TABLE products
ADD COLUMN brand VARCHAR(100),
ADD CONSTRAINT fk_brand
FOREIGN KEY (brand) REFERENCES brands(name);
