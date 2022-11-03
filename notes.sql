-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema notes
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `notes` ;

-- -----------------------------------------------------
-- Schema notes
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `notes` DEFAULT CHARACTER SET utf8 ;
USE `notes` ;

-- -----------------------------------------------------
-- Table `notes`.`User`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `notes`.`User` ;

CREATE TABLE IF NOT EXISTS `notes`.`User` (
  `idUser` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(25) NOT NULL,
  `email` VARCHAR(35) NOT NULL,
  `firstName` VARCHAR(25) NOT NULL,
  `lastName` VARCHAR(25) NOT NULL,
  `userStatus` ENUM('online', 'offline') NOT NULL,
  PRIMARY KEY (`idUser`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `notes`.`Note`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `notes`.`Note` ;

CREATE TABLE IF NOT EXISTS `notes`.`Note` (
  `idNote` INT NOT NULL AUTO_INCREMENT,
  `ownerId` INT NOT NULL,
  `title` VARCHAR(45) NOT NULL,
  `isPublic` ENUM('true', 'false') NOT NULL,
  `text` VARCHAR(404) NOT NULL,
  `dateOfEditing` DATETIME NOT NULL,
  PRIMARY KEY (`idNote`),
  INDEX `fk_Note_User_idx` (`ownerId` ASC) VISIBLE,
  CONSTRAINT `fk_Note_User`
    FOREIGN KEY (`ownerId`)
    REFERENCES `notes`.`User` (`idUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `notes`.`Stats`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `notes`.`Stats` ;

CREATE TABLE IF NOT EXISTS `notes`.`Stats` (
  `idStats` INT NOT NULL AUTO_INCREMENT,
  `userId` INT NOT NULL,
  `numOfNotes` INT NOT NULL,
  `numOfEditingNotes` INT NOT NULL,
  `dateOfCreating` DATETIME NOT NULL,
  PRIMARY KEY (`idStats`),
  INDEX `fk_Stats_User1_idx` (`userId` ASC) VISIBLE,
  CONSTRAINT `fk_Stats_User1`
    FOREIGN KEY (`userId`)
    REFERENCES `notes`.`User` (`idUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `notes`.`EditNote`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `notes`.`EditNote` ;

CREATE TABLE IF NOT EXISTS `notes`.`EditNote` (
  `idUser` INT NOT NULL,
  `idNote` INT NOT NULL,
  PRIMARY KEY (`idUser`, `idNote`),
  INDEX `fk_User_has_Note_Note1_idx` (`idNote` ASC) VISIBLE,
  INDEX `fk_User_has_Note_User1_idx` (`idUser` ASC) VISIBLE,
  CONSTRAINT `fk_User_has_Note_User1`
    FOREIGN KEY (`idUser`)
    REFERENCES `notes`.`User` (`idUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_User_has_Note_Note1`
    FOREIGN KEY (`idNote`)
    REFERENCES `notes`.`Note` (`idNote`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `notes`.`Tag`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `notes`.`Tag` ;

CREATE TABLE IF NOT EXISTS `notes`.`Tag` (
  `idTag` INT NOT NULL AUTO_INCREMENT,
  `text` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idTag`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `notes`.`Tags`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `notes`.`Tags` ;

CREATE TABLE IF NOT EXISTS `notes`.`Tags` (
  `Note_idNote` INT NOT NULL,
  `Tag_idTag` INT NOT NULL,
  PRIMARY KEY (`Note_idNote`, `Tag_idTag`),
  INDEX `fk_Note_has_Tag_Tag1_idx` (`Tag_idTag` ASC) VISIBLE,
  INDEX `fk_Note_has_Tag_Note1_idx` (`Note_idNote` ASC) VISIBLE,
  CONSTRAINT `fk_Note_has_Tag_Note1`
    FOREIGN KEY (`Note_idNote`)
    REFERENCES `notes`.`Note` (`idNote`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Note_has_Tag_Tag1`
    FOREIGN KEY (`Tag_idTag`)
    REFERENCES `notes`.`Tag` (`idTag`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
