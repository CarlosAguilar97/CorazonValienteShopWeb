-- ============================================================
-- Migración inicial — Corazón Valiente
-- Solo persiste: products, users (admin)
-- Carrito: sesión Flask | Órdenes: solo por WhatsApp
-- ============================================================

CREATE DATABASE IF NOT EXISTS corazon_valiente
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE corazon_valiente;

-- ── Productos ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS products (
  id             INT AUTO_INCREMENT PRIMARY KEY,
  name           VARCHAR(200)   NOT NULL,
  slug           VARCHAR(200)   NOT NULL UNIQUE,
  description    TEXT,
  price          DECIMAL(10,2)  NOT NULL,
  original_price DECIMAL(10,2),
  stock          INT            DEFAULT 0,
  colors_json    TEXT           DEFAULT '[]',
  sizes_json     TEXT           DEFAULT '["S","M","L","XL"]',
  images_json    TEXT           DEFAULT '[]',
  is_active      BOOLEAN        DEFAULT TRUE,
  created_at     DATETIME       DEFAULT CURRENT_TIMESTAMP,
  updated_at     DATETIME       DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ── Usuarios admin ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  email         VARCHAR(200)  NOT NULL UNIQUE,
  name          VARCHAR(200)  NOT NULL,
  password_hash VARCHAR(256)  NOT NULL,
  role          VARCHAR(20)   DEFAULT 'admin',
  is_active     BOOLEAN       DEFAULT TRUE,
  created_at    DATETIME      DEFAULT CURRENT_TIMESTAMP
);

-- ── Seed: producto de ejemplo ────────────────────────────────
INSERT IGNORE INTO products
  (name, slug, description, price, original_price, stock, colors_json, sizes_json, images_json)
VALUES (
  'Polo Corazón Valiente',
  'polo-corazon-valiente',
  'Polo oversize de calidad premium con diseño potente, ideal para un look urbano, moderno y con personalidad.',
  79.00, 99.00, 50,
  '["Negro","Índigo","Hueso","Vino"]',
  '["S","M","L","XL"]',
  '[]'
);

-- ── Seed: usuario admin por defecto ─────────────────────────
-- Password: Admin123! (cámbialo inmediatamente en producción)
INSERT IGNORE INTO users (email, name, password_hash, role)
VALUES (
  'admin@corazonvaliente.com',
  'Administrador',
  'pbkdf2:sha256:600000$salt$hash_placeholder',
  'admin'
);
-- NOTA: el hash real se genera al ejecutar `flask create-admin`
