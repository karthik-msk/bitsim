import hashlib

file_name = 'sha.py'
data2 = """import hashlib

while True:
    inp = input("Enter a string : ")
    res = hashlib.sha256(inp.encode('utf-8')).hexdigest()
    print("hash value : ", res)"""

new = hashlib.sha256(data2.encode("utf-8")).hexdigest()
with open(file_name) as f:
    data = f.read()
    print(data)
    print(data2)
    sha256hash = hashlib.sha256(data.encode("utf-8")).hexdigest()
print(sha256hash)
print(new)