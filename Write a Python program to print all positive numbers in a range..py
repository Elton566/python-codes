# Python program to print positive Numbers in a range
 
start, end = -4, 20
 
# iterating each number in list
for num in range(start, end + 1):
     
    # checking the condition
    if num >= 0:
        print(num, end = " ")