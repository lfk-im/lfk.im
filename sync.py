import click
import frontmatter
import os
import sys
import yaml

from click_default_group import DefaultGroup
from pathlib import Path
from sheetfu import SpreadsheetApp, Table
from slugify import slugify
from typesystem.fields import Boolean


Boolean.coerce_values.update({"n": False, "no": False, "y": True, "yes": True})

CUISINE_INITIAL = [
    "American",
    "Asian",
    "Bakeries",
    "Barbecue",
    "Bar & Grill",
    "Breakfast",
    "Breweries",
    "Burgers",
    "Cajun",
    "Chinese",
    "Coffee and Tea",
    "Deli",
    "Ethiopian",
    "Fast Food",
    "Fine Dining",
    "Greek",
    "Homestyle Cookin'",
    "Ice Cream / Juice",
    "Indian",
    "Italian",
    "Japanese",
    "Korean",
    "Latin American",
    "Mexican",
    "Middle-Eastern",
    "Pizza",
    "Sandwiches/Subs",
    "Seafood",
    "Spanish",
    "Steak",
    "Sushi",
    "Thai",
]

# Don't customize these
EXPECTED_ENV_VARS = [
    "LFK_GOOGLE_SHEET_APP_ID",
    "SHEETFU_CONFIG_AUTH_PROVIDER_URL",
    "SHEETFU_CONFIG_AUTH_URI",
    "SHEETFU_CONFIG_CLIENT_CERT_URL",
    "SHEETFU_CONFIG_CLIENT_EMAIL",
    "SHEETFU_CONFIG_CLIENT_ID",
    "SHEETFU_CONFIG_PRIVATE_KEY",
    "SHEETFU_CONFIG_PRIVATE_KEY_ID",
    "SHEETFU_CONFIG_PROJECT_ID",
    "SHEETFU_CONFIG_TOKEN_URI",
    "SHEETFU_CONFIG_TYPE",
]

# Feel free to customie everything below here

SHEETS_BOOL_FIELDS = [
    "active",
    "curbside",
    "delivery",
    "giftcard",
    "takeout",
]

SHEETS_STRING_FIELDS = [
    "name",
    "address",
    "cuisine",
    "curbside_instructions",
    "giftcard_notes",
    "hours",
    "neighborhood",
    "notes",
    "restaurant_phone",
    "social",
]

SHEETS_URL_FIELDS = [
    "giftcard_url",
    "website",
    "delivery_service_websites",
]

FOOD_SERVICE_DICT = {
    # "chownow_url": "ChowNow",
    # "doordash_url": "DoorDash",
    # "eatstreet_url": "EatStreet",
    # "grubhub_url": "Grubhub",
    # "postmates_url": "Postmates",
    # "seamless_url": "Seamless",
    # "ubereats_url": "Ubereats",
    "chownow_url": "chownow.com",
    "doordash_url": "doordash.com",
    "eatstreet_url": "eatstreet.com",
    "grubhub_url": "grubhub.com",
    "postmates_url": "postmates.com",
    "seamless_url": "seamless.com",
    "ubereats_url": "ubereats.com",
}

FOOD_SERVICE_URLS = [
    "chownow_url",
    "doordash_url",
    "eatstreet_url",
    "grubhub_url",
    "postmates_url",
    "seamless_url",
    "ubereats_url",
]


def load_aliases():
    if Path("_data", "aliases.yml").exists():
        input_file = Path("_data", "aliases.yml").read_text()
        data = yaml.load(input_file, Loader=yaml.FullLoader)
    else:
        data = dict()
    return data


def string_to_boolean(value):
    validator = Boolean()
    value, error = validator.validate_or_error(value)

    if value is None:
        return False
    else:
        return value


def verify_http(value):
    if not value or value.startswith("http"):
        return value
    return f"https://{value}"


