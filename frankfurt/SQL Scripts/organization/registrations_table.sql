CREATE TABLE IF NOT EXISTS `registrations` (
  `StudentID` INT(11) NOT NULL,
  `CourseID` INT(11) NOT NULL,
  `RegistrationID` INT(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`RegistrationID`),
  UNIQUE INDEX `StudentID` (`StudentID` ASC, `CourseID` ASC),
  INDEX `registrations_ibfk_1` (`CourseID` ASC),
  CONSTRAINT `registrations_ibfk_1`
    FOREIGN KEY (`CourseID`)
    REFERENCES `istanbul_sehir_university`.`courses` (`CourseID`)
    ON DELETE CASCADE,
  CONSTRAINT `registrations_ibfk_2`
    FOREIGN KEY (`StudentID`)
    REFERENCES `istanbul_sehir_university`.`members` (`PersonID`)
    ON DELETE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 61
DEFAULT CHARACTER SET = utf8