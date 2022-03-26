import psycopg2

# Update this part according to your own database!!!
connection = psycopg2.connect(database="20290168", user="postgres", password="pass", host="127.0.0.1",
                              port="5432")

cursor = connection.cursor()

# This part is given as an example for the query of the first question.
# For other questions, please add the necessary code pieces to the specified places!!!

# Question-1
print(str('Question-1'))
cursor.execute(""" set search_path to '20290168_Project1';--query 1
select orderid, totalprice, totalwithdiscountprice
from (select order_id as orderid,unit_price * quantity as totalprice,
	  unit_price * quantity * (1-discount) as totalwithdiscountprice
	  from order_details details) as sub_q
order by totalwithdiscountprice desc, orderid asc limit 10;
""")

rows = cursor.fetchall()
print('ORDERID\t TotalPrice\t\t\t\t TotalwithDiscountPrice')
for row in rows:
    print(str(row[0]).ljust(5) + " \t " + str(row[1]).ljust(20) + " \t " + str(row[2]).ljust(5))

# Question-2
print(str('Question-2'))
cursor.execute("""--query 2
select shippeddate, order_id, sum(totalprice) as totalprice, extract(year from shippeddate) as year
from (select o.shipped_date as shippeddate,
	  od.order_id as order_id, od.unit_price * od.quantity as totalprice, 
	 	extract(year from o.shipped_date) as year
	 from order_details od, orders o
	 where o.order_id = od.order_id) as sub_q
	 group by order_id, shippeddate
	 having shippeddate between '1997-12-30' and '1998-1-5' or 
	 shippeddate is null and sum(totalprice) > 4000
	 order by shippeddate asc, order_id asc;""")

rows = cursor.fetchall()
print('shippeddate\t order_id\t totalprice\t\t\t\t year')
for row in rows:
    print(str(row[0]).ljust(10) + " \t " + str(row[1]).ljust(7) + " \t " + str(row[2]).ljust(20) + " \t " + str(row[3]).ljust(5))

# Write your piece of code as in Question-1

# Question-3
print(str('Question-3'))
cursor.execute("""select  category_name, cats.category_id, 
    prod.product_name, prod.product_id, 
    prod.unit_price, prod.units_in_stock,  
    prod.units_on_order, prod.reorder_level,
    prod.discontinued
from categories cats, products prod
where prod.discontinued = '0' and prod.reorder_level > 20
    and prod.units_on_order = 0 and prod.category_id = cats.category_id 
order by product_name;""")
rows = cursor.fetchall()
print(
    'category_name\t category_id\t product_name\t\t\t\t\t\t product_id\t unit_price\t units_in_stock\t '
    'units_on_order\t reorder_level\t discontinued')
for row in rows:
    print(str(row[0]).ljust(13) + " \t "  # catname
          + str(row[1]).ljust(13) + " \t "  # catid
          + str(row[2]).ljust(28) + " \t\t "  # prodname
          + str(row[3]).ljust(7) + " \t "  # prodid
          + str(row[4]).ljust(7) + " \t "  # unitprice
          + str(row[5]).ljust(12) + " \t "  # uis
          + str(row[6]).ljust(10) + " \t "  # uoo
          + str(row[7]).ljust(10) + " \t "  # reoderlvl
          + str(row[8]).ljust(5))  # discont.

# Question-4
print(str('Question-4'))
cursor.execute("""--query 4
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
order by ship_name asc, ship_country desc, customer_id asc, salesperson asc, freight asc, product_id asc;""")
rows = cursor.fetchall()
print(
    'ship_name\t\t\t\t\t\t ship_country\t customer_id\t company_name\t\t\t\t\t salesperson\t\t phone\t\t\t\t '
    'product_id\t\t product_name\t\t\t\t\t freight')
for row in rows:
    print(str(row[0]).ljust(30) + " \t "  # shipname
          + str(row[1]).ljust(10) + " \t "  # shipcountry
          + str(row[2]).ljust(7) + " \t\t "  # customerid
          + str(row[3]).ljust(27) + " \t "  # company name
          + str(row[4]).ljust(15) + " \t "  # sales person
          + str(row[5]).ljust(10) + " \t "  # phone
          + str(row[6]).ljust(10) + " \t "  # proudct id
          + str(row[7]).ljust(28) + " \t "  # product name
          + str(row[8]))  # freight.

