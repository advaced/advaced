# Currently only tested on garuda-linux (v1.4)
install:
	python3 build
	chmod +rwx /usr/bin/advaced
	chmod +rwx /usr/lib/advaced
	chown 110 /usr/lib/advaced/database
