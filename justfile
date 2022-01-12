TAILWIND_CSS_VERSION := "latest"

@_default:
    just --list

@lint:
    black --check .
    curlylint *.html

@proxy:
    devd --modd -l http://localhost:4000

@serve:
    bundle exec jekyll serve --drafts --watch --port 4000

@static:
    # NODE_ENV=production npm run build
    npx -p tailwindcss@{{ TAILWIND_CSS_VERSION }} tailwindcss build \
    	src/index.css \
    	--config src/tailwind.config.js \
    	--output assets/2022.css

    npx -p tailwindcss@{{ TAILWIND_CSS_VERSION }} tailwindcss build \
    	src/index.css \
    	--config src/tailwind.min.config.js \
    	--output assets/2022.min.css

sync:
    python sync.py sync-cuisines
    # python sync.py sync-cuisines-to-aliases
    python sync.py sync-neighborhoods
    # python sync.py sync-places
    python sync.py sync-schemas

logo:
    curl -o 300.png https://via.placeholder.com/300.png/1A202C/F7FAFC/?text=LFK.im
    curl -o 16.png https://via.placeholder.com/16.png/1A202C/F7FAFC/?text=LFK.im
