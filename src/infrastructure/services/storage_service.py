import os
import uuid
import cloudinary
import cloudinary.uploader
from src.main.config.settings import settings

def upload_file(file, folder: str = "ecommerce") -> str:
    """
    Sube un archivo. Si CLOUDINARY_URL está configurado en settings, lo sube a Cloudinary.
    De lo contrario, lo guarda localmente en el servidor.
    Retorna la URL pública/accesible del archivo.
    """
    if settings.CLOUDINARY_URL:
        # Cloudinary se autoconfigura usando la variable de entorno CLOUDINARY_URL
        result = cloudinary.uploader.upload(file, folder=folder)
        return result.get("secure_url")
    
    # Caída a guardado local
    from flask import current_app
    ext = file.filename.rsplit(".", 1)[-1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    
    # Crear carpetas si no existen
    upload_folder = os.path.join(current_app.static_folder, "uploads", folder)
    os.makedirs(upload_folder, exist_ok=True)
    
    file_path = os.path.join(upload_folder, unique_name)
    file.save(file_path)
    
    return f"/static/uploads/{folder}/{unique_name}"
