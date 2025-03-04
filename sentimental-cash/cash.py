from cs50 import get_float

# getting dollars input (only floats)
cents = get_float("Change owed: ")
while True:
    if cents < 0:
        cents = get_float("Change owed: ")
    else:
        break
# calculating quarters
quarters = 0
while True:
    if cents >= 0.25:
        quarters += 1
        cents -= .25
    else:
        break
cents = round(cents, 2)
# calculating dimes
dimes = 0
while True:
    if cents >= .10:
        dimes += 1
        cents -= .10
    else:
        break
cents = round(cents, 2)
# calculating nickels
nickels = 0
while True:
    if cents >= 0.05:
        nickels += 1
        cents -= .05
    else:
        break
cents = round(cents, 2)
# calculating pennies
pennies = 0
while True:
    if cents >= 0.01:
        pennies += 1
        cents -= .01
    else:
        break
# printing the change
print(f"{quarters + dimes + nickels + pennies}")