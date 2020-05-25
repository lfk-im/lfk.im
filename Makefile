# .PHONY: build
# build: sync
# 	git cia -m ":robot: Update places"
# 	git push origin master

# .PHONY: add
# add: sync
# 	git add _places/
# 	git cia -m ":robot: Update places"
# 	git push origin master

# .PHONY: sync
# sync:
# 	python sync.py

.PHONY: static
static:
 	# @NODE_ENV=production npm run build
	@npx tailwindcss@1.4.6 build \
		src/index.css \
		--config src/tailwind.config.js \
		--output assets/2020.css

	@npx tailwindcss@1.4.6 build \
		src/index.css \
		--config src/tailwind.min.config.js \
		--output assets/2020.min.css
