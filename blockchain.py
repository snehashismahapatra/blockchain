import hashlib
import datetime
import secrets
import KeyGenerator


class client:
  def __init__(self,seed,block):
    kg = KeyGenerator.KeyGenerator()
    kg.seed_input(seed)
    self.private_key=kg.generate_private_key()
    self.public_key=kg.generate_public_key(self.private_key)
    self.wallet_address=kg.get_wallet_address(self.public_key)
    self.wallet_track=[]
    self.amount=0
    self.block=block
  
  def identity(self):
    return self.wallet_address
  
  def make_transaction(self,reciver,value):
    if self.amount>=value:
      t=transaction(self.wallet_address,reciver,value).request_transaction()
      self.block.request_transaction(t)
      self.amount=self.amount-value
    else:
      print("Amount exhausting")

  def info(self):
    print("private key : ",self.private_key)
    print("wallet address : ",self.wallet_address)
    print("amount : ",self.amount)
    print("Transaction : ",self.wallet_track)

class transaction:
  def __init__(self,sender,receiver,value):
    self.sender = sender
    self.receiver = receiver
    self.value = value
    self.time = datetime.datetime.now()
  
  def request_transaction(self):
    dic={"sender":self.sender,"receiver":self.receiver,"value":self.value,"time":self.time}
    return dic

class miner:
  def __init__(self,difficulty,ele,block):
    self.difficulty=difficulty
    self.prefix_ele=ele
    self.block=block
  
  def mine(self):
    transac_i=self.find_transaction()
    transac=self.block.transaction_pool[transac_i]
    prefix=self.prefix_ele*self.difficulty
    st=""
    for i in transac:
      st=st+str(i)+":"+str("j")+"\n"
    data=st
    st=st+"\n"+self.block.getcurrent_block()["hash"]
    hash=hashlib.sha256(st.encode('ascii')).hexdigest()
    cur_hash=hash
    i=0
    while not cur_hash.startswith(prefix):
      cur_hash=hashlib.sha256(str(hash+str(i)).encode('ascii')).hexdigest()
      i=i+1
    self.block.create_block(i,cur_hash,data)
    del self.block.transaction_pool[transac_i]
    return True

  def find_transaction(self):
    max=0
    max_i=0
    for t in range(len(self.block.transaction_pool)):
      if self.block.transaction_pool[t]["value"]>max:
        max=self.block.transaction_pool[t]["value"]
        max_i=t
    return max_i
    

class Blockchain:
  def __init__(self):
    self.difficulty=1
    self.prefix_ele="1"
    self.chain=[]
    self.transaction_pool=[]

  def create_genesis_block(self,receiver,value,rec):
    data={"sender":"Genesis","receiver":receiver,"value":value,"time":datetime.datetime.now()}
    st="sender:Genesis\nreceiver:"+receiver+"\nvalue:"+str(value)+"\ntime:"+str(data["time"])
    block={"index":1,
          "timeStamp":str(datetime.datetime.now()),
          "transaction":data,
          "Nonce":0,
          "Pre_hash":0,
          "hash":hashlib.sha256(str(st).encode('ascii')).hexdigest()}
    self.chain.append(block)
    rec.amount=value

  
  def create_block(self,nonce,hash,data):
    block={"index":len(self.chain)+1,
          "timeStamp":str(datetime.datetime.now()),
          "transaction":data,
          "Nonce":nonce,
          "Pre_hash": self.getcurrent_block()["hash"],
          "hash":hash}
    self.chain.append(block)
    if len(self.chain)%10:
      self.difficulty=self.difficulty+1
  
  def getcurrent_block(self):
    return self.chain[-1]
  
  def request_transaction(self,transac):
    self.transaction_pool.append(transac)
    return

  def blockchainshow(self):
    for i in self.chain:
      print(i)
     
blockchain=Blockchain()
tom=client("I am honest",blockchain)
blockchain.create_genesis_block(tom.identity(),5000,tom)
print("tom: ",tom.identity())
jerry=client("I am client",blockchain)
print("jerry: ",jerry.identity())
tom.make_transaction(jerry.identity(),500)
print(blockchain.transaction_pool)
print(blockchain.chain)
m1=miner(blockchain.difficulty,blockchain.prefix_ele,blockchain)
if m1.mine():
  jerry.amount=jerry.amount+500

print(blockchain.transaction_pool)
print(blockchain.chain)
tom.info()
jerry.info()