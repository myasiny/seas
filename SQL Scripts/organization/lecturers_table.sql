CREATE TABLE IF NOT EXISTS `lecturers` (
  `LecturerID` INT(11) NOT NULL,
  `CourseID` INT(11) NOT NULL,
  `LeCorID` INT(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`LeCorID`),
  UNIQUE INDEX `LecturerID` (`LecturerID` ASC, `CourseID` ASC),
  INDEX `lecturers_ibfk_1` (`CourseID` ASC),
  CONSTRAINT `lecturers_ibfk_1`
    FOREIGN KEY (`CourseID`)
    REFERENCES `istanbul_sehir_university`.`courses` (`CourseID`)
    ON DELETE CASCADE,
  CONSTRAINT `lecturers_ibfk_2`
    FOREIGN KEY (`LecturerID`)
    REFERENCES `istanbul_sehir_university`.`members` (`PersonID`)
    ON DELETE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 12
DEFAULT CHARACTER SET = utf8