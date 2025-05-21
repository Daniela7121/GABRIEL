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
-- Table structure for table `resultados_laboratorios`
--

DROP TABLE IF EXISTS `resultados_laboratorios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resultados_laboratorios` (
  `resultado_id` int NOT NULL AUTO_INCREMENT,
  `paciente_id` int NOT NULL,
  `laboratorio_id` int NOT NULL,
  `fecha` date NOT NULL,
  `resultado` text NOT NULL,
  PRIMARY KEY (`resultado_id`),
  KEY `paciente_id` (`paciente_id`),
  KEY `laboratorio_id` (`laboratorio_id`),
  CONSTRAINT `resultados_laboratorios_ibfk_1` FOREIGN KEY (`paciente_id`) REFERENCES `usuarios` (`usuario_id`),
  CONSTRAINT `resultados_laboratorios_ibfk_2` FOREIGN KEY (`laboratorio_id`) REFERENCES `laboratorios` (`laboratorio_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resultados_laboratorios`
--

LOCK TABLES `resultados_laboratorios` WRITE;
/*!40000 ALTER TABLE `resultados_laboratorios` DISABLE KEYS */;
INSERT INTO `resultados_laboratorios` VALUES (1,5,1,'2024-01-10','Resultado de sangre normal'),(2,9,2,'2024-01-11','Glucosa alta'),(3,5,3,'2024-01-12','Colesterol alto'),(4,4,4,'2024-01-13','Hepatitis negativo'),(5,7,5,'2024-01-14','Análisis de orina normal'),(6,3,6,'2024-01-15','Hemograma completo'),(7,9,7,'2024-01-16','Perfil tiroideo normal'),(8,15,8,'2024-01-17','Prueba de alergias negativa'),(9,10,9,'2024-01-18','Examen de visión normal'),(10,14,10,'2024-01-19','Electrocardiograma normal'),(11,8,11,'2024-01-20','Prueba COVID negativa'),(12,13,12,'2024-01-21','Radiografía de tórax normal'),(13,11,13,'2024-01-22','Prueba de función hepática normal'),(14,2,14,'2024-01-23','Examen de orina normal'),(15,1,15,'2024-01-24','Resultado de sangre normal');
/*!40000 ALTER TABLE `resultados_laboratorios` ENABLE KEYS */;
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
