def kelipatanOk(n):
  for i in range(1, n+1):
    if i % 3 == 0 and i % 4 == 0:
      print(f"{i} = OKYES")
    elif i % 3 == 0:
      print(f"{i} = OK")
    elif i % 4 == 0:
      print(f"{i} = YES")
    else:
      print(i)

n = int(input("Masukkan nilai n: "))
kelipatanOk(n)
