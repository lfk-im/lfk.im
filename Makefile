# .PHONY: build
# build: sync
# 	git cia -m ":robot: Update places"
# 	git push origin main

# .PHONY: add
# add: sync
# 	git add _places/
# 	git cia -m ":robot: Update places"
# 	git push origin main

# .PHONY: sync
# sync:
# 	python sync.py

.PHONY: static
static:
 	# @NODE_ENV=production npm run build
	@npx tailwindcss@1.8.7 build \
		src/index.css \
		--config src/tailwind.config.js \
		--output assets/2020.css

	@npx tailwindcss@1.8.7 build \
		src/index.css \
		--config src/tailwind.min.config.js \
		--output assets/2020.min.css


.PHONY: sync
sync:
	@python sync.py sync-cuisines --overwrite
# 	@python sync.py sync-cuisines-to-aliases --overwrite
	@python sync.py sync-neighborhoods --overwrite
# 	@python sync.py sync-places --overwrite
	@python sync.py sync-schemas --overwrite


.PHONY: logo
logo:
	curl -o 300.png https://via.placeholder.com/300.png/1A202C/F7FAFC/?text=LFK.im
	curl -o 16.png https://via.placeholder.com/16.png/1A202C/F7FAFC/?text=LFK.im
