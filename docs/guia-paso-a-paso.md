# 🗺️ Guía paso a paso — Corazón Valiente Ecommerce

## Paso 1 — Prerequisitos

Instala estas herramientas si aún no las tienes:

```bash
# Docker Desktop (incluye Docker Compose)
https://www.docker.com/products/docker-desktop/

# Git
https://git-scm.com/

# Python 3.12+ (para desarrollo local sin Docker)
https://www.python.org/downloads/

# Editor recomendado: VS Code
https://code.visualstudio.com/
```

---

## Paso 2 — Clonar / crear el proyecto

```bash
# Opción A: clonar desde tu repo
git clone <url-de-tu-repo> ecommerce
cd ecommerce

# Opción B: inicializar desde cero
mkdir ecommerce && cd ecommerce
git init
```

---

## Paso 3 — Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env    # o simplemente editar el .env ya creado

# Editar los valores importantes:
#   WHATSAPP_PHONE=51999999999   ← tu número real
#   SECRET_KEY=una_clave_larga_y_aleatoria
#   MYSQL_PASSWORD=tu_password
```

---

## Paso 4 — Levantar con Docker (recomendado)

```bash
# Construir imágenes y levantar contenedores en segundo plano
docker compose up --build -d

# Ver logs en tiempo real
docker compose logs -f web

# Verificar que ambos servicios están corriendo
docker compose ps
```

La app estará disponible en: **http://localhost:5000**
MySQL estará expuesto en: **localhost:3307** (para conectar con DBeaver u otro cliente)

---

## Paso 5 — Levantar en modo desarrollo local (sin Docker)

```bash
# Crear entorno virtual
python -m venv venv

# Activar (Linux/Mac)
source venv/bin/activate

# Activar (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Necesitas MySQL corriendo localmente.
# Cambia MYSQL_HOST=localhost en tu .env

# Ejecutar
python src/main/app.py
```

---

## Paso 6 — Verificar que todo funciona

```bash
# Health check general
curl http://localhost:5000/

# Listar productos (debe devolver JSON)
curl http://localhost:5000/api/products/

# Ver carrito vacío
curl http://localhost:5000/api/cart/

# Agregar un producto al carrito
curl -X POST http://localhost:5000/api/cart/add \
  -H "Content-Type: application/json" \
  -d '{"product_id":1,"product_name":"Polo Corazón Valiente","color":"Negro","size":"M","price":79}'
```

---

## Paso 7 — Agregar imágenes de producto

### Opción A — Imágenes locales (desarrollo)

1. Crea la carpeta `src/presentation/static/images/`
2. Coloca tus imágenes: `polo-negro.jpg`, `polo-hueso.jpg`, etc.
3. Actualiza la BD con la URL: `/static/images/polo-negro.jpg`

### Opción B — Cloudinary (producción)

```bash
# En .env:
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name

# Desde Python puedes subir así:
import cloudinary.uploader
result = cloudinary.uploader.upload("ruta/imagen.jpg")
url = result["secure_url"]  # esta URL va en la BD
```

---

## Paso 8 — Personalizar el número de WhatsApp

En `.env`:
```
WHATSAPP_PHONE=51987654321   # código de país + número, sin + ni espacios
```

En `src/presentation/views/index.html` busca la función `openWhatsApp` y actualiza:
```js
window.open(`https://wa.me/51987654321?text=${encoded}`, "_blank");
```

---

## Paso 9 — Agregar más productos a la BD

Conecta con DBeaver o TablePlus a `localhost:3307` y ejecuta:

```sql
INSERT INTO products (name, slug, description, price, original_price, stock, colors_json, sizes_json)
VALUES (
  'Polo Edición Especial',
  'polo-edicion-especial',
  'Descripción del producto',
  89.00, 110.00, 30,
  '["Negro","Blanco"]',
  '["S","M","L","XL","XXL"]'
);
```

---

## Paso 10 — Deploy en producción (VPS / Oracle Cloud)

```bash
# En el servidor, clonar y configurar
git clone <repo> && cd ecommerce
nano .env   # configurar con valores de producción

# Levantar
docker compose -f docker-compose.yml up -d --build

# Con Traefik (que ya conoces), agregar labels al servicio web:
#   traefik.enable=true
#   traefik.http.routers.ecommerce.rule=Host(`tudominio.com`)
#   traefik.http.services.ecommerce.loadbalancer.server.port=5000
```

---

## Estructura final de archivos

```
ecommerce/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
├── .gitignore
├── README.md
└── src/
    ├── main/
    │   ├── app.py                        ← Entrypoint Flask
    │   └── config/
    │       ├── settings.py               ← Variables de entorno
    │       ├── database.py               ← SQLAlchemy init
    │       └── logger.py                 ← Logger centralizado
    ├── domain/
    │   ├── entities/                     ← Product, CartItem, Order
    │   ├── value_objects/                ← Money, Phone
    │   ├── repositories/                 ← Contratos abstractos
    │   └── services/                     ← PricingService
    ├── application/
    │   ├── use_cases/                    ← list_products, create_order
    │   └── dto/                          ← ProductDTO, OrderDTO, CartDTO
    ├── infrastructure/
    │   ├── database/models/              ← SQLAlchemy models
    │   ├── database/migrations/          ← SQL init + seeds
    │   └── repositories/                 ← Implementaciones SQL
    └── presentation/
        ├── controllers/                  ← product, cart, order
        ├── routes/                       ← Blueprints Flask
        ├── views/index.html              ← Frontend completo
        └── middlewares/error_handler.py  ← Manejo de errores
```

---

## Endpoints disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Landing page |
| GET | `/api/products/` | Listar productos activos |
| GET | `/api/products/<id>` | Detalle de producto |
| POST | `/api/products/` | Crear producto |
| DELETE | `/api/products/<id>` | Eliminar producto |
| GET | `/api/cart/` | Ver carrito (sesión) |
| POST | `/api/cart/add` | Agregar ítem |
| DELETE | `/api/cart/remove/<index>` | Quitar ítem por índice |
| DELETE | `/api/cart/clear` | Vaciar carrito |
| POST | `/api/orders/` | Crear orden → genera link WhatsApp |
| GET | `/api/orders/` | Listar órdenes |
| GET | `/api/orders/<id>` | Ver orden |

---

## Problemas frecuentes

| Error | Solución |
|-------|----------|
| `Connection refused` MySQL | Esperar que el healthcheck pase: `docker compose logs db` |
| `ModuleNotFoundError` | Verificar que `venv` está activo y `pip install` corrió |
| `Template not found` | Verificar path en `app.py` → `template_folder` |
| WhatsApp no abre | Revisar `WHATSAPP_PHONE` en `.env`, sin `+` ni espacios |
