import os
import random
import math
import hashlib

k0 = 512
k1 = 384

halfkeyLength = 512
p_length = 300
q_length = 724

def fem(b, e, m):
    result = 1
    while e != 0:
        if (e & 1) == 1:
            result = (result * b) % m
        e >>= 1
        b = (b*b) % m
    return result

def fe(b, e):
    result = 1
    while e != 0:
        if (e & 1) == 1:
            result = (result * b)
        e >>= 1
        b = (b*b)
    return result

def miller_rabin(num):
    s = num - 1
    t = 0
    while s % 2 == 0:
        s = s // 2
        t += 1

    for trials in range(18):
        a = random.randint(2, num - 1)
        v = fem(a, s, num)
        if v != 1:
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = fem(v, 2, num)
    return True


def is_prime(num):
    if num < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
    if num in small_primes:
        return True
    for prime in small_primes:
        if num % prime == 0:
            return False
    return miller_rabin(num)


def get_prime(size):
    while True:
        num = random.randrange(fe(2,size-1), fe(2,size))
        if is_prime(num):
            return num


def EX_GCD(a,b,arr):
    if b == 0:
        arr[0] = 1
        arr[1] = 0
        return a
    g = EX_GCD(b, a % b, arr)
    t = arr[0]
    arr[0] = arr[1]
    arr[1] = t - (a // b) * arr[1]
    return g

def ModReverse(a,n):
    arr = [0,1,]
    gcd = EX_GCD(a,n,arr)
    if gcd == 1:
        return (arr[0] % n + n) % n
    else:
        return -1

def computeD(fn, e):
    return ModReverse(e, fn)

def keyGeneration():
    n = 0
    a = fe(2, 1023)
    b = fe(2, 1024)
    while (n < a or n > b - 1):
        p = get_prime(p_length)
        q = get_prime(q_length)
        n = p * q
    
    fn = (p-1) * (q-1)
    e = 65537
    d = computeD(fn, e)
    return (n, e, d, p, q)

def encryption(M, e, n):
    return fem(M, e, n)

def decryption(C, d, n):
    return fem(C, d, n)

def str2int(m):
    tmp = 0;
    for i in range (len(m)):
        tmp = tmp + ord(m[len(m) - 1 - i]) * fe(2, 8 * i)
    return tmp

def int2str(t):
    #print ("t:",t)
    tmp = t
    c = 0
    while (tmp != 0):
        tmp = tmp // fe(2, 8)
        c = c + 1
    m = ""
    m2 = ""
    for i in range(c):
        m += chr(t % fe(2, 8))
        t = t // fe(2, 8)
    for i in range(c):
        m2 += m[len(m) - 1 - i]
    return m2

def OAEP(m, k0, k1):
    r = ""
    for i in range (k0 // 8):
        r += int2str(random.randint(0, 255))
    s = hashlib.shake_256()
    s.update(r.encode("utf8"))

    m = str2int(m)
    m2 = m << k1
    m2 = int2str(m2)
    tmp1 = str2int(m2)
    tmp2 = str2int(s.hexdigest((1024 - k0) // 8))
    x = tmp1 ^ tmp2
    x = int2str(x)

    s2 = hashlib.shake_256()
    s2.update(x.encode("utf8"))
    tmp1 = str2int(s2.hexdigest(k0//8))
    tmp2 = str2int(r)
    y = tmp1 ^ tmp2
    y = int2str(y)

    return (x, y)

def ReverseOAEP(x, y):
    s2 = hashlib.shake_256()
    s2.update(x.encode("utf8"))
    tmp1 = str2int(s2.hexdigest(k0//8))
    tmp2 = str2int(y)
    r = tmp1 ^ tmp2
    r = int2str(r)

    tmp1 = str2int(x)
    s = hashlib.shake_256()
    s.update(r.encode("utf8"))
    tmp2 = str2int(s.hexdigest((1024 - k0) // 8))
    m2 = tmp1 ^ tmp2

    m = m2 >> k1
    m = int2str(m)
    return m
    
AES_key = "0000111122223333"
print ("AES_KEY:", AES_key, '\n')

(x, y) = OAEP(AES_key, k0, k1)
print ("x:", x, '\n\n', "y:", y, '\n')
m = ReverseOAEP(x, y)
print ("m:", m, '\n')

print ("check correctness:", AES_key == m)
