import click
import frontmatter
import os
import sys

from pathlib import Path
from sheetfu import SpreadsheetApp, Table
from slugify import slugify
from typesystem.fields import Boolean


Boolean.coerce_values.update({"n": False, "no": False, "y": True, "yes": True})


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


@click.command()
@click.option("--output-folder", default="_places")
@click.option("--sheet-app-id", envvar="LFK_GOOGLE_SHEET_APP_ID")
@click.option("--sheet-name", default="Sheet1", envvar="LFK_SHEET_NAME")
def main(sheet_app_id, output_folder, sheet_name):

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

        place = {
            "name": name,
            "address": address,
            "active": string_to_boolean(item.get_field_value("active")),
            "cuisine": item.get_field_value("cuisine"),
            "curbside": string_to_boolean(item.get_field_value("curbside")),
            "curbside_instructions": item.get_field_value("curbside_instructions"),
            "delivery": string_to_boolean(item.get_field_value("delivery")),
            "delivery_service_websites": item.get_field_value(
                "delivery_service_websites"
            ),
            "giftcard": string_to_boolean(item.get_field_value("giftcard")),
            "giftcard_url": verify_http(item.get_field_value("giftcard_url")),
            "hours": item.get_field_value("hours"),
            "neighborhood": item.get_field_value("neighborhood"),
            "notes": item.get_field_value("notes"),
            "restaurant_phone": item.get_field_value("restaurant_phone"),
            "social": item.get_field_value("social"),
            "takeout": string_to_boolean(item.get_field_value("takeout")),
            "website": verify_http(item.get_field_value("website")),
        }
        post.content = item.get_field_value("notes")

        post.metadata.update(place)

        input_file.write_text(frontmatter.dumps(post))


if __name__ == "__main__":
    main()
