import os
import random
import math
import binascii
import socket
from binascii import b2a_hex, a2b_hex
from Crypto.Cipher import AES

halfkeyLength = 512
p_length = 300
q_length = 724
host = "192.168.146.128"   
port = 25535
addr = (host, port)
byte = 1024
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
    M = str2int(M)
    return fem(M, e, n)

def decryption(C, d, n):
    m = fem(C, d, n)
    m = int2str(m)
    return m

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

x = "aa"
x = x.encode('utf-8')
sock.sendto(x, addr)
#n = raw_input()
n, addr = sock.recvfrom(byte)
n = n.decode("utf-8")
n = int(n)
#e = raw_input()
e, addr = sock.recvfrom(byte)
e = e.decode("utf-8")
e = int(e)
#C = raw_input()
C, addr = sock.recvfrom(byte)
C = C.decode("utf-8")
C = int(C)
#n = int(n)
#e = int(e)
#C = int(C)
#mm = raw_input()
mm, addr = sock.recvfrom(byte)
mm = mm.decode("utf-8")
mm = a2b_hex(mm)
#mm = mm.decode("hex")
message = "it_is_my_request"
m2 = "what's_your_next"
m3 = "it's_invalid_one"
#mes = str2int(message)
key = fe(2, 127)
key = int2str(key)
tmp = fe(2, 127)
count = 127
x = count * e
Cb = C * fem(2, x, n)
Cb = Cb % n
print("count:", count)
print("key:", key)
if(len(key) == 16):
       decipher = AES.new(key, AES.MODE_ECB)
       print("message:", decipher.decrypt(mm))
print("Cb")
print(Cb)
Cb = str(Cb)
text = Cb.encode('utf-8')
sock.sendto(Cb, addr)
Cb = int(Cb)

cipher = AES.new(key, AES.MODE_ECB)
msg = cipher.encrypt(message)
print("msg:")
text = msg
text = b2a_hex(text)
sock.sendto(text, addr)
print(msg.encode("hex"))




for i in range (128):
     #m = raw_input()
     data, addr = sock.recvfrom(byte)
     m = data.decode("utf-8")
     #m = int(m)
     print("count:", count)
     if(m == m2):
           print("key:", key)
           if(len(key) == 16):
                  decipher = AES.new(key, AES.MODE_ECB)
                  print("message:", decipher.decrypt(mm))
           key = str2int(key)
           key = key / 2
           key = key + tmp
     if (m == m3):
           key = str2int(key)
           key = key ^ tmp
           key = int2str(key)
           print("key:", key)
           if(len(key) == 16):
                  decipher = AES.new(key, AES.MODE_ECB)
                  print("message:", decipher.decrypt(mm))
           key = str2int(key)
           key = key / 2
           key = key + tmp

     key = int2str(key)
     count = count - 1
     x = count * e
     Cb = C * fem(2, x, n)
     Cb = Cb % n
     print("Cb:")
     print(Cb)
     Cb = str(Cb)
     text = Cb.encode('utf-8')
     sock.sendto(text, addr)
     Cb = int(Cb)
     cipher = AES.new(key, AES.MODE_ECB)
     msg = cipher.encrypt(message)
     print("msg:")
     text = msg
     text = b2a_hex(text)
     sock.sendto(text, addr) 
     print(msg.encode("hex"))

#decipher = AES.new(key, AES.MODE_ECB)
#print("message:", decipher.decrypt(mm))
