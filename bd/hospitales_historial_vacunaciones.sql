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
-- Table structure for table `historial_vacunaciones`
--

DROP TABLE IF EXISTS `historial_vacunaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historial_vacunaciones` (
  `vacunacion_id` int NOT NULL AUTO_INCREMENT,
  `paciente_id` int NOT NULL,
  `vacuna` varchar(100) NOT NULL,
  `fecha` date NOT NULL,
  `doctor_id` int DEFAULT NULL,
  `dosis` varchar(255) DEFAULT NULL,
  `observaciones` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`vacunacion_id`),
  KEY `paciente_id` (`paciente_id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `historial_vacunaciones_ibfk_1` FOREIGN KEY (`paciente_id`) REFERENCES `usuarios` (`usuario_id`),
  CONSTRAINT `historial_vacunaciones_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `usuarios` (`usuario_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_vacunaciones`
--

LOCK TABLES `historial_vacunaciones` WRITE;
/*!40000 ALTER TABLE `historial_vacunaciones` DISABLE KEYS */;
INSERT INTO `historial_vacunaciones` VALUES (1,5,'Influenza','2023-11-01',3,NULL,NULL),(2,9,'Hepatitis B','2023-11-02',4,NULL,NULL),(3,5,'COVID-19','2023-11-03',3,NULL,NULL),(4,4,'Tétanos','2023-11-04',7,NULL,NULL),(5,7,'Influenza','2023-11-05',8,NULL,NULL),(6,3,'Sarampión','2023-11-06',2,NULL,NULL),(7,9,'Varicela','2023-11-07',4,NULL,NULL),(8,15,'COVID-19','2023-11-08',3,NULL,NULL),(9,10,'Hepatitis B','2023-11-09',4,NULL,NULL),(10,14,'Influenza','2023-11-10',2,NULL,NULL),(11,8,'Tétanos','2023-11-11',7,NULL,NULL),(12,13,'Sarampión','2023-11-12',8,NULL,NULL),(13,11,'Varicela','2023-11-13',3,NULL,NULL),(14,2,'Influenza','2023-11-14',2,NULL,NULL),(15,1,'COVID-19','2023-11-15',4,NULL,NULL);
/*!40000 ALTER TABLE `historial_vacunaciones` ENABLE KEYS */;
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
