import uvicorn
import fastapi as _fastapi
import blockchain as _blockchain

blockchain = _blockchain.Blockchain()
app = _fastapi.FastAPI()


# endpoint to mine a block
@app.post(path="/mine_block")
def mine_block(data: str):
        if not blockchain.is_chain_valid():
                return _fastapi.HTTPException(status_code=400, detail="Blockchain is invalid!")
        block = blockchain.mine_block(data=data)
        return block


# endpoint to return a entire blockchain
@app.get(path="/blockchain")
def get_blockchain():
        if not blockchain.is_chain_valid():
                return _fastapi.HTTPException(status_code=400, detail="Blockchain is invalid!")
        
        chain = blockchain.chain
        return chain


# endpoint returns last block
@app.get(path="/blockchain/last")
def last_block():
        if not blockchain.is_chain_valid():
                return _fastapi.HTTPException(status_code=400, detail="Blockchain is invalid!")
        return blockchain.get_last_block()

# endpoint to see if the blockchain is valid
@app.get(path="/validate")
def is_blockchain_valid():
        return blockchain.is_chain_valid()


if __name__ == "__main__":
        uvicorn.run(app=app, port=8000)
