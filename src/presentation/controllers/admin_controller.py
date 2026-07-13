import os
import uuid
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from werkzeug.utils import secure_filename

from src.application.use_cases.products.list_products import ListProductsUseCase
from src.application.use_cases.products.create_product import CreateProductUseCase
from src.application.use_cases.products.update_product import UpdateProductUseCase
from src.application.use_cases.products.delete_product import DeleteProductUseCase
from src.application.dto.product_dto import CreateProductDTO
from src.infrastructure.repositories.product_repository_sql import ProductRepositorySQL
from src.application.use_cases.orders.list_orders import ListOrdersUseCase
from src.infrastructure.repositories.order_repository_sql import OrderRepositorySQL

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


def _repo():
    return ProductRepositorySQL()


def _allowed(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def _save_image(file, app) -> str:
    """Guarda el archivo delegando en el Storage Service (Cloudinary o Local)."""
    from src.infrastructure.services.storage_service import upload_file
    return upload_file(file, folder="products")


@login_required
def dashboard():
    products = ListProductsUseCase(_repo()).execute(only_active=False)
    orders = ListOrdersUseCase(OrderRepositorySQL()).execute()
    return render_template("admin/dashboard.html", products=products, orders=orders)


@login_required
def order_update_status(order_id: int):
    status = request.form.get("status")
    if status:
        repo = OrderRepositorySQL()
        order = repo.find_by_id(order_id)
        if order:
            order.status = status
            repo.save(order)
            flash(f"Estado del pedido #{order_id} actualizado a {status}.", "success")
        else:
            flash("Pedido no encontrado.", "error")
    return redirect(url_for("admin.dashboard"))


@login_required
def product_new_get():
    return render_template("admin/product_form.html", product=None)


@login_required
def product_new_post():
    from flask import current_app
    data   = request.form
    images = []

    # Imágenes subidas como archivo
    files = request.files.getlist("images_files")
    for f in files:
        if f and f.filename and _allowed(f.filename):
            images.append(_save_image(f, current_app))

    # URLs manuales (campo texto, separadas por coma)
    extra_urls = [u.strip() for u in data.get("images_urls", "").split(",") if u.strip()]
    images.extend(extra_urls)

    colors = [c.strip() for c in data.get("colors", "").split(",") if c.strip()]
    sizes  = [s.strip() for s in data.get("sizes",  "").split(",") if s.strip()]

    # Controlar conversiones numéricas seguras
    try:
        price = float(data.get("price", 0))
    except ValueError:
        price = 0.0

    try:
        original_price = float(data.get("original_price")) if data.get("original_price") else None
    except ValueError:
        original_price = None

    try:
        stock = int(data.get("stock", 0))
    except ValueError:
        stock = 0

    dto = CreateProductDTO(
        name=data.get("name", "").strip(),
        description=data.get("description", ""),
        price=price,
        stock=stock,
        original_price=original_price,
        colors=colors,
        sizes=sizes or ["S", "M", "L", "XL"],
        images=images,
    )

    try:
        CreateProductUseCase(_repo()).execute(dto)
        flash("Producto creado correctamente.", "success")
        return redirect(url_for("admin.dashboard"))
    except ValueError as e:
        flash(str(e), "error")
        # Retornar el formulario conservando la información que ingresó
        mock_product = {
            "name": dto.name,
            "description": dto.description,
            "price": dto.price,
            "original_price": dto.original_price,
            "stock": dto.stock,
            "colors": dto.colors,
            "sizes": dto.sizes,
            "images": dto.images,
        }
        return render_template("admin/product_form.html", product=mock_product)


@login_required
def product_edit_get(product_id: int):
    product = _repo().find_by_id(product_id)
    if not product:
        flash("Producto no encontrado.", "error")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/product_form.html", product=product)


@login_required
def product_edit_post(product_id: int):
    from flask import current_app
    data   = request.form
    repo   = _repo()

    # Mantener imágenes existentes
    product = repo.find_by_id(product_id)
    images  = list(product.images) if product else []

    # Nuevas imágenes subidas
    files = request.files.getlist("images_files")
    for f in files:
        if f and f.filename and _allowed(f.filename):
            images.append(_save_image(f, current_app))

    # URLs manuales adicionales
    extra_urls = [u.strip() for u in data.get("images_urls", "").split(",") if u.strip()]
    images.extend(extra_urls)

    # Eliminar imágenes marcadas para borrar
    remove_list = request.form.getlist("remove_image")
    images = [img for img in images if img not in remove_list]

    colors = [c.strip() for c in data.get("colors", "").split(",") if c.strip()]
    sizes  = [s.strip() for s in data.get("sizes",  "").split(",") if s.strip()]

    try:
        price = float(data.get("price", 0))
    except ValueError:
        price = 0.0

    try:
        original_price = float(data.get("original_price")) if data.get("original_price") else None
    except ValueError:
        original_price = None

    try:
        stock = int(data.get("stock", 0))
    except ValueError:
        stock = 0

    update_data = {
        "name":           data.get("name", "").strip(),
        "description":    data.get("description", ""),
        "price":          price,
        "stock":          stock,
        "original_price": original_price,
        "colors":         colors,
        "sizes":          sizes or ["S", "M", "L", "XL"],
        "images":         images,
        "is_active":      data.get("is_active") == "on",
    }
    try:
        UpdateProductUseCase(repo).execute(product_id, update_data)
        flash("Producto actualizado.", "success")
        return redirect(url_for("admin.dashboard"))
    except ValueError as e:
        flash(str(e), "error")
        # Retornar el formulario conservando la información que ingresó
        mock_product = {
            "id":             product_id,
            "name":           update_data["name"],
            "description":    update_data["description"],
            "price":          update_data["price"],
            "original_price": update_data["original_price"],
            "stock":          update_data["stock"],
            "colors":         update_data["colors"],
            "sizes":          update_data["sizes"],
            "images":         update_data["images"],
            "is_active":      update_data["is_active"],
        }
        return render_template("admin/product_form.html", product=mock_product)


@login_required
def product_delete(product_id: int):
    deleted = DeleteProductUseCase(_repo()).execute(product_id)
    flash("Producto eliminado." if deleted else "Producto no encontrado.", "success" if deleted else "error")
    return redirect(url_for("admin.dashboard"))
