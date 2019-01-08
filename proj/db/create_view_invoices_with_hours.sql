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
  and i.id not in (select id from invoices_with_non_prod_hours)
