CREATE TABLE `users` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`username` varchar(80) NOT NULL UNIQUE,
	`password` varchar(255) NOT NULL,
	`email` varchar(120) NOT NULL UNIQUE,
	PRIMARY KEY (`id`)
);

CREATE TABLE `entity` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`name` varchar(120) NOT NULL UNIQUE,
	`decription` TEXT,
	PRIMARY KEY (`id`)
);

CREATE TABLE `category` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`parent_id` INT NOT NULL,
	`entity_id` INT NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `account` (
	`id` int NOT NULL AUTO_INCREMENT,
	`entity_id` int NOT NULL,
	`user_id` int NOT NULL,
	`balancce` numeric NOT NULL,
	`currency` numeric NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `budget` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`categoty_id` INT NOT NULL,
	`limit` numeric NOT NULL,
	`start_date` DATETIME NOT NULL,
	`end_date` DATETIME NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `operation` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`category_id` INT NOT NULL,
	`entity_id` INT NOT NULL,
	`account_id` INT NOT NULL,
	`date` DATE NOT NULL,
	`amount` numeric NOT NULL,
	`currency` numeric NOT NULL,
	PRIMARY KEY (`id`)
);

ALTER TABLE `category` ADD CONSTRAINT `category_fk0` FOREIGN KEY (`entity_id`) REFERENCES `entity`(`id`);

ALTER TABLE `account` ADD CONSTRAINT `account_fk0` FOREIGN KEY (`entity_id`) REFERENCES `entity`(`id`);

ALTER TABLE `account` ADD CONSTRAINT `account_fk1` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`);

ALTER TABLE `budget` ADD CONSTRAINT `budget_fk0` FOREIGN KEY (`categoty_id`) REFERENCES `category`(`id`);

ALTER TABLE `operation` ADD CONSTRAINT `operation_fk0` FOREIGN KEY (`category_id`) REFERENCES `category`(`id`);

ALTER TABLE `operation` ADD CONSTRAINT `operation_fk1` FOREIGN KEY (`entity_id`) REFERENCES `entity`(`id`);

ALTER TABLE `operation` ADD CONSTRAINT `operation_fk2` FOREIGN KEY (`account_id`) REFERENCES `account`(`id`);
