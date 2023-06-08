from web3 import Web3
from eth_account import Account
import urllib.request
import hashlib
import base58
import codecs
import ecdsa
import binascii
import threading


privKeys = open('hex_privKeys.txt','r')

ETH_rpc = [x.replace('\n','') for x in open('./RPC/Ethereum.txt','r')]
BSC_rpc = [x.replace('\n','') for x in open('./RPC/BinanceChain.txt','r')]
Polygon_rpc = [x.replace('\n','') for x in open('./RPC/Polygon.txt','r')]
Avax_rpc = [x.replace('\n','') for x in open('./RPC/Avalanche.txt','r')]


def priv2add_Bitcoin(x):
    try:
        private_key = x.replace('\n',"").replace(' ',"")
        private_key_bytes = codecs.decode(private_key, 'hex')
        public_key_raw = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
        public_key_bytes = public_key_raw.to_string()
        public_key_hex = codecs.encode(public_key_bytes, 'hex')
        public_key = (b'04' + public_key_hex).decode("utf-8")
        if (ord(bytearray.fromhex(public_key[-2:])) % 2 == 0):
            public_key_compressed = '02'
        else:
            public_key_compressed = '03'
        public_key_compressed += public_key[2:66]
        hex_str = bytearray.fromhex(public_key_compressed)
        sha = hashlib.sha256()
        sha.update(hex_str)
        rip = hashlib.new('ripemd160')
        rip.update(sha.digest())
        key_hash = rip.hexdigest()
        modified_key_hash = "00" + key_hash
        sha = hashlib.sha256()
        hex_str = bytearray.fromhex(modified_key_hash)
        sha.update(hex_str)
        sha_2 = hashlib.sha256()
        sha_2.update(sha.digest())
        checksum = sha_2.hexdigest()[:8]
        byte_25_address = modified_key_hash + checksum
        address = base58.b58encode(bytes(bytearray.fromhex(byte_25_address))).decode('utf-8')
        return address
    except:
        pass


def convert_Bitcoin_privkey_hex2wif(z):

    private_key_static = z
    extended_key = "80"+private_key_static+"01"
    first_sha256 = hashlib.sha256(binascii.unhexlify(extended_key)).hexdigest()
    second_sha256 = hashlib.sha256(binascii.unhexlify(first_sha256)).hexdigest()
    final_key = extended_key+second_sha256[:8]
    WIF = base58.b58encode(binascii.unhexlify(final_key)).decode('ascii')
    return WIF

def convert_Litecoin_privkey_hex2wif(z):

    private_key_static = z
    extended_key = "B0"+private_key_static+"01"
    first_sha256 = hashlib.sha256(binascii.unhexlify(extended_key)).hexdigest()
    second_sha256 = hashlib.sha256(binascii.unhexlify(first_sha256)).hexdigest()
    final_key = extended_key+second_sha256[:8]
    WIF = base58.b58encode(binascii.unhexlify(final_key)).decode('ascii')
    return WIF

def convert_Doge_privkey_hex2wif(z):

    private_key_static = z
    extended_key = "9E"+private_key_static+"01"
    first_sha256 = hashlib.sha256(binascii.unhexlify(extended_key)).hexdigest()
    second_sha256 = hashlib.sha256(binascii.unhexlify(first_sha256)).hexdigest()
    final_key = extended_key+second_sha256[:8]
    WIF = base58.b58encode(binascii.unhexlify(final_key)).decode('ascii')
    return WIF



def Bitcoin_scraper(privKeys,pk_type,colour):

    count=0

    for x in privKeys:
        try:
            count+=1

            key = x.replace('\n','').replace(' ','')
            add = priv2add_Bitcoin(key)
            contents = urllib.request.urlopen("https://blockchain.info/q/getreceivedbyaddress/" + str (add)).read()

            print (colour + 'Biction address Checked : ' + str(add.replace('\n','')) + colour_red + ' : Total Balance = ' + str(contents.decode('UTF8')))
            print (colour_cyan+'PrivKey : ' + str (key) + " Scan Number" + ' : ' + str (count) )

            if int(contents) > 0:

                print (colour_yellow + 'Used Wallet Found : ' + colour_reset + str (add) + colour_green + ' : Balance : ' + str(contents.decode('UTF8')) + colour_reset)
                f=open("./Wallets/bitcoin_wallets.txt","a")

                if pk_type == 'hex':

                    f=open(u"Bitcoin_wallets.txt","a")
                    f.write(key+'\n')
                    f.close()

                if pk_type == 'wif':

                    f.write(convert_Bitcoin_privkey_hex2wif(key)+'\n')
                    f.close()                    
        except:
            pass



def Ethereum_a_like_scraper(privKeys,rpc_list,coin,colour):

    web3 = Web3(Web3.HTTPProvider(rpc_list[0]))

    rpcRotator = 0
    count = 0

    for x in privKeys:

        try:
            priv = x.replace('\n','').replace(' ','')
            private_key = "0x" + priv
            acct = Account.from_key(priv)
            wallet_address = acct.address

            pkCheck = True

        except:
            print('key error: '+x)
            pkCheck = False

        if pkCheck == True:

            try:
 
                print(colour +coin+' address Checked : '+wallet_address +colour_yellow+' : Total Balance = '+ str(web3.eth.get_balance(wallet_address)) ) 
                print (colour_cyan+'PrivKey : ' + private_key + ' Scan Number : ' + str (count) )
                count += 1

                if str(web3.eth.get_balance(wallet_address)) != '0':
                    print('saved')
                    print(colour_yellow +'Wallet address: '+wallet_address +colour_yellow+' Balance: '+ str(web3.eth.get_balance(wallet_address))+colour_yellow+' PrivateKey: '+x ) 
                    f = open(u'./Wallets/'+coin+"_wallets.txt","a")
                    f.write( private_key +'\n')
                    f.close()



            except:

                rpcRotator += 1
                print('RPC ERROR - Switching to a new one')
                web3 = Web3(Web3.HTTPProvider(rpc_list[rpcRotator%len(rpc_list)]))
                print('new RPC block Height: ' +str(web3.eth.block_number))

        else:
            pass

colour_blue = '\033[94m'
colour_cyan = '\033[36m'
colour_reset = '\033[0;0;39m'
colour_red = '\033[31m'
colour_green='\033[0;32m'
colour_yellow='\033[0;33m'
colour_purple='\033[0;35m'
colour_white='\033[0;37;40m'

if __name__ == "__main__":

    btc = threading.Thread(target=Bitcoin_scraper, args=(privKeys, 'wif',colour_red, ))
    btc.start()
    eth = threading.Thread(target=Ethereum_a_like_scraper, args=(privKeys, ETH_rpc, 'Ethereum',colour_white, ))
    eth.start()
    bsc = threading.Thread(target=Ethereum_a_like_scraper, args=(privKeys, BSC_rpc, 'BinanceChain',colour_yellow, ))
    bsc.start()
    matic = threading.Thread(target=Ethereum_a_like_scraper, args=(privKeys, Polygon_rpc, 'Polygon',colour_green, ))
    matic.start()
    avax = threading.Thread(target=Ethereum_a_like_scraper, args=(privKeys, Avax_rpc, 'Avax',colour_purple, ))
    avax.start()

    btc.join()
    eth.join()
    bsc.join()
    matic.join()
    avax.join()




    



    
