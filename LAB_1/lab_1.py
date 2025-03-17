print("Hello world !!")

num1 = 22
num2 = 44

sum = num1+num2


print(f"The sum of {num1} and {num2} is {sum} ")

num = 100

root = num**0.5

print(f"The sqrt of {num} is {root}")

num3 = int(input("Give the first no.:"))
num4 = int(input("Give the second no.:"))

summ = num4 + num3

print(f"The sum of {num3} and {num4} is {summ}")

a = float(input('Enter first side: '))
b = float(input('Enter second side: '))
c = float(input('Enter third side: '))

s = (a + b + c) / 2

area = (s*(s-a)*(s-b)*(s-c)) ** 0.5
print('The area of the triangle is %0.2f' %area)

# Solve Quadratic Equations

import cmath

a = 32
b = 23
c = 45

d = (b**2) - (4*a*c)

sol1 = (-b-cmath.sqrt(d))/(2*a)
sol2 = (-b+cmath.sqrt(d))/(2*a)

print(f"The solution of the numbers are {sol1} and {sol2}")

# Random Variable generation

from random import *

ran_num = randint(0, 9)

print(F"The random number generated is {ran_num}")

# Converting Kilometer into miles

km = float(input("Enter the value in km: "))

conv_factor = 0.621371

miles = km * conv_factor

print(f"The vale of {km} kilometers is {miles} miles")

# odd or even

no = int(input("Enter a no.: "))

if no%2 == 0:
  print("the no. entered is even" )
else:
  print("the no. entered is odd")

# Check a no. is prime or not

num = int(input("Enter a number: "))

flag = False

if num == 0 or num == 1 :
  print("The no. given is prime")

elif num > 1 :
  for i in range(2, num):
    if (num % i) == 0:
      flag = True
      break

  if flag :
    print("The no. is not a prime")
  else :
    print("The no. is a prime ")

