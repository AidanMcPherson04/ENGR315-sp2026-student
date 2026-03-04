# this will test your ability to write a while loop
# use the print() statement to determine whether your number is correct

# an example while loop is given below
a = 1
while a != 5:
    a = a + 1  # pay attention where the counter (this part of the loop) is located
    print("not 5 yet, but we're at " + str(a))
    if a == 5: 
         break # this is to prevent an infinite loop while you are writing your code


# now, move the counter to before the print statement
# notice how the value of a has changed in the print value,
# but remains the same in the actual value of a

# first, we're going to write the condition of a while loop
# this loop is going to multiply the variable x by 2 3 times
b = 5
x = 0
while x != 3:
    b = b * 2
    x = x + 1
    if x == 3:
        break # this is to prevent an infinite loop while you are writing your code

# now, try and write the body of a while loop that should add a variable to itself 5 times
# when writing the code delete "break" - this is to prevent an infinite loop
c = 3
y = 0
while y < 5:
    c = c + c
    y = y + 1
    if y == 5:
        break

# it's time to combine both of these concepts.
# write a loop entirely from scratch that prints out a statement 6 times
# the counter variable you will use is z
z = 0
while z < 6:
    print("This is the " + str(z) + "th time this statement has been printed")
    z = z + 1
    if z == 6:
        break