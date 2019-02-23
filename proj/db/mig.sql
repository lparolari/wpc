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
-- invoices with production hours

create view invoices_with_prod_hours (id, emitted_at, gross, tax, net, from_dt, to_dt, note, customer_id, hours, reason, prog) as
select 
	i.id, i.emitted_at, i.gross, i.tax, i.net, i.from_dt, i.to_dt, i.note, i.customer_id, 
	sum(
		round (
			cast ( 
				( julianday(w.end) - julianday(w.begin) ) * 24 as real), 
			2) 
	) as hours,
	i.reason, i.prog
from works w
inner join invoices i on (w.begin >= i.from_dt and w.begin <= i.to_dt)
where w.prod = 1
group by i.id, i.emitted_at, i.gross, i.tax, i.net, i.from_dt, i.to_dt, i.note, i.customer_id, i.reason, i.prog;
-- invoices with non production hours

create view invoices_with_non_prod_hours (id, emitted_at, gross, tax, net, from_dt, to_dt, note, customer_id, hours, reason, prog) as
select 
	i.id, i.emitted_at, i.gross, i.tax, i.net, i.from_dt, i.to_dt, i.note, i.customer_id, 
	sum(
		round (
			cast ( 
				( julianday(w.end) - julianday(w.begin) ) * 24 as real), 
			2) 
	) as hours,
	i.reason, i.prog
from works w
inner join invoices i on (w.begin >= i.from_dt and w.begin <= i.to_dt)
where w.prod = 0
group by i.id, i.emitted_at, i.gross, i.tax, i.net, i.from_dt, i.to_dt, i.note, i.customer_id, i.reason, i.prog;
-- invoices with prod and non prod hours

-- Note that the unions are used  to simulate a full outher join, that
--  it is not supported in SQLite.
-- It works cobining with the inner join invoices that has production and not production hours,
--  than the first union prodvides invoices with production hours only selecting all recoords that are not in the non production table.
--  The second union provides invoices with non production hours, exluding records that are in the production table.

create view invoices_with_hours (
    id, emitted_at, gross, tax, net, from_dt, to_dt, note, customer_id, hours_prod, hours_non_prod, reason, prog) as

select i2.id, i1.emitted_at, i1.gross, i1.tax, i1.net, i1.from_dt, i1.to_dt, i1.note, i1.customer_id, 
	i1.hours,  -- prod hours.
	i2.hours ,  -- non prod hours.
	i1.reason, i1.prog
from invoices_with_prod_hours i1 
inner join invoices_with_non_prod_hours i2 on (i1.id = i2.id)

union

select i.id, i.emitted_at, i.gross, i.tax, i.net, i.from_dt, i.to_dt, i.note, i.customer_id, i.hours, 0, i.reason, i.prog
from invoices_with_prod_hours i
where i.id not in (select id from invoices_with_non_prod_hours)

union

select i.id, i.emitted_at, i.gross, i.tax, i.net, i.from_dt, i.to_dt, i.note, i.customer_id, 0, i.hours, i.reason, i.prog
from invoices_with_non_prod_hours i
where i.id not in (select id from invoices_with_prod_hours)

union

-- invoices without works. (probably a fake invoice)
select i.id, i.emitted_at, i.gross, i.tax, i.net, i.from_dt, i.to_dt, i.note, i.customer_id, 0, 0, i.reason, i.prog
from invoices i
where i.id not in (select id from invoices_with_prod_hours)
  and i.id not in (select id from invoices_with_non_prod_hours);
