import os
import uuid
import urllib.parse
from flask import jsonify, request, session, current_app
from src.main.config.settings import settings
from src.application.use_cases.orders.create_order import CreateOrderUseCase
from src.infrastructure.repositories.order_repository_sql import OrderRepositorySQL

CART_KEY = "cart"
ALLOWED_VOUCHER = {"png", "jpg", "jpeg", "webp", "pdf"}


def _get_cart():
    return session.get(CART_KEY, [])


def _save_cart(cart):
    session[CART_KEY] = cart
    session.modified = True


def _cart_response(cart):
    total = round(sum(i["price"] * i["quantity"] for i in cart), 2)
    return {"items": cart, "total": total, "item_count": sum(i["quantity"] for i in cart)}


def get_cart():
    return jsonify(_cart_response(_get_cart())), 200


def add_item():
    data = request.get_json()
    required = ["product_id", "color", "size"]
    if not all(k in data for k in required):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    try:
        product_id = int(data["product_id"])
    except (ValueError, TypeError):
        return jsonify({"error": "ID de producto inválido"}), 400

    from src.infrastructure.repositories.product_repository_sql import ProductRepositorySQL
    product = ProductRepositorySQL().find_by_id(product_id)
    if not product or not product.is_active:
        return jsonify({"error": "Producto no disponible o inactivo"}), 404

    cart = _get_cart()
    for item in cart:
        if (item["product_id"] == product_id
                and item["color"] == data["color"]
                and item["size"]  == data["size"]):
            item["quantity"] += 1
            _save_cart(cart)
            return jsonify(_cart_response(cart)), 200

    cart.append({
        "product_id":   product_id,
        "product_name": product.name,
        "color":        data["color"],
        "size":         data["size"],
        "price":        float(product.price),
        "quantity":     1,
        "image_url":    product.images[0] if product.images else "",
    })
    _save_cart(cart)
    return jsonify(_cart_response(cart)), 201


def remove_item(index: int):
    cart = _get_cart()
    if index < 0 or index >= len(cart):
        return jsonify({"error": "Índice inválido"}), 404
    cart.pop(index)
    _save_cart(cart)
    return jsonify(_cart_response(cart)), 200


def clear_cart():
    _save_cart([])
    return jsonify({"items": [], "total": 0, "item_count": 0}), 200


def checkout():
    """
    Recibe: nombre, dirección, notas y foto del voucher (multipart/form-data).
    Guarda el voucher en static/uploads/vouchers/, registra el pedido en la base de datos y genera el link de WhatsApp.
    """
    cart = _get_cart()
    if not cart:
        return jsonify({"error": "El carrito está vacío"}), 400

    name    = request.form.get("name", "").strip()
    address = request.form.get("address", "").strip()
    notes   = request.form.get("notes", "").strip()

    if not name:
        return jsonify({"error": "El nombre es requerido"}), 400
    if not address:
        return jsonify({"error": "La dirección de entrega es requerida"}), 400

    # ── Guardar voucher ───────────────────────────────────────
    voucher_url  = None
    voucher_file = request.files.get("voucher")

    if voucher_file and voucher_file.filename:
        ext = voucher_file.filename.rsplit(".", 1)[-1].lower()
        if ext not in ALLOWED_VOUCHER:
            return jsonify({"error": "Formato de voucher no permitido. Usa JPG, PNG o PDF"}), 400

        from src.infrastructure.services.storage_service import upload_file
        try:
            voucher_url = upload_file(voucher_file, folder="vouchers")
        except Exception as e:
            return jsonify({"error": f"Error al subir el voucher: {str(e)}"}), 500

    total = round(sum(i["price"] * i["quantity"] for i in cart), 2)

    # ── Registrar pedido en la Base de Datos ──────────────────
    try:
        repo = OrderRepositorySQL()
        use_case = CreateOrderUseCase(repo)
        use_case.execute(
            name=name,
            address=address,
            notes=notes,
            total=total,
            voucher_url=voucher_url,
            items_data=cart
        )
    except Exception as e:
        return jsonify({"error": f"Error al guardar pedido en BD: {str(e)}"}), 500

    # ── Generar mensaje WhatsApp ──────────────────────────────
    lines = ["🛍️ *NUEVO PEDIDO — Corazón Valiente*\n"]
    lines.append(f"👤 *Nombre:* {name}")
    if address:
        lines.append(f"📍 *Dirección:* {address}")
    if notes:
        lines.append(f"📝 *Notas:* {notes}")
    lines.append("")
    lines.append("*Productos:*")

    for i, item in enumerate(cart, 1):
        lines.append(
            f"{i}. {item['product_name']}\n"
            f"   Color: {item['color']} | Talla: {item['size']} | "
            f"×{item['quantity']} → S/ {item['price'] * item['quantity']:.2f}"
        )

    lines.append(f"\n💰 *Total: S/ {total:.2f}*")

    if voucher_url:
        absolute_voucher_url = request.host_url + voucher_url.lstrip('/')
        lines.append(f"\n📎 *Voucher de pago (enlace):* {absolute_voucher_url}")
        lines.append("📌 Por favor confirma la recepción en el servidor.")
    else:
        lines.append("\n⚠️ *Voucher de pago:* Pendiente de envío.")

    message = urllib.parse.quote("\n".join(lines))
    whatsapp_link = f"https://wa.me/{settings.WHATSAPP_PHONE}?text={message}"

    # Vaciar carrito de la sesión tras finalizar checkout con éxito
    _save_cart([])

    return jsonify({
        "whatsapp_link": whatsapp_link,
        "voucher_url":   voucher_url,
        "total":         total,
    }), 200
