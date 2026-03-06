name = "Nugraha"

print(name[1])
print(name[1:])
print(name[-3:])
print(name[:-2])

name = "I Love Sukabumi and Bandung"
splitword = name.split()
print(splitword)
someword = splitword[2:][::-1]
print(someword)
joinword = ",".join(someword)
print(joinword)
final = joinword.replace(",and","")
print(final)