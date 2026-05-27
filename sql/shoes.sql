-- SQL dump for demo exam project
-- Generated from local database `shoes`
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";
SET NAMES utf8mb4;
START TRANSACTION;
CREATE DATABASE IF NOT EXISTS `shoes` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `shoes`;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `orders`;
DROP TABLE IF EXISTS `products`;
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `pickup_points`;
DROP TABLE IF EXISTS `order_statuses`;
DROP TABLE IF EXISTS `units`;
DROP TABLE IF EXISTS `suppilers`;
DROP TABLE IF EXISTS `manufactures`;
DROP TABLE IF EXISTS `categories`;
DROP TABLE IF EXISTS `roles`;

-- Structure for table `roles`
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(222) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Structure for table `categories`
CREATE TABLE `categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(222) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Structure for table `manufactures`
CREATE TABLE `manufactures` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(111) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Structure for table `suppilers`
CREATE TABLE `suppilers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(222) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Structure for table `units`
CREATE TABLE `units` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(222) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Structure for table `order_statuses`
CREATE TABLE `order_statuses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(55) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Structure for table `pickup_points`
CREATE TABLE `pickup_points` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `address` varchar(222) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Structure for table `users`
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `full_name` varchar(222) COLLATE utf8mb4_unicode_ci NOT NULL,
  `login` varchar(222) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(222) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Structure for table `products`
CREATE TABLE `products` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `article` varchar(55) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(55) COLLATE utf8mb4_unicode_ci NOT NULL,
  `category_id` int(11) NOT NULL,
  `description` varchar(55) COLLATE utf8mb4_unicode_ci NOT NULL,
  `manufacture_id` int(11) NOT NULL,
  `suppiler_id` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `unit_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `discount` decimal(5,2) NOT NULL,
  `image_path` varchar(55) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `article` (`article`),
  KEY `category_id` (`category_id`),
  KEY `manufacture_id` (`manufacture_id`),
  KEY `suppiler_id` (`suppiler_id`),
  KEY `unit_id` (`unit_id`),
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`),
  CONSTRAINT `products_ibfk_2` FOREIGN KEY (`manufacture_id`) REFERENCES `manufactures` (`id`),
  CONSTRAINT `products_ibfk_3` FOREIGN KEY (`suppiler_id`) REFERENCES `suppilers` (`id`),
  CONSTRAINT `products_ibfk_4` FOREIGN KEY (`unit_id`) REFERENCES `units` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Structure for table `orders`
CREATE TABLE `orders` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `status_id` int(11) NOT NULL,
  `pickup_point_id` int(11) NOT NULL,
  `order_date` date NOT NULL,
  `delivery_date` date NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pickup_point_id` (`pickup_point_id`),
  KEY `product_id` (`product_id`),
  KEY `status_id` (`status_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`pickup_point_id`) REFERENCES `pickup_points` (`id`),
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `orders_ibfk_3` FOREIGN KEY (`status_id`) REFERENCES `order_statuses` (`id`),
  CONSTRAINT `orders_ibfk_4` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table `roles`
INSERT INTO `roles` (`id`, `title`) VALUES (1, 'admin');
INSERT INTO `roles` (`id`, `title`) VALUES (2, 'client');
INSERT INTO `roles` (`id`, `title`) VALUES (3, 'guest');
INSERT INTO `roles` (`id`, `title`) VALUES (4, 'manager');

-- Data for table `categories`
INSERT INTO `categories` (`id`, `title`) VALUES (1, 'Кроссовки');
INSERT INTO `categories` (`id`, `title`) VALUES (2, 'Туфли');

-- Data for table `manufactures`
INSERT INTO `manufactures` (`id`, `title`) VALUES (1, 'Завод Москва');
INSERT INTO `manufactures` (`id`, `title`) VALUES (2, 'Завод Питер');

-- Data for table `suppilers`
INSERT INTO `suppilers` (`id`, `title`) VALUES (1, 'Поставщик Москва');
INSERT INTO `suppilers` (`id`, `title`) VALUES (2, 'Поставщик Питер');
INSERT INTO `suppilers` (`id`, `title`) VALUES (3, 'Поставщик TORCH');

-- Data for table `units`
INSERT INTO `units` (`id`, `title`) VALUES (1, 'Шт');

-- Data for table `order_statuses`
INSERT INTO `order_statuses` (`id`, `title`) VALUES (1, 'Создан');
INSERT INTO `order_statuses` (`id`, `title`) VALUES (2, 'Оформлен');
INSERT INTO `order_statuses` (`id`, `title`) VALUES (3, 'Оплачен');

-- Data for table `pickup_points`
INSERT INTO `pickup_points` (`id`, `address`) VALUES (1, 'Moscow');
INSERT INTO `pickup_points` (`id`, `address`) VALUES (2, 'Saint-Peterburg');

-- Data for table `users`
INSERT INTO `users` (`id`, `full_name`, `login`, `password`, `role_id`) VALUES (1, 'Устименко Лев Романович', 'levandr', '1', 1);
INSERT INTO `users` (`id`, `full_name`, `login`, `password`, `role_id`) VALUES (2, 'admin', 'admin', '1', 1);
INSERT INTO `users` (`id`, `full_name`, `login`, `password`, `role_id`) VALUES (3, 'manager', 'manager', '1', 4);
INSERT INTO `users` (`id`, `full_name`, `login`, `password`, `role_id`) VALUES (4, 'client', 'client', '1', 2);

-- Data for table `products`
INSERT INTO `products` (`id`, `article`, `title`, `category_id`, `description`, `manufacture_id`, `suppiler_id`, `price`, `unit_id`, `quantity`, `discount`, `image_path`) VALUES (1, '12333', 'Кроссовки', 1, 'кроссы', 1, 1, 1400.00, 1, 45, 90.00, '123123.png');
INSERT INTO `products` (`id`, `article`, `title`, `category_id`, `description`, `manufacture_id`, `suppiler_id`, `price`, `unit_id`, `quantity`, `discount`, `image_path`) VALUES (3, '123', 'Nke Monarch', 1, 'КРУТЫЕ КРОССОВКИ ЗА ЛЯМ ДВЕСТИ ', 1, 1, 12.00, 1, 2, 10.00, 'photo_2026-05-26_00-11-35.jpg');
INSERT INTO `products` (`id`, `article`, `title`, `category_id`, `description`, `manufacture_id`, `suppiler_id`, `price`, `unit_id`, `quantity`, `discount`, `image_path`) VALUES (4, '0', 'fffff', 1, '', 1, 2, 4444.00, 1, 111, 20.00, 'img.png');
INSERT INTO `products` (`id`, `article`, `title`, `category_id`, `description`, `manufacture_id`, `suppiler_id`, `price`, `unit_id`, `quantity`, `discount`, `image_path`) VALUES (5, '23', 'ыва', 1, 'ыва', 1, 1, 123.00, 1, 123, 10.00, 'None');

-- Data for table `orders`
INSERT INTO `orders` (`id`, `product_id`, `status_id`, `pickup_point_id`, `order_date`, `delivery_date`, `user_id`) VALUES (1, 1, 2, 2, '2026-05-27', '2026-05-27', 2);
INSERT INTO `orders` (`id`, `product_id`, `status_id`, `pickup_point_id`, `order_date`, `delivery_date`, `user_id`) VALUES (2, 3, 1, 1, '2026-05-27', '2026-05-27', 2);
INSERT INTO `orders` (`id`, `product_id`, `status_id`, `pickup_point_id`, `order_date`, `delivery_date`, `user_id`) VALUES (3, 3, 2, 1, '2026-05-27', '2026-05-27', 2);
INSERT INTO `orders` (`id`, `product_id`, `status_id`, `pickup_point_id`, `order_date`, `delivery_date`, `user_id`) VALUES (4, 1, 1, 1, '2026-04-30', '2026-05-27', 2);
INSERT INTO `orders` (`id`, `product_id`, `status_id`, `pickup_point_id`, `order_date`, `delivery_date`, `user_id`) VALUES (5, 3, 1, 1, '2026-05-27', '2026-05-27', 2);

SET FOREIGN_KEY_CHECKS = 1;
COMMIT;
