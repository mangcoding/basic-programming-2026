hourly_fee = int(input("Tarif Per jam: "))
hour = int(input("Total Jam: "))
minutes = int(input("kelebihan menit: "))

hour_from_minutes = minutes/60
total_hour = hour+hour_from_minutes
salary = total_hour*hourly_fee

print("Hourly Fee",hourly_fee)
print("Total Hourly",total_hour)
print("Salary", salary)