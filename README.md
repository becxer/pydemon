
##How to install
 
		$ sudo pip install pydemon

##How to use

		$ pydemon yours.py
		or
		$ pydemon 'bash script'
		or
		$ pydemon script.sh

##How to ignore file such as ".swp"

		$ vi .pydemon.dat
		
		add your ignore pattern to "ignore_postfix" like below
		
		{
			"ignore_postfix": [
				".swp", 
				".log"
			],
			"run_count": 16
		}

