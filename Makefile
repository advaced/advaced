# Currently only tested on garuda-linux (v1.4)
install:
	python3 build
	chmod +rwx /usr/bin/advaced
	chmod +rwx /usr/lib/advaced
	chmod 777 /usr/lib/advaced/database
	chmod 777 /usr/lib/advaced/database/db.db
