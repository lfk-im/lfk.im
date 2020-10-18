# import inflection
import frontmatter
import os
import requests
import typer
import typesystem
import yaml


from bs4 import BeautifulSoup
from pathlib import Path
from sheetfu import SpreadsheetApp, Table
from slugify import slugify
from typesystem.fields import Boolean


Boolean.coerce_values.update({"n": False, "no": False, "y": True, "yes": True})

STOPWORDS = ["the"]

CUISINE_INITIAL = [
    "American",
    "Asian",
    "Bakeries",
    "Bar & Grill",
    "Barbecue",
    "Bars",
    "Breakfast",
    "Breweries",
    "Burgers",
    "Butcher",
    "Cajun",
    "Chinese",
    "Coffee and Tea",
    "Deli",
    "Desserts",
    "Ethiopian",
    "Fast Food",
    "Fine Dining",
    "Fried Chicken",
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
    "Steakhouse",
    "Sushi",
    "Thai",
]

CUISINE_INITIAL_SLUGS = [
    slugify(cuisine, stopwords=STOPWORDS) for cuisine in CUISINE_INITIAL
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
    "dinein",
    "featured",
    "giftcard",
    "perma_closed",
    "takeout",
]

SHEETS_STRING_FIELDS = [
    "name",
    "address",
    "place_type",
    "cuisine",
    "curbside_instructions",
    "giftcard_notes",
    "hours",
    "locality",
    "neighborhood",
    "notes",
    "region",
    "restaurant_phone",
]

