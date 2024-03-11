def fibonacci(n):
    if n == 0:
        print('Call to fibonacci(%s) returning 0.' % (n))
        return 0
    elif n == 1 or n == 2:
        print('Call to fibonacci(%s) returning 1.' % (n))
        return 1
    else:
        print('Call to fibonacci(%s) and fibonacci(%s)' % (n-1, n-2))
        result = fibonacci(n - 1) + fibonacci(n - 2)
        print('Call to fibonacci(%s) returning %s.' % (n, result))
    return result

