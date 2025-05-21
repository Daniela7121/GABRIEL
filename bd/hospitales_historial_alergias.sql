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
-- Table structure for table `historial_alergias`
--

DROP TABLE IF EXISTS `historial_alergias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historial_alergias` (
  `alergia_id` int NOT NULL AUTO_INCREMENT,
  `paciente_id` int NOT NULL,
  `alergia` varchar(100) NOT NULL,
  `descripcion` text,
  `fecha_registro` date NOT NULL,
  PRIMARY KEY (`alergia_id`),
  KEY `paciente_id` (`paciente_id`),
  CONSTRAINT `historial_alergias_ibfk_1` FOREIGN KEY (`paciente_id`) REFERENCES `usuarios` (`usuario_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_alergias`
--

LOCK TABLES `historial_alergias` WRITE;
/*!40000 ALTER TABLE `historial_alergias` DISABLE KEYS */;
INSERT INTO `historial_alergias` VALUES (1,5,'Polvo','Reacción leve','2023-10-01'),(2,9,'Penicilina','Anafilaxia','2023-10-02'),(3,5,'Frutos secos','Hinchazón de labios','2023-10-03'),(4,4,'Mariscos','Urticaria','2023-10-04'),(5,7,'Polen','Congestión nasal','2023-10-05'),(6,3,'Ácaros','Estornudos frecuentes','2023-10-06'),(7,9,'Lácteos','Dolor abdominal','2023-10-07'),(8,15,'Gatos','Picazón en piel','2023-10-08'),(9,10,'Polvo','Irritación ocular','2023-10-09'),(10,14,'Moho','Dificultad para respirar','2023-10-10'),(11,8,'Cacahuate','Reacción severa','2023-10-11'),(12,13,'Abejas','Shock anafiláctico','2023-10-12'),(13,11,'Polen','Tos crónica','2023-10-13'),(14,2,'Penicilina','Erupción cutánea','2023-10-14'),(15,1,'Frutos secos','Hinchazón facial','2023-10-15');
/*!40000 ALTER TABLE `historial_alergias` ENABLE KEYS */;
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
