-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: hospitales
-- ------------------------------------------------------
-- Server version	9.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `usuario_id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `contrasena` varchar(100) NOT NULL,
  `rol_id` int NOT NULL,
  `estado` enum('activo','inactivo') NOT NULL DEFAULT 'activo',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`usuario_id`),
  UNIQUE KEY `email` (`email`),
  KEY `rol_id` (`rol_id`),
  KEY `idx_usuario_email` (`email`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`rol_id`) REFERENCES `roles` (`rol_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'juan perez','juan.perez@mail.com','juanperez123',1,'activo','2025-05-19 06:48:01',1),(2,'ana lopez','ana.lopez@mail.com','analopez123',1,'activo','2025-05-19 06:48:01',1),(3,'carlos ruiz','carlos.ruiz@mail.com','carlosruiz123',2,'activo','2025-05-19 06:48:01',1),(4,'maria gomez','maria.gomez@mail.com','mariagomez123',2,'activo','2025-05-19 06:48:01',1),(5,'pedro martinez','pedro.martinez@mail.com','pedromartinez123',3,'activo','2025-05-19 06:48:01',1),(6,'luisa fernandez','luisa.fernandez@mail.com','luisafernandez123',1,'activo','2025-05-19 06:48:01',1),(7,'jose sanchez','jose.sanchez@mail.com','josesanchez123',2,'activo','2025-05-19 06:48:01',1),(8,'sofia ramirez','sofia.ramirez@mail.com','sofiaramirez123',1,'activo','2025-05-19 06:48:01',1),(9,'jorge torres','jorge.torres@mail.com','jorgetorres123',3,'activo','2025-05-19 06:48:01',1),(10,'carla diaz','carla.diaz@mail.com','carladiaz123',1,'activo','2025-05-19 06:48:01',1),(11,'luis herrera','luis.herrera@mail.com','luisherrera123',1,'activo','2025-05-19 06:48:01',1),(12,'elena morales','elena.morales@mail.com','elenamorales123',2,'activo','2025-05-19 06:48:01',1),(13,'mario castillo','mario.castillo@mail.com','mariocastillo123',4,'activo','2025-05-19 06:48:01',1),(14,'ana ruiz','ana.ruiz@mail.com','anaruiz123',1,'activo','2025-05-19 06:48:01',1),(15,'pablo ortega','pablo.ortega@mail.com','pabloortega123',5,'activo','2025-05-19 06:48:01',1),(17,'Daniela','daniela.camargo@alumnos.udg.mx','123456',3,'activo','2025-05-20 06:45:11',1);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-20 23:36:48
