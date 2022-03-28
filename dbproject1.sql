set search_path to '20290168_Project1';

--query 1
select orderid, totalprice, totalwithdiscountprice
from (select order_id as orderid,unit_price * quantity as totalprice,
	  unit_price * quantity * (1-discount) as totalwithdiscountprice,
      	  row_number()over(order by unit_price * quantity * (1-discount) desc, order_id asc)
	  from order_details details) as sub_q
where row_number < 11;



--query 2
select shippeddate, order_id, sum(totalprice) as totalprice, extract(year from shippeddate) as year
from (select o.shipped_date as shippeddate,
	  od.order_id as order_id, od.unit_price * od.quantity as totalprice, 
	 	extract(year from o.shipped_date) as year
	 from order_details od, orders o
	 where o.order_id = od.order_id) as sub_q
	 group by order_id, shippeddate
	 having shippeddate between '1997-12-30' and '1998-1-5' or 
	 shippeddate is null and sum(totalprice) > 4000
	 order by shippeddate asc, order_id asc;
--query 3
select  category_name, cats.category_id, 
	prod.product_name, prod.product_id, 
	prod.unit_price, prod.units_in_stock,  
	prod.units_on_order, prod.reorder_level,
	prod.discontinued
from categories cats, products prod
where prod.discontinued = '0' and prod.reorder_level > 20
	and prod.units_on_order = 0 and prod.category_id = cats.category_id 
order by product_name;

--query 4
select ship_name, ship_country, customers.customer_id, customers.company_name,
	 first_name || ' ' || last_name AS salesperson, shippers.phone, products.product_id,
	product_name, freight
from	orders, customers, employees, order_details, products, shippers
where freight > 70 and 
order_details.order_id = orders.order_id and 
order_details.product_id = products.product_id and
orders.employee_id = employees.employee_id and
orders.ship_country	 = customers.country and
orders.customer_id = customers.customer_id and
shippers.shipper_id = orders.ship_via and 
ship_country like '%y' and customers.customer_id like 'M%'
order by ship_name asc, ship_country desc, customer_id asc, salesperson asc, freight asc, product_id asc;
--query 5
SELECT 
    p.product_id, c.customer_id, extract(year from o.order_date) as year,
	SUM(CASE WHEN extract( year from o.order_date )=1999 THEN ((1 - discount) * quantity * od.unit_price) ELSE 0 END) AS "1999",
	SUM(CASE WHEN extract( year from o.order_date )=1998 THEN ((1 - discount) * quantity * od.unit_price) ELSE 0 END) AS "1998",
	SUM(CASE WHEN extract( year from o.order_date )=1997 THEN ((1 - discount) * quantity * od.unit_price) ELSE 0 END) AS "1997",
    SUM(CASE WHEN extract( year from o.order_date )=1996 THEN ((1 - discount) * quantity * od.unit_price) ELSE 0 END) AS "1996"
FROM products p, order_details od, orders o, customers c
where od.order_id = o.order_id 
group by od.product_id, p.product_id, product_name, c.customer_id, o.customer_id, year
having od.product_id = p.product_id and p.product_id < 5 and
	c.customer_id = o.customer_id and c.customer_id like 'E%'
	order by year asc, p.product_id asc;

--query 6
select 'Customers' as tablename, city, company_name, contact_name
from 
customers
where contact_name like '%w%'
union
select 'Suppliers' as tablename, city, company_name, contact_name
from 
suppliers
where contact_name like '%g%'
order by contact_name asc;

--query 7
select products_name, unit_price 
from(
		 select product_name as products_name, unit_price, row_number() over(order by unit_price asc)
		 from products ) top
where row_number < 6 
union
select products_name, unit_price 
from(
		 select product_name as products_name, unit_price, row_number() over(order by unit_price desc)
		 from products) top
where row_number < 6
order by unit_price desc;
   
--query 8
select shippedyear, 
		category_name, sum(categorysales)
		from (select sum(round(cast((quantity * order_details.unit_price * (1 - discount)) as numeric) , 2))
		as categorysales, extract(year from shipped_date) as shippedyear, categories.category_name
from order_details 
join products on order_details.product_id = products.product_id
join categories on categories.category_id = products.category_id
join orders on orders.order_id = order_details.order_id
where 	
	shipped_date > '1997-6-1' and shipped_date is not null
group by categories.category_name, shippedyear) subq
group by shippedyear, category_name
		order by shippedyear;

		
		

