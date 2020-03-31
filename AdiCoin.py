import datetime
import hashlib
import json
import requests
from flask import Flask,jsonify,request
from uuid import uuid4
from urllib.parse import urlparse
#### Building a Crytocurrency ########

class Blockchain:
    def __init__(self):
        self.chain=[]           #list that will contain all our block
        self.transactions=[]    #store trnsaction
        self.create_block(proof = 1,prev_hash='0')      #to create our first block or (Genesis block)
        self.nodes=set()

    def create_block(self,proof,prev_hash):
        block={'index':len(self.chain)+ 1, 
        'timestamp':str(datetime.datetime.now()),
        'proof':proof,
        'prev_hash':prev_hash,
        'transactions':self.transactions}
        self.transactions=[]
        self.chain.append(block)      # create and append the block to our chain
        return block
    def get_prev_block(self):
        return self.chain[-1]       # get the last block of the chain
    def proof_of_work(self,prev_proof):
        new_proof= 1
        check_proof=False
        while check_proof is False:
            hash_operation= hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_operation[:4] =='0000':
                check_proof=True        #when four 0 are meet then we break the loop as we have mined our coin
            else:
                new_proof+=1
        return new_proof

    def hash(self,block):
        encoed_block =json.dumps(block, sort_keys=True).encode() #get the hash of each block json dumps is used to conert our dictonary as string
        return hashlib.sha256(encoed_block).hexdigest()  #return hexvalue

    def verify(self,chain):
        previousBlock=self.chain[0]
        blockIndex=1
        while blockIndex<len(chain):
            block=chain[blockIndex]
            if block['prev_hash'] != self.hash(previousBlock):
                return False                        #return false when the hash of the previous block doesn't match the current block
            prev_proof=previousBlock['proof']
            proof=block['proof']
            hash_operation= hashlib.sha256(str(proof*3 - prev_proof*3).encode()).hexdigest()      #get the hash generated inorder to check if it follows our four 0 rule
            if hash_operation [:4]!='0000':
                return False                    #return false it the genrated hash doesn't follow our rule
            previousBlock=block     #increment the previous block to our current block
            blockIndex+=1   #increment to the next block
        return True

    def add_trans(self,sender,receiver,amount):
        self.transactions.append({'sender':sender,
            'receiver':receiver,
            'amount':amount})
        prev_blck= self.get_prev_block()
        return prev_block

    def add_node(self,address):
        parsed_url=urlparse(address)        # distibute the url in diffrent part
        self.nodes.add(parsed_url.netloc)    #add the netloc that is basically th ip address
        
    def  replace_chain(self):
        network = self.nodes
        longest_chain = None    #to find the longest chain in our decentralized system
        max_length = len(self.chain)
        for node in network:
            response=response.get(f'http://{node}/get_block')
            if response.status_code==200:
                response.json()['length']
                chain=response.json()['chain']
                if length > max_length and self.verify(chain):
                    max_length=length
                    longest_chain=chain
        if longest_chain:
            self.chain=longest_chain
            return True
        return False

##### WEB APP ######
blockchain=Blockchain()

#addrss for the node on Port 5000
node_address = str(uuid4()).replace('-','') 
 

app=Flask(__name__)

@app.route('/mine',methods=['GET'])
def mine():
    prev_block=blockchain.get_prev_block()      #get the previous block
    prev_proof=prev_block['proof']      #get the proof from the previous block
    proof=blockchain.proof_of_work(prev_proof)      #get the proof of the mined block
    prev_hash=blockchain.hash(prev_block)   #get the hash of revious block
    blockchain.add_trans(sender=node_address,receiver='Aditya',amount=100)
    block=blockchain.create_block(proof,prev_hash)      #creating our new block just by inserting the value
    response= {'message':"Block Minned",
    'index':block['index'],
    'timestamp':block['timestamp'],
    'proof':block['proof'],
    'prev_hash':block['prev_hash'],
    'transactions':block['transactions']}
    return jsonify(response),200


#### Create a Blockchain ######
    

#### Get Full Blockchain ####
@app.route('/get_chain',methods=['GET'])
def get_chain():
    response={'chain':blockchain.chain,
    'length':len(blockchain.chain)}
    return jsonify(response),200

@app.route('/verify',methods=['GET'])
def verify():
    result=blockchain.verify(blockchain.chain)  #returns true if there is no error in our entire block chain
    if result:
        msg="Verified"
    else:
        msg="Eroor Not Verified"
    response={'Verification':msg}
    return jsonify(response)
@app.route('/add_trans',methods=['POST'])
def add_transaction():
    json=request.get_json()
    transaction_keys=['sender','receiver','amount']
    if not all (key in json for key in transaction_keys):
        return "Elements are missing",400
    else:
        index=blockchain.add_trans(json['sender'],json['receiver'],json['amount'])
        response={'message':f'This transactions will be added to Block'}
        return jsonify(response),201

#connecting new node
@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json = request.get_json()       #to get the json file once the user post to us
    
    nodes = json.get("nodes")
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'All the nodes are now connected. The Adicoin Blockchain now contains the following nodes:',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201
@app.route('/replace_chain',methods=['POST']) 
def replace_chain():
    is_chain_replaced=blockchain.replace_chain()
    if is_chain_replaced:
        msg="Node have diffrent node so chain got replaced"
    else:
        msg="Node have same node"
    response={'Verification':msg,
                'chain':blockchain.chain}
    return jsonify(response),200



app.run(host='0.0.0.0',port= 5001,debug=True)
