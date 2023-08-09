import time
txs = []
while True:
    while True:
        time.sleep(3)
        with open("transactions.txt", "r") as file:
            con = file.readlines()
            if(len(con)>2):
                txs = con[:2]
                rem = con[2:]
                break
    with open("transactions.txt", "w") as rewrite:
        rewrite.writelines(rem)
    with open("confirmed.txt", "a+") as update:
        update.writelines(txs)

