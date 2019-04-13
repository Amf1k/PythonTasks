print('Введите целое число')
num = abs(int(input()))
if num == 0:
    print('число разрядов: ', 1)
else:
    count = 0;
    while num > 0:
        count += 1
        num = num // 10
    print('число разрядов: ', count)
