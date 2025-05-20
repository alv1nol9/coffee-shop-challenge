from customer import Customer
from coffee import Coffee
from order import Order

# Create Customers
c1 = Customer("Alice")
c2 = Customer("Bob")

# Create Coffees
latte = Coffee("Latte")
mocha = Coffee("Mocha")

# Create Orders
o1 = c1.create_order(latte, 3.5)
o2 = c1.create_order(mocha, 4.0)
o3 = c2.create_order(latte, 5.0)
o4 = c2.create_order(latte, 2.0)

print(f"Alice's Coffees: {[coffee.name for coffee in c1.coffees()]}")
print(f"Latte Orders: {len(latte.orders())}")
print(f"Latte Average Price: {latte.average_price():.2f}")
print(f"Latte Customers: {[customer.name for customer in latte.customers()]}")
print(f"Top spender on Latte: {Customer.most_aficionado(latte).name}")
