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

## Overview

### :newspaper: Website

- [GitHub Pages](https://pages.github.com/) for Hosting
- [Jekyll](https://jekyllrb.com/) for statically building the pages (you can ignore this if you don't run it locally)
- [TailwindCSS](https://tailwindcss.com/) for CSS

### :robot: Automation

- [GitHub Actions](https://github.com/features/actions) for automating Place updates
- [Google Sheets](https://www.google.com/sheets/about/) for collaborating and updating the website
- [Python 3.7](https://www.python.org/) drives our Automation
- [Sheetfu](https://github.com/socialpoint-labs/sheetfu) the library we use to get data from Google Sheets into Python

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

## Random tips

### Automation / GitHub Actions

Our GitHub Actions Workflow which pulls from Google Sheets has to be configured. The script.py was designed to help error in hopefully useful ways. You can skip this step completely if you want and just fork the website and update `_places` which might be the best way to start.

- `LFK_GOOGLE_SHEET_APP_ID` (required)
- `LFK_SHEET_NAME` (optional, defaults to "Sheet1")

These are required by Sheetfu to run. To setup, check out the [Sheetfu Authentication](https://github.com/socialpoint-labs/sheetfu/blob/master/documentation/authentication.rst) which walks you through setting up a free Google Cloud project.

Once your project is created, you you can download a secret.json file which we will turn into a bunch of environment variables. See the "If you want to initialize it from ENV vars" section for a better overview.

**Please note:** Do **not** commit these values in your public GitHub repo. Instead, we will add these as Secrets in our project's Settings.

- `SHEETFU_CONFIG_AUTH_PROVIDER_URL` (required)
- `SHEETFU_CONFIG_AUTH_URI` (required)
- `SHEETFU_CONFIG_CLIENT_CERT_URL` (required)
- `SHEETFU_CONFIG_CLIENT_EMAIL` (required)
- `SHEETFU_CONFIG_CLIENT_ID` (required)
- `SHEETFU_CONFIG_PRIVATE_KEY` (required)
- `SHEETFU_CONFIG_PRIVATE_KEY_ID` (required)
- `SHEETFU_CONFIG_PROJECT_ID` (required)
- `SHEETFU_CONFIG_TOKEN_URI` (required)
- `SHEETFU_CONFIG_TYPE` (required)

**Do not skip this step** Don't forget to give your Google Cloud project permission to access your Google Sheet by inviting email address in your `SHEETFU_CONFIG_CLIENT_EMAIL` or `client_email` from the secrets file to have Read or Write access.

### Optimize your page size

GitHub Pages are easy to work with at the cost of having options over how content is served like compression or HTML, CSS, and JS optimization. I tried to keep the HTML readable vs. using Jekyll/Liquid tricks to compress them.

The workaround is to use a CDN in front of GitHub and to turn these options on. CloudFlare (no affiliation) is my free goto for us tasks and here are the rough steps I used to turn it on:

1. Login to your Cloudflare account (or register an account)
2. Pick your domain (assumes you have already set it up)
3. Slick the Speed app
4. Click the Optimization tab
5. Scroll down to the Auto Minify and check the :white_check_mark: next to HTML. (You may want CSS and JS too, but we already host our CSS via a CDN.)

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