def print_expected_env_variables():
    click.echo(
        """
To use this command, you will need to setup a Google Cloud Project and have
authentication properly setup. To start, check out:

> https://github.com/socialpoint-labs/sheetfu/blob/master/documentation/authentication.rst

Once you have your your seceret JSON file, you'll want to convert the key/value
pairs in this file into ENV variables or SECRETS if you want to run this script
as a GitHub Action.

These are the values that you need to configure for the script to run:
"""
    )

    for var in EXPECTED_ENV_VARS:
        if var not in os.environ or not os.environ.get(var):
            click.echo(f"- {var}")

    click.echo("")


@click.group(cls=DefaultGroup, default="sync-places", default_if_no_args=True)
def cli():
    pass


@cli.command()
def sync_cuisines():
    click.echo("sync-cuisines")

    aliases = load_aliases()
    cuisine_aliases = aliases["cuisines"]

    data = []
    places = Path("_places").glob("*.md")
    for place in places:
        post = frontmatter.loads(place.read_text())
        cuisines = post["cuisines"]
        if cuisines and len(cuisines):
            data += cuisines

    if not Path("_cuisines").exists():
        Path("_cuisines").mkdir()

    for cuisine in CUISINE_INITIAL:
        cuisine_slug = slugify(cuisine)
        if not Path("_cuisines").joinpath(f"{cuisine_slug}.md").exists():
            post = frontmatter.loads("")
            post["active"] = True
            post["name"] = cuisine
            post["sitemap"] = True
            post["slug"] = cuisine_slug
            try:
                aliases = [
                    alias["aliases"]
                    for alias in cuisine_aliases
                    if cuisine.lower() == alias["name"].lower()
                ][0]
                aliases = [f"/cuisines/{slugify(alias)}/" for alias in aliases]
                post["redirect_from"] = aliases
            except IndexError:
                pass

            Path("_cuisines").joinpath(f"{cuisine_slug}.md").write_text(
                frontmatter.dumps(post)
            )

    data = set(data)

    alias_data = []
    aliases = [alias["aliases"] for alias in cuisine_aliases]
    for alias in aliases:
        alias_data += alias

    for cuisine in data:
        cuisine_slug = slugify(cuisine)
        if cuisine not in alias_data:
            if not Path("_cuisines").joinpath(f"{cuisine_slug}.md").exists():
                post = frontmatter.loads("")
                post["active"] = True
                post["name"] = cuisine
                post["sitemap"] = False
                post["slug"] = cuisine_slug
                # try:
                #     aliases = [
                #         alias["aliases"]
                #         for alias in cuisine_aliases
                #         if cuisine == alias["name"]
                #     ][0]
                #     aliases = [f"/cuisines/{slugify(alias)}/" for alias in aliases]
                #     post["redirect_from"] = aliases
                # except IndexError:
                #     pass

                Path("_cuisines").joinpath(f"{cuisine_slug}.md").write_text(
                    frontmatter.dumps(post)
                )


@cli.command()
def sync_neighborhoods():
    click.echo("sync-neighborhoods")

    aliases = load_aliases()
    neighborhood_aliases = aliases["neighborhoods"]

    data = []
    places = Path("_places").glob("*.md")
    for place in places:
        post = frontmatter.loads(place.read_text())
        neighborhood = post["neighborhood"]
        if neighborhood and len(neighborhood):
            data.append(neighborhood)

    if not Path("_neighborhoods").exists():
        Path("_neighborhoods").mkdir()

    data = set(data)

    for neighborhood in data:
        neighborhood_slug = slugify(neighborhood)
        if not any(
            [alias for alias in neighborhood_aliases if neighborhood in alias["name"]]
        ):
            if not Path("_neighborhoods").joinpath(f"{neighborhood_slug}.md").exists():
                post = frontmatter.loads("")
                post["active"] = True
                post["name"] = neighborhood
                post["sitemap"] = True
                post["slug"] = neighborhood_slug

                Path("_neighborhoods").joinpath(f"{neighborhood_slug}.md").write_text(
                    frontmatter.dumps(post)
                )