# Write your piece of code as in Question-1

# Question-5
print(str('Question-5'))

cursor.execute("""SELECT p.product_id, c.customer_id, extract(year from o.order_date) as year, SUM(CASE WHEN extract( 
year from o.order_date )=1999 THEN ((1 - discount) * quantity * od.unit_price) ELSE 0 END) AS "1999", SUM(CASE WHEN 
extract( year from o.order_date )=1998 THEN ((1 - discount) * quantity * od.unit_price) ELSE 0 END) AS "1998", 
SUM(CASE WHEN extract( year from o.order_date )=1997 THEN ((1 - discount) * quantity * od.unit_price) ELSE 0 END) AS 
"1997", SUM(CASE WHEN extract( year from o.order_date )=1996 THEN ((1 - discount) * quantity * od.unit_price) ELSE 0 
END) AS "1996" FROM products p, order_details od, orders o, customers c where od.order_id = o.order_id group by 
od.product_id, p.product_id, product_name, c.customer_id, o.customer_id, year having od.product_id = p.product_id and 
p.product_id < 5 and c.customer_id = o.customer_id and c.customer_id like 'E%' order by year asc, p.product_id asc;""")
rows = cursor.fetchall()
print('prdouct_id\t customer_id\t year\t Year 1999\t Year 1998\t Year 1997\t\t\t\t Year 1996\t')
for row in rows:
    print(str(row[0]).ljust(10) + " \t "  # pid
          + str(row[1]).ljust(10) + " \t "  # cid
          + str(row[2]).ljust(2) + " \t "  # year
          + str(row[3]).ljust(8) + " \t "  # 99
          + str(row[4]).ljust(8) + " \t "  # 98
          + str(row[5]).ljust(20) + " \t "  # 97
          + str(row[6]).ljust(10) + " \t ")  # 96

# Question-6
print(str('Question-6'))

cursor.execute("""select 'Customers' as tablename, city, company_name, contact_name
from 
customers
where contact_name like '%w%'
union
select 'Suppliers' as tablename, city, company_name, contact_name
from 
suppliers
where contact_name like '%g%'
order by contact_name asc;
""")
rows = cursor.fetchall()
print('tablename\t city\t\t\t company_name\t\t\t\t contact_name\t')
for row in rows:
    print(str(row[0]).ljust(10) + " \t "  # tablename
          + str(row[1]).ljust(10) + " \t "  # city
          + str(row[2]).ljust(24) + " \t "  # companyname
          + str(row[3]).ljust(8) + " \t ")  # contactname

# Write your piece of code as in Question-1

# Question-7
print(str('Question-7'))

cursor.execute("""select products_name, unit_price 
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
order by unit_price desc;""")
rows = cursor.fetchall()
print('products_name\t\t\t\t unit_price\t')
for row in rows:
    print(str(row[0]).ljust(24) + " \t "  # products_name
          + str(row[1]).ljust(10) + " \t ")  # unit_price
# Write your piece of code as in Question-1

# Question-8
print(str('Question-8'))
cursor.execute("""select shippedyear, 
		category_name,
		sum(categorysales)
		from (select sum(round(cast((quantity * order_details.unit_price * (1 - discount)) as numeric) , 2))
		as categorysales, extract(year from shipped_date) as shippedyear,
			  categories.category_name
from order_details 
join products on order_details.product_id = products.product_id
join categories on categories.category_id = products.category_id
join orders on orders.order_id = order_details.order_id

where 	
	shipped_date > '1997-6-1' and shipped_date is not null
group by categories.category_name, shippedyear) subq
group by shippedyear, category_name
		order by shippedyear;

		""")
rows = cursor.fetchall()
print('shippedyear\t caregory_name\t\t sum')
for row in rows:
    print(str(row[0]).ljust(10) + " \t "  # tablename
          + str(row[1]).ljust(14) + " \t "  # city
          + str(row[2]) + " \t ")  # companyname
# Write your piece of code as in Question-1

connection.commit()
connection.close()
