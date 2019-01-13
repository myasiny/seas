CREATE TABLE IF NOT EXISTS `last_activities` (
  `Username` VARCHAR(255) NOT NULL,
  `Api_Endpoint` VARCHAR(50) NOT NULL,
  `Time` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `IP` VARCHAR(15) NOT NULL,
  `Activity_ID` INT(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`Activity_ID`),
  INDEX `username` (`Username` ASC),
  CONSTRAINT `last_activities_ibfk_1`
    FOREIGN KEY (`Username`)
    REFERENCES `istanbul_sehir_university`.`members` (`Username`))
ENGINE = InnoDB
AUTO_INCREMENT = 179
DEFAULT CHARACTER SET = utf8