import math

def trib(n):

    # https://mathworld.wolfram.com/TribonacciNumber.html

    ot = (1/3)

    up = (19 + 3*math.sqrt(33))**ot
    um = (19 - 3*math.sqrt(33))**ot

    s = (586 + 102*math.sqrt(33))

    numerator = 3 * ((ot*up + ot*um + ot)**(n+1)) * (s**ot) # n+1 because we are considering that trib(0) = 1
    denominator = (s**(2/3)) + 4 - 2*(s**ot)

    return round(numerator/denominator) # Python does not have enough precision

def main():
    for i in range(0, 100):
        print(i, trib(i))

if __name__ == '__main__':
    main()