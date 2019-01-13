CREATE TABLE IF NOT EXISTS `answers` (
  `answerID` INT(11) NOT NULL AUTO_INCREMENT,
  `questionID` INT(11) NULL DEFAULT NULL,
  `studentID` INT(11) NULL DEFAULT NULL,
  `answer` JSON NULL DEFAULT NULL,
  `grade` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`answerID`),
  UNIQUE INDEX `questionID` (`questionID` ASC, `studentID` ASC),
  INDEX `answers_ibfk_2` (`studentID` ASC),
  CONSTRAINT `answers_ibfk_1`
    FOREIGN KEY (`questionID`)
    REFERENCES `istanbul_sehir_university`.`questions` (`QuestionID`)
    ON DELETE CASCADE,
  CONSTRAINT `answers_ibfk_2`
    FOREIGN KEY (`studentID`)
    REFERENCES `istanbul_sehir_university`.`members` (`PersonID`)
    ON DELETE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8