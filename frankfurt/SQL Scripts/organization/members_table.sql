CREATE TABLE IF NOT EXISTS `members` (
  `PersonID` INT(11) NOT NULL,
  `Role` INT(11) NULL DEFAULT '4',
  `Name` VARCHAR(255) NOT NULL,
  `Surname` VARCHAR(255) NOT NULL,
  `Username` VARCHAR(255) NOT NULL,
  `Password` VARCHAR(255) NOT NULL,
  `Email` VARCHAR(50) NOT NULL,
  `Department` VARCHAR(255) NULL DEFAULT NULL,
  `ProfilePic` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`PersonID`),
  UNIQUE INDEX `Name` (`Name` ASC, `Surname` ASC, `Username` ASC),
  UNIQUE INDEX `idx_members_Username` (`Username` ASC),
  INDEX `members_ibfk_1` (`Role` ASC),
  INDEX `username` (`Username` ASC),
  CONSTRAINT `members_ibfk_1`
    FOREIGN KEY (`Role`)
    REFERENCES `istanbul_sehir_university`.`roles` (`roleID`)
    ON DELETE SET NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8