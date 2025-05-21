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
-- Table structure for table `medicamentos`
--

DROP TABLE IF EXISTS `medicamentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medicamentos` (
  `medicamento_id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text,
  `stock` int DEFAULT '0',
  `precio` decimal(10,2) NOT NULL,
  `farmacia_id` int DEFAULT NULL,
  PRIMARY KEY (`medicamento_id`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `farmacia_id` (`farmacia_id`),
  CONSTRAINT `medicamentos_ibfk_1` FOREIGN KEY (`farmacia_id`) REFERENCES `farmacias` (`farmacia_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicamentos`
--

LOCK TABLES `medicamentos` WRITE;
/*!40000 ALTER TABLE `medicamentos` DISABLE KEYS */;
INSERT INTO `medicamentos` VALUES (1,'Paracetamol','Analgésico y antipirético',100,25.50,1),(2,'Ibuprofeno','Antiinflamatorio no esteroideo',50,30.00,1),(3,'Amoxicilina','Antibiótico de amplio espectro',80,45.00,2),(4,'Metformina','Control de glucosa en diabetes',60,35.00,2),(5,'Loratadina','Antihistamínico para alergias',40,28.00,3),(6,'Omeprazol','Inhibidor de bomba de protones',70,40.00,3),(7,'Simvastatina','Reduce colesterol',90,50.00,4),(8,'Aspirina','Antiplaquetario y analgésico',120,20.00,4),(9,'Clorfeniramina','Antihistamínico para alergias',30,22.00,5),(10,'Diclofenaco','Antiinflamatorio',55,33.00,5),(11,'Ranitidina','Antiácido y antiulceroso',75,27.00,6),(12,'Prednisona','Corticosteroide',65,60.00,6),(13,'Cetirizina','Antihistamínico',85,29.00,7),(14,'Metoclopramida','Antiemético',45,31.00,7),(15,'Clonazepam','Ansiolítico',25,70.00,8);
/*!40000 ALTER TABLE `medicamentos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-20 23:36:47
