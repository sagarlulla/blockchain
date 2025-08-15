import datetime as _dt
import hashlib as _hashlib
import json as _json


class Blockchain:
	def __init__(self) -> None:
		self.chain = list()
		genesis_block = self._create_block(index=0, data="i am the genesis block", proof=1, previous_hash="0")
		self.chain.append(genesis_block)
	
	def mine_block(self, data: str) -> dict:
		previous_block = self.get_last_block()
		previous_proof = previous_block["proof"]
		index = len(self.chain)
		proof = self._proof_of_work(index=index, data=data, previous_proof=previous_proof)
		previous_hash = self._hash(block=previous_block)
		block = self._create_block(index=index, data=data, proof=proof, previous_hash=previous_hash)
		self.chain.append(block)
		return block
	
	def _hash(self, block: dict) -> str:
		"""
		Hash a block and return the cryptographic hash of the block
		:param block: dict
		:return: str
		"""
		encoded_block = _json.dumps(block, sort_keys=True).encode()
		return _hashlib.sha512(encoded_block).hexdigest()
	
	def _to_digest(self, index: int, data: str, new_proof: int, previous_proof: int) -> bytes:
		"""
		:param index:
		:param data:
		:param new_proof:
		:param previous_proof:
		:return: bytes
		"""
		# calculate digest based on very complex formula
		to_digest = str(new_proof ** 2 - previous_proof ** 2 + index) + data
		return to_digest.encode()
	
	def _proof_of_work(self, index: int, data: str, previous_proof: int) -> int:
		new_proof = 1
		check_proof = False
		while not check_proof:
			to_digest = self._to_digest(index=index, data=data, new_proof=new_proof, previous_proof=previous_proof)
			hash_value = _hashlib.sha512(to_digest).hexdigest()
			
			if hash_value[:4] == "0000":
				check_proof = True
			else:
				new_proof += 1
		return new_proof
	
	def get_last_block(self) -> dict[int | str]:
		return self.chain[-1]
	
	def _create_block(self, index: int, data: str, proof: int, previous_hash: str) -> dict[int | str]:
		"""
		:param index: int
		:param data: str
		:param proof: int
		:param previous_hash: str
		:return: dict
		"""
		block: dict[int | str] = {
			"index": index,
			"timestamp": str(_dt.datetime.now()),
			"data": data,
			"proof": proof,
			"previous_hash": previous_hash
		}
		return block
	
	def is_chain_valid(self) -> bool:
		previous_block = self.chain[0]
		block_index = 1
		
		while block_index < len(self.chain):
			current_block = self.chain[block_index]
			# Check if the previous hash of the current block is the same as the hash of its previous block
			if current_block["previous_hash"] != self._hash(previous_block):
				return False
			previous_proof = previous_block["proof"]
			current_index, current_data, current_proof = current_block["index"], current_block["data"], current_block["proof"]
			hash_value = _hashlib.sha512(self._to_digest(new_proof=current_proof, previous_proof=previous_proof, index=current_index, data=current_data)).hexdigest()
			
			if hash_value[:4] != "0000":
				return False
			
			previous_block = current_block
			block_index += 1
			
		return True
