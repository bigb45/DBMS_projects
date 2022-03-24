import psycopg2

# Update this part according to your own database!!!
connection = psycopg2.connect(database="20290168", user="postgres", password="pass", host="127.0.0.1",
                              port="5432")

cursor = connection.cursor()

# This part is given as an example for the query of the first question.
# For other questions, please add the necessary code pieces to the specified places!!!

# Question-1
print(str('Question-1'))
cursor.execute("""select orders.order_id, quantity, unit_price from orders, 
               order_details where orders.order_id = order_details.order_id and unit_price > 100;""")

rows = cursor.fetchall()
print('ORDERID\t TotalPrice\t TotalwithDiscountPrice')
for row in rows:
    print(str(row[0]).ljust(5) + " \t " + str(row[1]).ljust(7) + " \t " + str(row[2]).ljust(5))

# Question-2
print(str('Question-2'))
cursor.execute("""select shippeddate, order_id, sum(totalprice) as totalprice
from (select o.shipped_date as shippeddate,
	  od.order_id as order_id, od.unit_price * od.quantity * (1-discount) as totalprice, 
	   	extract(year from o.shipped_date) as year
	 from order_details od, orders o
	 where o.order_id = od.order_id) as sub_q
	 group by order_id, shippeddate
	 having shippeddate between '1997-12-30' and '1998-1-5' or 
	 shippeddate is null and sum(totalprice) > 4000
	 order by shippeddate asc, order_id asc limit 10;""")

rows = cursor.fetchall()
print('shippeddate\t order_id\t totalprice')
for row in rows:
    print(str(row[0]).ljust(10) + " \t " + str(row[1]).ljust(7) + " \t " + str(row[2]).ljust(5))

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
print('category_name\t category_id\t product_name\t\t\t\t\t\t product_id\t unit_price\t units_in_stock\t units_on_order\t reorder_level\t discontinued')
for row in rows:
    print(str(row[0]).ljust(13) + " \t "#catname
          + str(row[1]).ljust(13) + " \t "#catid
          + str(row[2]).ljust(28) + " \t\t "#prodname
          + str(row[3]).ljust(7) + " \t "#prodid
          + str(row[4]).ljust(7) + " \t "#unitprice
          + str(row[5]).ljust(12) + " \t "#uis
          + str(row[6]).ljust(10) + " \t "#uoo
          + str(row[7]).ljust(10) + " \t "#reoderlvl
          + str(row[8]).ljust(5))#discont.


# Question-4
print(str('Question-4'))
cursor.execute("""select ship_name, ship_country, customers.customer_id, customers.company_name,
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
order by ship_name asc, ship_country desc, customer_id asc, salesperson asc;""")
rows = cursor.fetchall()
print('ship_name\t\t\t\t\t\t ship_country\t customer_id\t company_name\t\t\t\t\t salesperson\t\t phone\t\t\t\t product_id\t\t product_name\t\t\t\t\t freight')
for row in rows:
    print(str(row[0]).ljust(30) + " \t "#shipname
          + str(row[1]).ljust(10) + " \t "#shipcountry
          + str(row[2]).ljust(7) + " \t\t "#customerid
          + str(row[3]).ljust(27) + " \t "#company name
          + str(row[4]).ljust(15) + " \t "#sales person
          + str(row[5]).ljust(10) + " \t "#phone
          + str(row[6]).ljust(10) + " \t "#proudct id
          + str(row[7]).ljust(28) + " \t "#product name
          + str(row[8]))#freight.

# Write your piece of code as in Question-1

# Question-5
print(str('Question-5'))

# Write your piece of code as in Question-1

# Question-6
print(str('Question-6'))

# Write your piece of code as in Question-1

# Question-7
print(str('Question-7'))

# Write your piece of code as in Question-1

# Question-8
print(str('Question-8'))

# Write your piece of code as in Question-1

connection.commit()
connection.close()
