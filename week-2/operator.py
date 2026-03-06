# banknotes (break down money into smaller bills/coin)
# for example 98.000 
# mod50 = 98000 % 50000
# money50 = (98.000 - mod50)/50000

bills100 = 100000
bills50 = 50000
bills20 = 20000
bills10 = 10000
bills5 = 5000
bills2 = 2000
bills1 = 1000

money = float(input("Please input your amount: "))
mod100 = money % bills100
money100 = (money - mod100)/bills100

mod50 = mod100 % bills50
money50 = (mod100 - mod50)/bills50

mod20 = mod50 % bills20
money20 = (mod50 - mod20)/bills20

# please continue the rest

print(money100, "pcs of 100000")
print(money50, "pcs of 50000")
print(money20, "pcs of 20000")