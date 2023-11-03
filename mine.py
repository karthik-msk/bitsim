import hashlib
import shutil
import time
import os
import sys

txs = []
blocks = []
tx_per_block = 50
prev_hash = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
total_blocks = 0
difficulty = 4

if(os.path.exists("chain")):
    shutil.rmtree("chain")

os.makedirs("chain")

def hash256(string):
    return hashlib.sha256(string.encode("utf-8")).hexdigest()

def merkleTree(hashlist):
    if len(hashlist)%2==1:
        hashlist.append(hashlist[-1])
    #print(hashlist)
    newlist = []
    for i in range(0, len(hashlist), 2):
        newlist.append(hashlist[i]+hashlist[i+1])
    #print(newlist)
    hashlist = []
    hashlist = [hash256(i) for i in newlist]
    #print(hashlist)
    if len(hashlist) == 1:
        return(hashlist[0])
    return(merkleTree(hashlist))

def create_file(block_number, hash_value, content):
    filename = str(block_number) + "-" + hash_value + ".txt"
    blocks.append(filename)
    with open("chain/"+filename, "w") as file:
        file.write(content)
    
def verify():
    print("\nVerifying validity of the chain...")
    if(len(blocks) > 1):
        for i in range(len(blocks)-1):
            with open("chain/"+blocks[i], "r") as file:
                content = file.read()
                curHash = hash256(content)
            with open("chain/"+blocks[i+1], "r") as file:
                lines = file.readlines()
                prevHashLine = lines[1]
                prevHash = prevHashLine.split(" : ")[1].replace("\n","")
            if(curHash!=prevHash):
                print("BLOCK NUMBER : ", i," HAS BEEN TAMPERED. CHAIN COLLAPSED")
                sys.exit()
    time.sleep(1)
    print("CHAIN IS VALID")
    time.sleep(1)

def mine(transactions, difficulty, merkleroot):
    global total_blocks, prev_hash
    new_nonce = -1
    hash_value = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    
    block = """Block Number : %d\nPrevious Hash : %s\nMerkle Root : %s\nNonce : %d\nTransactions : \n"""%(total_blocks, prev_hash, merkleroot, new_nonce)
    
    for tx in transactions:
        block = block+tx

    while hash_value[0:difficulty] != "0"*difficulty:
        #print(block)
        print(hash_value, new_nonce)
        print("-----------------------------------------------------------------------------")
        lines = block.split("\n")
        cur_nonce = lines[3]
        print("``````````````````", cur_nonce)
        cur_value = int(cur_nonce.split(" : ")[1])
        new_value = cur_value+1
        new_nonce = "Nonce : "+str(new_value)
        block = block.replace(cur_nonce, new_nonce)
        hash_value = hash256(block)
    total_blocks = total_blocks + 1
    prev_hash = hash_value
    print("MINED BLOCK : ", hash_value)
    print("With nonce value : ", new_value)
    create_file(total_blocks-1, hash_value, block)
    #print(blocks)

while True:
    while True:
        time.sleep(3)
        with open("unconfirmed_transactions.txt", "r") as file:
            con = file.readlines()
            if(len(con)>tx_per_block):
                transactions_to_verify = con[:tx_per_block]
                remaining_transactions = con[tx_per_block:]
                break
        print("Waiting for adequate transactions...")
    
    with open("unconfirmed_transactions.txt", "w") as file:
        file.writelines(remaining_transactions)
    
    hashlist = [hash256(i) for i in transactions_to_verify]
    merkleroot = merkleTree(hashlist)

    mine(transactions_to_verify, difficulty, merkleroot)
    verify()

    with open("confirmed.txt", "a+") as file:
        file.writelines(transactions_to_verify)
