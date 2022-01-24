import csv

mylist = ['monk', 2, 3, 4, 5, 6, 7, 8, 9, 0]

with open('filename.csv', 'w') as myfile:
    wr = csv.writer(myfile, quoting = csv.QUOTE_ALL)
    wr.writerow(mylist)



def foo(a, b):
    return a + bar(b)


def bar(b):
    return b

print(foo(1,2))

