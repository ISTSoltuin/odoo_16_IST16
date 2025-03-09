# token_generator/models/token_generator.py

from odoo import models, fields, api
import logging
from web3 import Web3
import os

_logger = logging.getLogger(__name__)

GANACHE_URL = os.getenv('GANACHE_URL', 'HTTP://209.145.61.30:7545')
PRIVATE_KEY = 'YOUR_PRIVATE_KEY'  # Substitua pelo valor da sua chave privada do Ganache
ACCOUNT_ADDRESS = 'YOUR_ACCOUNT_ADDRESS'  # Substitua pelo endereço da sua conta do Ganache

class TokenGenerator(models.Model):
    _name = 'token.generator'
    _description = 'Token Generator'

    name = fields.Char('Name')
    token_count = fields.Integer('Token Count')

    def generate_tokens(self):
        token_count = self.token_count
        _logger.info(f'Generating {token_count} fake tokens')

        # Conectar ao Ganache
        web3 = Web3(Web3.HTTPProvider(GANACHE_URL))
        if not web3.isConnected():
            _logger.error('Could not connect to Ganache')
            return False

        # ABI e bytecode do contrato (exemplo de um contrato ERC20)
        abi = [...]
        bytecode = '0x...'

        # Preparar o contrato
        TokenContract = web3.eth.contract(abi=abi, bytecode=bytecode)

        # Estimar o gás necessário para a implantação do contrato
        tx_hash = TokenContract.constructor().buildTransaction({
            'from': ACCOUNT_ADDRESS,
            'nonce': web3.eth.getTransactionCount(ACCOUNT_ADDRESS),
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei')
        })

        signed_tx = web3.eth.account.signTransaction(tx_hash, PRIVATE_KEY)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

        tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        contract_address = tx_receipt.contractAddress
        _logger.info(f'Token contract deployed at {contract_address}')

        # Interagir com o contrato para gerar tokens
        token_contract = web3.eth.contract(address=contract_address, abi=abi)
        tx_hash = token_contract.functions.mint(ACCOUNT_ADDRESS, token_count).buildTransaction({
            'from': ACCOUNT_ADDRESS,
            'nonce': web3.eth.getTransactionCount(ACCOUNT_ADDRESS) + 1,
            'gas': 200000,
            'gasPrice': web3.toWei('50', 'gwei')
        })

        signed_tx = web3.eth.account.signTransaction(tx_hash, PRIVATE_KEY)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        web3.eth.waitForTransactionReceipt(tx_hash)
        _logger.info(f'{token_count} tokens generated')

        return True
