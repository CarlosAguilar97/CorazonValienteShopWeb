# 🛍️ Corazón Valiente — Ecommerce

Ecommerce de una sola página con carrito funcional, selección de color/talla y pedido por WhatsApp.

## Stack

- **Backend**: Python + Flask
- **Frontend**: HTML + Tailwind CSS (templates Jinja2)
- **Base de datos**: MySQL 8
- **Contenedores**: Docker + Docker Compose

## Estructura

```
ecommerce/
├── src/
│   ├── main/           → Entrypoint Flask + config
│   ├── domain/         → Entidades, repositorios abstractos, servicios de dominio
│   ├── application/    → Casos de uso, DTOs, puertos
│   ├── infrastructure/ → MySQL, repos concretos, WhatsApp, Cloudinary
│   ├── presentation/   → Controladores, rutas Flask, vistas HTML
│   └── tests/
├── docker-compose.yml
├── requirements.txt
└── .env
```

## Inicio rápido

```bash
# 1. Clonar y entrar al proyecto
git clone <repo> && cd ecommerce

# 2. Copiar variables de entorno
cp .env.example .env  # editar valores

# 3. Levantar con Docker
docker compose up --build

# 4. Abrir en el navegador
http://localhost:5000
```

## Variables de entorno (.env)

| Variable | Descripción |
|---|---|
| `MYSQL_HOST` | Host de MySQL |
| `MYSQL_PORT` | Puerto (default 3306) |
| `MYSQL_USER` | Usuario |
| `MYSQL_PASSWORD` | Contraseña |
| `MYSQL_DB` | Nombre de la base de datos |
| `WHATSAPP_PHONE` | Número con código de país (ej: 51999999999) |
| `SECRET_KEY` | Clave secreta Flask |
| `CLOUDINARY_URL` | URL de Cloudinary (opcional, para imágenes) |

## API Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/` | Landing page |
| GET | `/api/products` | Listar productos |
| GET | `/api/products/<id>` | Detalle de producto |
| POST | `/api/cart/add` | Agregar al carrito |
| DELETE | `/api/cart/remove/<id>` | Quitar del carrito |
| GET | `/api/cart` | Ver carrito |
| POST | `/api/orders` | Crear orden |
| GET | `/api/orders/whatsapp` | Generar link WhatsApp |
