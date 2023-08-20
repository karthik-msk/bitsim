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
difficulty = 1

if(os.path.exists("blocks")):
    shutil.rmtree("blocks")

os.makedirs("blocks")

def hash256(string):
    return hashlib.sha256(string.encode("utf-8")).hexdigest()

def merkleTree(hashlist):
    if len(hashlist)%2==1:
        hashlist.append(hashlist[-1])
    print(hashlist)
    newlist = []
    for i in range(0, len(hashlist), 2):
        newlist.append(hashlist[i]+hashlist[i+1])
    #print(newlist)
    hashlist = []
    hashlist = [hash256(i) for i in newlist]
    print(hashlist)
    if len(hashlist) == 1:
        return(hashlist[0])
    return(merkleTree(hashlist))

def create_file(total_blocks, hash, content):
    filename = str(total_blocks) + "-" + hash + ".txt"
    blocks.append(filename)
    with open("blocks/"+filename, "w") as file:
        file.write(content)
    
def verify():
    print("Verifying validity of the chain...")
    if(len(blocks) > 1):
        for i in range(len(blocks)-1):
            with open("blocks/"+blocks[i], "r") as file:
                content = file.read()
                curHash = hash256(content)
            with open("blocks/"+blocks[i+1], "r") as file:
                lines = file.readlines()
                prevHashLine = lines[1]
                prevHash = prevHashLine.split(" : ")[1].replace("\n","")
            #print(curHash)
            #print(prevHash)
            #print("-------------------")
            if(curHash!=prevHash):
                print("BLOCK NUMBER : ", i," HAS BEEN TAMPERED. CHAIN COLLAPSED")
                sys.exit()

    print("The chain is VALID")
    time.sleep(1)

def mine(transactions, difficulty, merkleroot):
    global total_blocks, prev_hash
    new_nonce = -1
    hash_value = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    block = """Block Number : %d\nPrevious Hash : %s\nMerkle Root : %s\nNonce : %d
    \nTransactions : \n"""%(total_blocks, prev_hash, merkleroot, new_nonce)
    for i in transactions:
        block = block+i
    while hash_value[0:difficulty] != "0"*difficulty:
        #print(block)
        print(hash_value, new_nonce)
        print("-------------------------------------------")
        lines = block.split("\n")
        cur_nonce = lines[3]
        cur_value = int(cur_nonce.split(":")[1])
        new_value = cur_value+1
        new_nonce = "Nonce : "+str(new_value)
        block = block.replace(cur_nonce, new_nonce)
        hash_value = hash256(block)
    total_blocks = total_blocks + 1
    prev_hash = hash_value
    print("-MINED", block, hash_value)
    create_file(total_blocks-1, hash_value, block)
    #print(blocks)

while True:
    while True:
        time.sleep(3)
        with open("unconfirmed_transactions.txt", "r") as file:
            con = file.readlines()
            if(len(con)>tx_per_block):
                current_transactions = con[:tx_per_block]
                remaining = con[tx_per_block:]
                break
    
    with open("unconfirmed_transactions.txt", "w") as rewrite:
        rewrite.writelines(remaining)
    hashlist = [hash256(i) for i in current_transactions]
    merkleroot = merkleTree(hashlist)


    mine(current_transactions, difficulty, merkleroot)
    verify()

    
    with open("confirmed.txt", "a+") as update:
        update.writelines(current_transactions)
