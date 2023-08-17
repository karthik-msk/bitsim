import hashlib
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


trans = ["Nimish pays Bhavesh 0.123 BTC 24001","Tarique pays Karthikeyan 8.4859 BTC 24002","Stalin pays Rajveer 9.864 BTC 24003","Chandrashekhar pays Smitesh 7.9913 BTC 24004"]
hashlist = [hash256(i) for i in trans]
a = merkleTree(hashlist)
print(a)
#print(res)
#print(hashlist)