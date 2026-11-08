# Tienda de componentes

Catálogo web para explorar y cotizar piezas de computador.

## Ficha del proyecto
- **Organización o plataforma:** Tienda de componentes
- **Giro:** Venta y cotización de componentes de computador
- **Integrantes:** Completar con nombre y RUT de ambos integrantes
- **Entidad de contexto:** `Categoria`
- **Entidad principal:** `Pieza`
- **Propósito de la sesión:** Cotizador temporal con cantidades, subtotal, IVA y total

## Descripción
Los clientes pueden buscar piezas por nombre, código o descripción, filtrar por
categoría, revisar la ficha del producto y añadir unidades a un cotizador de sesión.
El personal con rol `is_staff` gestiona el inventario desde el panel protegido.

## Tecnologías
- Python 3.14
- Django 6.1.3
- SQLite
- Pillow 12.0.0
- python-dotenv 1.1.1
- Bootstrap 5

## Instalación local

En Windows PowerShell, desde la raíz del proyecto:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

`SECRET_KEY` puede dejarse vacía para desarrollo local: Django genera una clave temporal. Para un entorno no local, define `SECRET_KEY`, `DEBUG=False` y `ALLOWED_HOSTS` en `.env`; nunca publiques ese archivo.

## Migraciones y datos de prueba

```powershell
python manage.py migrate
python manage.py poblar_datos
python manage.py runserver
```

El comando `poblar_datos` crea cinco categorías, catorce piezas y cuentas de prueba de forma idempotente. Las contraseñas de las cuentas nuevas se generan aleatoriamente y se muestran una vez en la terminal. También se pueden definir `SEED_ADMIN_PASSWORD` y `SEED_USER_PASSWORD` en `.env` antes de ejecutarlo.

Las imágenes de los productos y las que se cargan desde el panel se almacenan en `images/piezas/`.

El usuario administrador inicia en `/admin/`; el usuario estándar sirve para probar el flujo de cliente. Guarda las claves generadas durante el comando: no se incluyen en el repositorio.

Si una cuenta ya existía, el comando la conserva y no vuelve a mostrar su clave. Para restablecer la clave de un administrador existente, ejecuta `python manage.py changepassword admin`.

Para verificar la instalación:

```powershell
python manage.py check
python manage.py test
```

## Funcionalidades
- Catálogo público con búsqueda y filtros por categoría.
- Ficha de detalle del producto.
- Carrito almacenado en sesión.
- Registro e inicio de sesión.
- Administración protegida de productos y categorías.

## Bitácora de uso de IA

### Caso 1: Modelado de datos
- **Prompt:** Diseñar modelos Django para un catálogo de piezas con categorías, inventario, imágenes y perfiles de clientes.
- **Respuesta técnica:** Separar `Categoria`, `Pieza` y `Perfil`; usar `ForeignKey(PROTECT)`, código único, validación de valores no negativos y `ImageField`.
- **Adaptación aplicada:** Se mantuvo el dominio de la tienda y se verificó el esquema mediante migraciones y pruebas.

### Caso 2: Consultas, sesiones e imágenes
- **Prompt:** Implementar búsqueda multi-campo, paginación y un cotizador transitorio que valide stock y calcule IVA.
- **Respuesta técnica:** Usar `Q`, `Paginator`, `request.session`, `Decimal` y operaciones transaccionales al simular la compra.
- **Adaptación aplicada:** Se probaron filtros, límites de stock, subtotal, IVA y las imágenes locales asignadas a productos.

### Caso 3: Seguridad y roles
- **Prompt:** Proteger el CRUD del personal y permitir el registro de clientes con datos complementarios.
- **Respuesta técnica:** Aplicar `login_required`, comprobación `is_staff`, CSRF y `UserCreationForm`.
- **Adaptación aplicada:** El registro crea un `Perfil` con RUT y teléfono; se comprobó la configuración y el conjunto de pruebas.

## Trabajo colaborativo
- **Repositorio:** https://github.com/SrBroda/EVA3_Back_TiendaPiezas
- **Integrante 1:** Completar nombre, RUT y aportes.
- **Integrante 2:** Completar nombre, RUT y aportes.

> Antes de entregar, reemplacen los campos pendientes de integrantes con los datos reales del equipo y registren los commits de ambos colaboradores.

## Preparar el ZIP de entrega

Incluye el código y `images/` para conservar las fotografías de los productos. Excluye `.venv/`, `.env`, `__pycache__/` y `db.sqlite3`; las migraciones y `poblar_datos` reconstruyen el esquema y los datos.


-admin12345678