x = "world"
print("Welcome","to",x,end=" | ")
print("Hi")

a = 2
b = 3

#format with index
print("{} + {} is {}".format(a,b,a+b))

#format using key
print("{a} + {b} is {c}".format(a=a,b=b,c=a+b))

#old style format
print("%d + %d is %d"%(a,b,a+b))

#using f-string (Recommended for Python 3.6+)
print(f"{a} + {b} is {a+b}")

phi = 22/7
print(f"phi is {phi:.2f}")

salary = 100000000
print(f"your salary is {salary:,}")

#Alignment formatting
print("-----------------------------------")
print(f"{'Name':<20} {'Class':^5} {'Score':>5}")
print("-----------------------------------")
print(f"{'Muhammad Nizar':<20} {'25i':^5} {'100':>5}")
print(f"{'Faizi':<20} {'25i':^5} {'100':>5}")
print(f"{'Regith':<20} {'25i':^5} {'99':>5}")

print("%X"%32)