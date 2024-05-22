def factorial(number):
    if number == 1:
        return 1
    else:
        return number * factorial(number-1)

def trailingZeros(n):
    count = 0
    if n < 5:
        return 0
    else:
        while(n >= 5):
            n //= 5
            count += n
        return count
