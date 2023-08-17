import hashlib

while True:
    inp = input("Enter a string : ")
    res = hashlib.sha256(inp.encode('utf-8')).hexdigest()
    print("hash value : ", res)