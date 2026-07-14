-- ============================================================
-- Migración inicial — Corazón Valiente (Versión Aiven/Vercel)
-- Tablas: products, users, orders, order_items
-- ============================================================

-- ── Productos ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `products` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(200) NOT NULL,
  `slug` VARCHAR(200) NOT NULL UNIQUE,
  `description` TEXT DEFAULT NULL,
  `price` DECIMAL(10,2) NOT NULL,
  `original_price` DECIMAL(10,2) DEFAULT NULL,
  `stock` INT DEFAULT 0,
  `colors_json` TEXT DEFAULT NULL,
  `sizes_json` TEXT DEFAULT NULL,
  `images_json` TEXT DEFAULT NULL,
  `is_active` TINYINT(1) DEFAULT 1,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ── Usuarios admin ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `email` VARCHAR(200) NOT NULL UNIQUE,
  `name` VARCHAR(200) NOT NULL,
  `password_hash` VARCHAR(256) NOT NULL,
  `role` VARCHAR(20) DEFAULT 'admin',
  `is_active` TINYINT(1) DEFAULT 1,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ── Órdenes ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `orders` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL,
  `address` VARCHAR(255) NOT NULL,
  `notes` TEXT DEFAULT NULL,
  `total` DECIMAL(10,2) NOT NULL,
  `voucher_url` VARCHAR(500) DEFAULT NULL,
  `status` VARCHAR(50) DEFAULT 'Pendiente',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ── Items de Órdenes ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `order_items` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `order_id` INT NOT NULL,
  `product_id` INT NOT NULL,
  `product_name` VARCHAR(255) NOT NULL,
  `color` VARCHAR(100) DEFAULT NULL,
  `size` VARCHAR(50) DEFAULT NULL,
  `price` DECIMAL(10,2) NOT NULL,
  `quantity` INT NOT NULL,
  CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ── Seed: producto de ejemplo ────────────────────────────────
INSERT IGNORE INTO `products` (`id`, `name`, `slug`, `description`, `price`, `original_price`, `stock`, `colors_json`, `sizes_json`, `images_json`, `is_active`) 
VALUES (1, 'Polo Corazón Valiente', 'polo-corazon-valiente', 'Polo oversize de calidad premium con diseño potente, ideal para un look urbano, moderno y con personalidad.', 79.00, 99.00, 50, '["Negro", "Índigo", "Hueso", "Vino"]', '["S", "M", "L", "XL"]', '[]', 1);

-- ── Seed: usuario admin por defecto (Password: Admin456) ─────
INSERT IGNORE INTO `users` (`id`, `email`, `name`, `password_hash`, `role`, `is_active`) 
VALUES (1, 'admin@corazonvaliente.com', 'Administrador', 'scrypt:32768:8:1$Fjs4Y7ds74IxECZ1$627882f25ef55396c8d56d071e7e45a9e2aff8e85330d01d767ef5c761322a5686ec9b86faff68f5ac473cdc581da298dbe83cb06820218ec689b73cae8d8e2b', 'admin', 1);
