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
