import json
import multiprocessing

from wallet_explorer import WalletExplorer
from blockchain_info import BlockchainInfo
import _thread

import time

if __name__ == '__main__':
  waller_explorer = WalletExplorer()
  blockchain = BlockchainInfo()

  # Create process as follows
  try:
    multiprocessing.Process(target=blockchain.read_links).start()
    with open('wallet_explorer_tags.json', 'r') as f:
      json_data = json.load(f)
    for json_tag in json_data:
      multiprocessing.Process(target=waller_explorer.read_links, args=(json_tag,)).start()
  except Exception as e:
    print("Error: unable to start thread", e)
  while 1:
    pass
