from cs50 import get_int
# getting input
n = get_int("Height: ")
while True:
    if n < 1 or n > 8:
        n = get_int("Height: ")
    else:
        break

for i in range(n):  # for each column
    for j in range(n):  # for each row
        if (i + j < n - 1):
            print(" ", end="")
        else:
            print("#", end="")
    print("\n", end="")
