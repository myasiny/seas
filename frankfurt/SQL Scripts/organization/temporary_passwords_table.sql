CREATE TABLE IF NOT EXISTS `temporary_passwords` (
  `UserID` INT(11) NOT NULL,
  `Password` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`UserID`),
  CONSTRAINT `temporary_passwords_ibfk_1`
    FOREIGN KEY (`UserID`)
    REFERENCES `istanbul_sehir_university`.`members` (`PersonID`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8