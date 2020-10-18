TAILWIND_CSS_VERSION := 1.8.10


.PHONY: lint
lint:
	@black --check .
	@curlylint *.html


.PHONY: proxy
proxy:
	devd --modd -l http://localhost:4000


.PHONY: serve
serve:
	bundle exec jekyll serve --drafts --watch --port 4000


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
	@python sync.py sync-cuisines
# 	@python sync.py sync-cuisines-to-aliases
	@python sync.py sync-neighborhoods
# 	@python sync.py sync-places
	@python sync.py sync-schemas


.PHONY: logo
logo:
	curl -o 300.png https://via.placeholder.com/300.png/1A202C/F7FAFC/?text=LFK.im
	curl -o 16.png https://via.placeholder.com/16.png/1A202C/F7FAFC/?text=LFK.im
