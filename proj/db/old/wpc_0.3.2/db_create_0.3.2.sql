CREATE TABLE `customers` ( 
	`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
	`name` TEXT NOT NULL UNIQUE
);

CREATE TABLE `clients` (
	`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
	`name` TEXT NOT NULL,
	`note` TEXT NULL,
	`customer_id` INTEGER NOT NULL, 
	FOREIGN KEY(`customer_id`) REFERENCES `customers`(`id`) 
);

CREATE TABLE `works` (
	`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`date` TEXT NOT NULL,
	`from_dt` TEXT NOT NULL,
	`to_dt` TEXT NOT NULL,
	`minutes` INTEGER,
	`prod` INTEGER NOT NULL DEFAULT 1,
	`add` REAL, 
	`note` TEXT, 
	`registry` TEXT NOT NULL,
	`price` REAL NOT NULL, 
	`km` INTEGER NOT NULL DEFAULT 0, 
	`customer_id` INTEGER NOT NULL, 
	`client_id` INTEGER NULL, 
	FOREIGN KEY(`customer_id`) REFERENCES `customers`(`id`),
	FOREIGN KEY(`client_id`) REFERENCES `clients`(`id`) 
);

CREATE TABLE `payments` ( 
	`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`paid_at` TEXT NOT NULL, 
	`gross` REAL, 
	`tax` REAL, 
	`net` REAL NOT NULL, 
	`note` TEXT, 
	`customer_id` INTEGER NOT NULL, 
	`invoice_id` INTEGER,
	FOREIGN KEY(`customer_id`) REFERENCES `customers`(`id`),
	FOREIGN KEY(`invoice_id`) REFERENCES `invoices`(`id`) 
);

CREATE TABLE `invoices` ( 
	`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
	`emitted_at` TEXT NOT NULL, 
	`from_dt` TEXT NOT NULL, 
	`to_dt` TEXT NOT NULL, 
	`gross` REAL NOT NULL, 
	`tax` REAL, 
	`net` REAL, 
	`prog` INTEGER, 
	`reason` TEXT NOT NULL, 
	`note` TEXT,
	`customer_id` INTEGER NOT NULL,
	FOREIGN KEY(`customer_id`) REFERENCES `customers`(`id`)
);
