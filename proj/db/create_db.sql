CREATE TABLE "customers" ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, `name` TEXT NOT NULL )

CREATE TABLE "works" ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, `date` TEXT NOT NULL, `begin` TEXT NOT NULL, `end` TEXT NOT NULL, `minutes` INTEGER, `prod` INTEGER NOT NULL DEFAULT 1, `add` REAL, `note` TEXT, `registry` TEXT NOT NULL, `price` REAL NOT NULL, `km` INTEGER NOT NULL DEFAULT 0, `customer_id` INTEGER NOT NULL, FOREIGN KEY(`customer_id`) REFERENCES `customers`(`id`) )

CREATE TABLE `payments` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, `paid_at` INTEGER, `gross` REAL, `tax` REAL, `net` REAL NOT NULL, `note` TEXT, `customer_id` INTEGER, `invoice_id` INTEGER )

CREATE TABLE "invoices" ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, `customer_id` INTEGER NOT NULL, `emitted_at` TEXT NOT NULL, `gross` REAL NOT NULL, `tax` REAL, `net` REAL, `from_dt` TEXT NOT NULL, `to_dt` TEXT NOT NULL, `prog` INTEGER NOT NULL, `reason` TEXT NOT NULL, `note` TEXT )
