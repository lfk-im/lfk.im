<h1 align="center">Welcome to lfk.im 👋</h1>
<p>
  <a href="#" target="_blank">
    <img alt="License: BSD" src="https://img.shields.io/badge/License-BSD-yellow.svg" />
  </a>
  <a href="https://twitter.com/webology" target="_blank">
    <img alt="Twitter: webology" src="https://img.shields.io/twitter/follow/webology.svg?style=social" />
  </a>
</p>

> I built LFK.im over the course of a day to help people figure out which restaurants were open and what their options for ordering food are in Lawrence, Kansas.
>
> Our workflow involves using a Google Sheet to build a database of local businesses along with their hours and contact information.
>
> We started off using a Python script to access this database and save them as Jekyll-friendly frontmatter/markdown files. See the `_places` folder for how this is structured.
>
> After my running this script became a bottleneck, I created an GitHub Action which runs this script every 15-minutes or after ever update to the website.

### 🏠 [Homepage](https://lfk.im)

## Usage

The lfk.im website runs on GitHub Pages using Jekyll.

To run the website locally, you'll want to run:

```shell
$ bundle install
$ jekyll serve --watch
```

Then check the website out at http://localhost:4000/

### Setting up the Python Sync

Create a virtualenv using your method of choice.

```shell
$ python -m pip install -r requirements.txt

# to run, but except it to fail on your first run:
$ python sync.py
```

When you run `sync.py`, it will walk you through which ENV variables that you need to setup to sync your Google Sheet locally.

## Author

👤 **Jeff Triplett**

* Website: https://jefftriplett.com
* Twitter: [@webology](https://twitter.com/webology)
* Github: [@jefftriplett](https://github.com/jefftriplett)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/jefftriplett/lfk.im/issues).

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
