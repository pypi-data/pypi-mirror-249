from solders.instruction import Instruction
from solders.pubkey import Pubkey

ID: Pubkey

def request_heap_frame(bytes_: int) -> Instruction: ...
def set_compute_unit_limit(units: int) -> Instruction: ...
def set_compute_unit_price(micro_lamports: int) -> Instruction: ...
