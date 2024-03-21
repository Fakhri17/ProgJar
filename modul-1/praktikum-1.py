# hitung huruf
print("Program menghitung huruf pada kata")
kata = input("Masukkan Kata: ")
print("Jumlah huruf pada kata", kata, "adalah", len(kata))
print("\n")

# HITUNG KELILING & LUAS LINGKARAN DARI JARI2 YANG DIINPUT
print("Program menghitung keliling lingkaran")
jari2 = float(input("Masukkan jari-jari: "))
luas = 3.14 * jari2 * jari2
keliling = 2 * 3.14 * jari2
print("Luas lingkaran: ", luas)
print("Keliling lingkaran: ", keliling)
print("\n")

# Farenheit to Celcius
print("Program konversi suhu farenheit ke celcius")
farenheit = float(input("Masukkan suhu dalam farenheit: "))
celcius = (farenheit - 32) * 5/9
print("Suhu dalam celcius: ", celcius)
print("\n")

# print bilangan genap 1-100
print("Program menampilkan bilangan genap 1-100")
for i in range(1, 101):
    if i % 2 == 0:
        print(i, end=" ")

print("\n")

