
# Function to check if a number is prime
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

# Function to print prime numbers from 1 to n
def print_prime(n):
    for i in range(1, n+1):
        if is_prime(i):
            print(i, end=" ")


angka = int(input("Masukkan angka: "))
print_prime(angka)
            