CREATE TABLE IF NOT EXISTS `questions` (
  `QuestionID` INT(11) NOT NULL AUTO_INCREMENT,
  `ExamID` INT(11) NULL DEFAULT NULL,
  `info` JSON NULL DEFAULT NULL,
  PRIMARY KEY (`QuestionID`),
  INDEX `questions_ibfk_1` (`ExamID` ASC),
  CONSTRAINT `questions_ibfk_1`
    FOREIGN KEY (`ExamID`)
    REFERENCES `istanbul_sehir_university`.`exams` (`ExamID`)
    ON DELETE SET NULL)
ENGINE = InnoDB
AUTO_INCREMENT = 161
DEFAULT CHARACTER SET = utf8