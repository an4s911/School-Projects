f = open("pledge.txt", 'r')
str1 = f.read(10)
str2 = f.read(5)
str3 = f.read()
print("Output of first read:\n", str1, "\nOutput of second read:\n", str2, "\nOutput of third read:\n", str3)