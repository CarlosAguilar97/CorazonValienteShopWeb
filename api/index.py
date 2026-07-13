import sys
import os

# Agregar la raíz del proyecto al sys.path para permitir importaciones correctas de "src"
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.main.app import app
