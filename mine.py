import hashlib
import time
txs = []
tx_per_block = 2
prev_hash = 0
bl = 0
difficulty = 4

def hash256(string):
    return hashlib.sha256(string.encode("utf-8")).hexdigest()

def mine(transactions, difficulty):
    global bl, prev_hash
    nonce = -1
    hash_value = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    block = """Block Number : %d\nPrevious Hash : %d\nNonce : %d
    \nTransactions : \n"""%(bl, prev_hash, nonce)
    for i in transactions:
        block = block+i
    while hash_value[0:difficulty] != "0"*difficulty:
        print(block)
        print(hash_value)
        print("-------------------------------------------")
        lines = block.split("\n")
        cur_nonce = lines[2]
        cur_value = int(cur_nonce.split(":")[1])
        new_value = cur_value+1
        new_nonce = "Nonce : "+str(new_value)
        block = block.replace(cur_nonce, new_nonce)
        hash_value = hash256(block)
    bl= bl + 1
    print("-MINED", block, hash_value)

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

    mine(current_transactions, difficulty)
    
    with open("confirmed.txt", "a+") as update:
        update.writelines(current_transactions)
