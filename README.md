**The Coin Harvester**

**For harversting used private keys on multiple chains from a private key dictionary**

![image](https://github.com/0x6679/coinHarvester/assets/43137410/aa0aae7f-f4db-4c7d-af76-0f1e71de65b8)

Have you ever felt the urge to decentralise the funds within other individuals' wallets, alongside the rightful owners? 
If so, I have some exciting news for you! Allow me to introduce the coinHarvester.

1/ This remarkable tool takes the hex private keys stored in the 'hex_privKeys.txt' file. (already added a few example to the file)

2/ It generates corresponding addresses based on each coin's standard and subsequently verifies them if these addresses have been ever used.

3/ The program then proceeds to save the used addresses in the balance folder.

4/ Profit $$$$$ (khmm....) ₿₿₿₿₿₿₿

**Currently supporting 5 chains:**

	-Bitcoin
	-Ethereum
	-BinanceChain
	-Polygon
	-Avalanche

**Work in progress:**

	-Litecoin
	-Bitcoin Cash
	-Doge

**To install the requirements:**

	pip install -r requirements.txt

**Usage:**

	python coinHarvester.py

**You can easily add your own flavor of diamond supply chain if its compatible with (= a cheap copy of)  Ethereum**

Fork it, before it forks you!

**Instructions:**

	1/ Open up the RPC folder and create a new file specifically for the coin you intend to add.
	
	2/ Obtain the RPCs for your desired currency and copy them into the created file, with each listed on a separate line.
	
	3/ Open the coinHarvester code and include the following line beneath the existing RPCs:

		YourCoin_rpc = [x.replace('\n','') for x in open('./RPC/YourCoin.txt','r')]

	4/ Scroll down to the bottom of the code and expand it by adding the following:

		YourCoin = threading.Thread(target=Ethereum_a_like_scraper, args=(privKeys, YourCoin_rpc, 'YourCoin',colour_purple, ))
		
		YourCoin.start()
		
		YourCoin.join()

	Bada-bim bada-bum - your coin is added to the script

**if you like the project please consider to sell your house and transfer the founds to the following address:**

	bc1qy2vl8mwxtfld2xyjl54k2l23pzjnj9v7fjvxve
	
thx




