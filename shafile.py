import hashlib

file_name = 'sha.py'

with open(file_name) as f:
    data = f.read()
    sha256hash = hashlib.sha256(data.encode("utf-8")).hexdigest()
print(sha256hash)