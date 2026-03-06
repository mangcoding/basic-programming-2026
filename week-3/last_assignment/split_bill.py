people = int(input("Berapa jumlah yang jajan? :"))
bill = float(input("Berapa jumlah yang harus dibayar? :"))
tax = 10

#total setelah pajak
total = bill + tax/100 * bill
bill_per_people = total/people

print("Total Orang", people)
print("Total Tagihan", bill)
print("Total setelah pajak", total)
print('Jumlah yang harus dibayar per {:.2f}'.format(bill_per_people))