@cli.command()
@click.option("--output-folder", default="_places")
@click.option("--sheet-app-id", envvar="LFK_GOOGLE_SHEET_APP_ID")
@click.option("--sheet-name", default="Sheet1", envvar="LFK_SHEET_NAME")
def sync_places(sheet_app_id, output_folder, sheet_name):

    output_folder = Path(output_folder)

    try:
        sa = SpreadsheetApp(from_env=True)
    except AttributeError:
        print_expected_env_variables()
        sys.exit(1)

    try:
        spreadsheet = sa.open_by_id(sheet_app_id)
    except Exception:
        click.echo(
            f"We can't find that 'sheet_app_id'. Please double check that 'LFK_GOOGLE_SHEET_APP_ID' is set. (Currently set to: '{sheet_app_id}')"
        )
        sys.exit(1)

    try:
        sheet = spreadsheet.get_sheet_by_name(sheet_name)
    except Exception:
        click.echo(
            f"We can't find that 'sheet_name' aka the tab. Please double check that 'LFK_SHEET_NAME' is set. (Currently set to: '{sheet_name}')"
        )
        sys.exit(1)

    # returns the sheet range that contains data values.
    data_range = sheet.get_data_range()

    table = Table(data_range, backgrounds=True)

    for item in table:
        name = item.get_field_value("name")
        address = item.get_field_value("address")
        slug = slugify(" ".join([name, address]))
        filename = f"{slug}.md"

        input_file = output_folder.joinpath(filename)
        if input_file.exists():
            post = frontmatter.load(input_file)
        else:
            post = frontmatter.loads("")

        place = {}
        place["sitemap"] = False
        place["slug"] = slug

        # Our goal is to build a Place record without having to deal with
        # annoying errors if a field doesn't exist. We will still let you
        # know which field wasn't there though.

        if SHEETS_BOOL_FIELDS:
            for var in SHEETS_BOOL_FIELDS:
                try:
                    place[var] = string_to_boolean(item.get_field_value(var))
                except ValueError:
                    click.echo(f"A column named '{var}' was expected, but not found.")

        if SHEETS_STRING_FIELDS:
            for var in SHEETS_STRING_FIELDS:
                try:
                    place[var] = item.get_field_value(var)
                except ValueError:
                    click.echo(f"A column named '{var}' was expected, but not found.")

        if SHEETS_URL_FIELDS:
            for var in SHEETS_URL_FIELDS:
                try:
                    place[var] = verify_http(item.get_field_value(var))
                except ValueError:
                    click.echo(f"A column named '{var}' was expected, but not found.")

        food_urls = []

        if "cuisine" in place and len(place["cuisine"]):
            place["cuisines"] = [
                cuisine.strip() for cuisine in place["cuisine"].split(",")
            ]
        else:
            place["cuisines"] = None

        if place["cuisines"] and len(place["cuisines"]):
            place["cuisine_slugs"] = [slugify(cuisine) for cuisine in place["cuisines"]]
        else:
            place["cuisine_slugs"] = None

        if "neighborhood" in place and len(place["neighborhood"]):
            place["neighborhood_slug"] = slugify(place["neighborhood"])

        if "delivery_service_websites" in place and len(
            place["delivery_service_websites"]
        ):
            food_urls.append(
                {"name": "order online", "url": place["delivery_service_websites"]}
            )

        if FOOD_SERVICE_URLS:
            for var in FOOD_SERVICE_URLS:
                try:
                    value = verify_http(item.get_field_value(var))
                    if len(value):
                        food_urls.append(
                            {"name": FOOD_SERVICE_DICT.get(var), "url": value}
                        )
                except ValueError:
                    click.echo(f"A column named '{var}' was expected, but not found.")

            place["food_urls"] = [food_url for food_url in food_urls if food_url]

        post.content = item.get_field_value("notes")

        post.metadata.update(place)

        input_file.write_text(frontmatter.dumps(post))


if __name__ == "__main__":
    cli()