SHEETS_URL_FIELDS = [
    "delivery_service_websites",
    "facebook_url",
    "giftcard_url",
    "instagram_url",
    "twitch_url",
    "twitter_url",
    "website",
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


class Url(typesystem.Schema):
    name = typesystem.String()
    url = typesystem.String()


class Cuisine(typesystem.Schema):
    active = typesystem.Boolean(default=True)
    aliases = typesystem.Array(
        allow_null=True, default=list, items=typesystem.String(allow_blank=True)
    )
    description = typesystem.String(allow_blank=True)
    name = typesystem.String()
    redirect_from = typesystem.Array(
        allow_null=True, default=list, items=typesystem.String(allow_blank=True)
    )
    sitemap = typesystem.Boolean(default=True)
    slug = typesystem.String()
    title = typesystem.String(allow_blank=True)


class Neighborhood(typesystem.Schema):
    active = typesystem.Boolean(default=True)
    name = typesystem.String()
    sitemap = typesystem.Boolean(default=True)
    slug = typesystem.String()
    title = typesystem.String()


class Place(typesystem.Schema):
    active = typesystem.Boolean()
    address = typesystem.String(allow_null=True)
    cuisine = typesystem.String(allow_null=True)
    cuisine_slugs = typesystem.Array(
        allow_null=True, items=typesystem.String(allow_null=True)
    )
    cuisines = typesystem.Array(
        allow_null=True, items=typesystem.String(allow_null=True)
    )
    curbside = typesystem.Boolean(default=False)
    curbside_instructions = typesystem.String(allow_null=True)
    delivery = typesystem.Boolean(default=False)
    delivery_service_websites = typesystem.String(allow_null=True)
    dinein = typesystem.Boolean(default=False)
    facebook_url = typesystem.String(allow_null=True)
    featured = typesystem.Boolean(default=False)
    food_urls = typesystem.Array(
        allow_null=True, items=typesystem.Reference(allow_null=True, to=Url)
    )
    giftcard = typesystem.Boolean(default=False)
    giftcard_notes = typesystem.String(allow_null=True)
    giftcard_url = typesystem.String(allow_null=True)
    hours = typesystem.String(allow_null=True)
    instagram_url = typesystem.String(allow_null=True)
    locality = typesystem.String(
        allow_null=True
    )  # set default to a variable like "Lawrence"
    name = typesystem.String()
    neighborhood = typesystem.String(allow_null=True)
    neighborhood_slug = typesystem.String(allow_null=True)
    notes = typesystem.String(allow_blank=True)
    perma_closed = typesystem.Boolean(allow_null=True)
    place_type = typesystem.String(allow_null=True)
    region = typesystem.String(allow_null=True)
    restaurant_phone = typesystem.String(allow_null=True)
    sitemap = typesystem.Boolean()
    slug = typesystem.String()
    takeout = typesystem.Boolean(default=False)
    twitch_url = typesystem.String(allow_null=True)
    twitter_url = typesystem.String(allow_null=True)
    website = typesystem.String(allow_null=True)


class Schema(typesystem.Schema):
    active = typesystem.Boolean(default=True)
    name = typesystem.String()
    sitemap = typesystem.Boolean(default=False)
    slug = typesystem.String()
    title = typesystem.String()


app = typer.Typer()


def load_aliases():
    if Path("_data", "aliases.yml").exists():
        input_file = Path("_data", "aliases.yml").read_text()
        data = yaml.load(input_file, Loader=yaml.FullLoader)
    else:
        data = dict()
    return data


def aliases_to_cuisine():
    aliases = load_aliases()

    data = {}
    cuisines = aliases["cuisines"]
    for cuisine in cuisines:
        cuisine_aliases = cuisine["aliases"]
        if len(cuisine_aliases):
            for cuisine_alias in cuisine_aliases:
                data[cuisine_alias] = cuisine["name"]
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
    typer.echo(
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
            typer.echo(f"- {var}")

    typer.echo("")


@app.command()
def sync_cuisines_to_aliases():
    typer.secho("sync-cuisines-to-aliases", fg="yellow")

    aliases = load_aliases()
    cuisine_aliases = aliases["cuisines"]

    data = []
    places = Path("_places").glob("*.md")
    for place in places:
        post = frontmatter.loads(place.read_text())
        cuisines = post["cuisines"]
        if cuisines and len(cuisines):
            data += cuisines

    for cuisine in CUISINE_INITIAL:
        cuisine_slug = slugify(cuisine, stopwords=STOPWORDS)
        if not any(
            [True for alias in cuisine_aliases if cuisine_slug == alias["name"].lower()]
        ):
            aliases["cuisines"].append({"name": cuisine_slug, "aliases": list()})

    data = set([slugify(item, stopwords=STOPWORDS) for item in data])
    unknown_cuisines = []
    for cuisine in data:
        if not any([True for alias in cuisine_aliases if cuisine in alias["aliases"]]):
            if cuisine not in CUISINE_INITIAL_SLUGS:
                unknown_cuisines.append(cuisine)

    aliases["unknown-cuisines"] = list()
    aliases["unknown-cuisines"].append(
        {"name": "unknown-cuisines", "aliases": unknown_cuisines}
    )

    Path("_data", "aliases.yml").write_text(yaml.dump(aliases))


@app.command()
def sync_cuisines(output_folder: str = "_cuisines"):
    typer.secho("sync-cuisines", fg="yellow")

    aliases = load_aliases()
    cuisine_aliases = aliases["cuisines"]

    data = []
    places = Path("_places").glob("*.md")
    for place in places:
        post = frontmatter.loads(place.read_text())
        cuisines = post["cuisines"]
        if cuisines and len(cuisines):
            data += cuisines

    output_folder = Path(output_folder)
    if not output_folder.exists():
        output_folder.mkdir()

    for cuisine in CUISINE_INITIAL:
        cuisine_slug = slugify(cuisine, stopwords=STOPWORDS)

        input_file = output_folder.joinpath(f"{cuisine_slug}.md")

        if input_file.exists():
            post = frontmatter.load(input_file)
        else:
            post = frontmatter.loads("")
            post["active"] = True
            post[
                "description"
            ] = f"{cuisine} restaurants offering curbside, takeout, and delivery food in Lawrence, Kansas"
            post["name"] = cuisine
            post["sitemap"] = True
            post["slug"] = cuisine_slug

            if cuisine.endswith("s"):
                post["title"] = f"{cuisine} in Lawrence, Kansas"
            else:
                post["title"] = f"{cuisine} Restaurants in Lawrence, Kansas"

            try:
                aliases = [
                    alias["aliases"]
                    for alias in cuisine_aliases
                    if cuisine_slug == alias["name"].lower()
                ][0]
                redirect_from = [
                    f"/cuisines/{slugify(alias, stopwords=STOPWORDS)}/"
                    for alias in aliases
                ]
                post["aliases"] = aliases
                post["redirect_from"] = redirect_from
            except IndexError:
                pass

        typer.echo(dict(Cuisine.validate(post.metadata)))

        input_file.write_text(frontmatter.dumps(post))

    data = set(data)

    alias_data = []
    aliases = [alias["aliases"] for alias in cuisine_aliases]
    for alias in aliases:
        alias_data += alias

    for cuisine in data:
        cuisine_slug = slugify(cuisine, stopwords=STOPWORDS)
        if cuisine.lower() not in alias_data:
            input_file = output_folder.joinpath(f"{cuisine_slug}.md")

            if input_file.exists():
                post = frontmatter.loads(input_file.read_text())
                obj = Cuisine.validate(post.metadata)
            else:
                post = frontmatter.loads("")
                post["name"] = cuisine
                post["slug"] = cuisine_slug
                obj = Cuisine.validate(post.metadata)

            typer.echo(dict(obj))
            post.metadata.update(dict(obj))
            input_file.write_text(frontmatter.dumps(post))


@app.command()
def sync_neighborhoods(output_folder: str = "_neighborhoods"):
    typer.secho("sync-neighborhoods", fg="yellow")

    aliases = load_aliases()
    neighborhood_aliases = aliases.get("neighborhoods", list())

    data = []
    places = Path("_places").glob("*.md")
    for place in places:
        post = frontmatter.loads(place.read_text())
        neighborhood = post["neighborhood"]
        if neighborhood and len(neighborhood):
            data.append(neighborhood)

    output_folder = Path(output_folder)
    if not output_folder.exists():
        output_folder.mkdir()

    data = set(data)

    for neighborhood in data:
        neighborhood_slug = slugify(neighborhood, stopwords=STOPWORDS)
        input_file = output_folder.joinpath(f"{neighborhood_slug}.md")

        if not any(
            [alias for alias in neighborhood_aliases if neighborhood in alias["name"]]
        ):

            if input_file.exists():
                post = frontmatter.loads(input_file.read_text())
                obj = Neighborhood.validate(post.metadata)
            else:
                post = frontmatter.loads("")
                post["name"] = neighborhood
                post["slug"] = neighborhood_slug
                post["title"] = f"{neighborhood} Restaurants"
                obj = Neighborhood.validate(post.metadata)

            typer.echo(dict(obj))
            post.metadata.update(dict(obj))
            input_file.write_text(frontmatter.dumps(post))


@app.command()
def sync_places(
    output_folder: str = "_places",
    sheet_app_id: str = typer.Argument(default="", envvar="LFK_GOOGLE_SHEET_APP_ID"),
    sheet_name: str = typer.Argument(default="", envvar="LFK_SHEET_NAME"),
):
    typer.secho("sync-places", fg="yellow")

    output_folder = Path(output_folder)
    cuisine_aliases = aliases_to_cuisine()

    aliases = load_aliases()
    try:
        unknown_cuisines = aliases["unknown-cuisines"][0]["aliases"]
    except:
        unknown_cuisines = None

    try:
        sa = SpreadsheetApp(from_env=True)
    except AttributeError:
        print_expected_env_variables()
        raise typer.Exit()

    try:
        spreadsheet = sa.open_by_id(sheet_app_id)
    except Exception:
        typer.echo(
            f"We can't find that 'sheet_app_id'. Please double check that 'LFK_GOOGLE_SHEET_APP_ID' is set. (Currently set to: '{sheet_app_id}')"
        )
        raise typer.Exit()

    try:
        sheet = spreadsheet.get_sheet_by_name(sheet_name)
    except Exception:
        typer.echo(
            f"We can't find that 'sheet_name' aka the tab. Please double check that 'LFK_SHEET_NAME' is set. (Currently set to: '{sheet_name}')"
        )
        raise typer.Exit()

    # returns the sheet range that contains data values.
    data_range = sheet.get_data_range()

    table = Table(data_range, backgrounds=True)

    for item in table:
        name = item.get_field_value("name")
        address = item.get_field_value("address")
        neighborhood = item.get_field_value("neighborhood")
        slug = slugify(" ".join([name, neighborhood or address]), stopwords=STOPWORDS)
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
                    typer.echo(f"A column named '{var}' was expected, but not found.")

        if SHEETS_STRING_FIELDS:
            for var in SHEETS_STRING_FIELDS:
                try:
                    place[var] = item.get_field_value(var)
                except ValueError:
                    typer.echo(f"A column named '{var}' was expected, but not found.")

        if SHEETS_URL_FIELDS:
            for var in SHEETS_URL_FIELDS:
                try:
                    place[var] = verify_http(item.get_field_value(var))
                except ValueError:
                    typer.echo(f"A column named '{var}' was expected, but not found.")

        food_urls = []

        if "cuisine" in place and len(place["cuisine"]):
            place["cuisines"] = [
                cuisine.strip() for cuisine in place["cuisine"].split(",")
            ]
            if unknown_cuisines:
                place["cuisines"] = [
                    cuisine
                    for cuisine in place["cuisines"]
                    if slugify(cuisine, stopwords=STOPWORDS) not in unknown_cuisines
                ]

        else:
            place["cuisines"] = None

        if place["cuisines"] and len(place["cuisines"]):
            place["cuisine_slugs"] = []
            for cuisine in place["cuisines"]:
                cuisine_slug = slugify(cuisine, stopwords=STOPWORDS)
                place["cuisine_slugs"].append(cuisine_slug)
                if (
                    cuisine_slug in cuisine_aliases
                    and cuisine_aliases[cuisine_slug] not in place["cuisine_slugs"]
                ):
                    place["cuisine_slugs"].append(cuisine_aliases[cuisine_slug])

        else:
            place["cuisine_slugs"] = None

        if "neighborhood" in place and len(place["neighborhood"]):
            place["neighborhood_slug"] = slugify(
                place["neighborhood"], stopwords=STOPWORDS
            )

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
                    typer.echo(f"A column named '{var}' was expected, but not found.")

            place["food_urls"] = [food_url for food_url in food_urls if food_url]

        post.content = item.get_field_value("notes")

        post.metadata.update(place)

        typer.echo(dict(Place.validate(post.metadata)))

        input_file.write_text(frontmatter.dumps(post))


@app.command()
def sync_schemas(output_folder: str = "_schemas"):
    typer.secho("sync-schemas", fg="yellow")

    schemas = []

    # cache place.place_types to build our schemas
    places = Path("_places").glob("*.md")
    for place in places:
        post = frontmatter.loads(place.read_text())
        place_type = post["place_type"]
        schemas.append(place_type)

    output_folder = Path(output_folder)
    if not output_folder.exists():
        output_folder.mkdir()

    schemas = set(schemas)
    schemas = sorted(schemas)

    for schema in schemas:
        # print(inflection.pluralize(inflection.titleize(schema)))
        # print(slugify(inflection.tableize(schema), stopwords=STOPWORDS))
        schema_slug = slugify(schema, stopwords=STOPWORDS)
        input_file = Path("_schemas").joinpath(f"{schema_slug}.md")

        if input_file.exists():
            post = frontmatter.loads(input_file.read_text())
            obj = Schema.validate(post.metadata)
        else:
            post = frontmatter.loads("")
            post["name"] = schema
            post["slug"] = schema_slug
            post["title"] = f"{schema} Businesses"
            obj = Schema.validate(post.metadata)

        typer.echo(dict(obj))
        post.metadata.update(dict(obj))
        input_file.write_text(frontmatter.dumps(post))


if __name__ == "__main__":
    app()
