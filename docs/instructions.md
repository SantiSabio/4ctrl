# Instalación

### Creación del entotrno virtual (`env`)

```shell
# Crear env en la carpeta '.venv'

python3 -m venv .venv

# Activar env

source .venv/bin/activate

# Instalar requerimientos

pip install -r requirements.txt

# Para copiar requerimientos a un archivo requirements.txt:

#pip freeze > requirements.txt
```

### Migración desde la base de datos

```shell
flask db init
flask db migrate -m "Create Products and Brands tables"
flask db upgrade
```

Se creará la carpeta `migrations` en el actual directorio.

### Ingresar consulta SQL

```sql
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
```
