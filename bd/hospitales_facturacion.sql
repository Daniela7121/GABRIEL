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
-- Table structure for table `facturacion`
--

DROP TABLE IF EXISTS `facturacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facturacion` (
  `factura_id` int NOT NULL AUTO_INCREMENT,
  `paciente_id` int NOT NULL,
  `fecha` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `total` decimal(10,2) NOT NULL,
  `estado_pago` enum('pendiente','pagado','cancelado') NOT NULL DEFAULT 'pendiente',
  `conceptos` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`factura_id`),
  KEY `idx_factura_paciente` (`paciente_id`),
  CONSTRAINT `facturacion_ibfk_1` FOREIGN KEY (`paciente_id`) REFERENCES `usuarios` (`usuario_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facturacion`
--

LOCK TABLES `facturacion` WRITE;
/*!40000 ALTER TABLE `facturacion` DISABLE KEYS */;
INSERT INTO `facturacion` VALUES (1,5,'2024-01-10 15:00:00',1500.00,'pagado',NULL),(2,9,'2024-01-11 16:00:00',2000.00,'pendiente',NULL),(3,5,'2024-01-12 17:00:00',1800.00,'pagado',NULL),(4,4,'2024-01-13 18:00:00',1200.00,'cancelado',NULL),(5,7,'2024-01-14 19:00:00',1600.00,'pagado',NULL),(6,3,'2024-01-15 20:00:00',1900.00,'pendiente',NULL),(7,9,'2024-01-16 21:00:00',1750.00,'pagado',NULL),(8,15,'2024-01-17 22:00:00',2200.00,'pagado',NULL),(9,10,'2024-01-18 23:00:00',1300.00,'pendiente',NULL),(10,14,'2024-01-20 00:00:00',2100.00,'pagado',NULL),(11,8,'2024-01-21 01:00:00',1050.00,'pagado','[(\'antibiotico\', \'800\'), (\'consulta general\', \'250\')]'),(12,13,'2024-01-22 02:00:00',1250.00,'cancelado',NULL),(13,11,'2024-01-23 03:00:00',1950.00,'pagado',NULL),(14,2,'2024-01-24 04:00:00',1800.00,'pagado',NULL),(15,1,'2024-01-25 05:00:00',1400.00,'pendiente',NULL);
/*!40000 ALTER TABLE `facturacion` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-20 23:36:46
