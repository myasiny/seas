CREATE TABLE IF NOT EXISTS `exams` (
  `ExamID` INT(11) NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(255) NOT NULL,
  `CourseID` INT(11) NULL DEFAULT NULL,
  `Time` VARCHAR(50) NOT NULL,
  `Duration` INT(11) NOT NULL,
  `Status` VARCHAR(20) NOT NULL DEFAULT 'draft',
  `Timezone` VARCHAR(10) NOT NULL DEFAULT '+03:00',
  PRIMARY KEY (`ExamID`),
  UNIQUE INDEX `Name` (`Name` ASC),
  UNIQUE INDEX `Name_2` (`Name` ASC, `Time` ASC),
  INDEX `exams_ibfk_1` (`CourseID` ASC),
  CONSTRAINT `exams_ibfk_1`
    FOREIGN KEY (`CourseID`)
    REFERENCES `istanbul_sehir_university`.`courses` (`CourseID`)
    ON DELETE SET NULL)
ENGINE = InnoDB
AUTO_INCREMENT = 344
DEFAULT CHARACTER SET = utf8