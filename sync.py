import click
import frontmatter

from pathlib import Path
from sheetfu import SpreadsheetApp, Table
from slugify import slugify
from typesystem.fields import Boolean


Boolean.coerce_values.update({"n": False, "no": False, "y": True, "yes": True})


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


@click.command()
@click.argument("token_filename")
@click.argument("output_folder")
@click.argument("sheet_app_id", envvar="GOOGLE_SHEET_APP_ID")
@click.argument("sheet_name", envvar="GOOGLE_SHEET_NAME")
def main(token_filename, output_folder, sheet_app_id, sheet_name):

    output_folder = Path(output_folder)

    spreadsheet = SpreadsheetApp(token_filename).open_by_id(sheet_app_id)

    sheet = spreadsheet.get_sheet_by_name(sheet_name)

    # returns the sheet range that contains data values.
    data_range = sheet.get_data_range()

    table = Table(data_range, backgrounds=True)

    for item in table:
        name = item.get_field_value("name")
        slug = slugify(name)
        filename = f"{slug}.md"

        input_file = output_folder.joinpath(filename)
        if input_file.exists():
            post = frontmatter.load(input_file)
        else:
            post = frontmatter.loads("")

        place = {
            "name": item.get_field_value("name"),
            "active": string_to_boolean(item.get_field_value("active")),
            "address": item.get_field_value("address"),
            "takeout": string_to_boolean(item.get_field_value("takeout")),
            "curbside": string_to_boolean(item.get_field_value("curbside")),
            "delivery": string_to_boolean(item.get_field_value("delivery")),
            "cuisine": item.get_field_value("cuisine"),
            "curbside_instructions": item.get_field_value("curbside_instructions"),
            "neighborhood": item.get_field_value("neighborhood"),
            "restaurant_phone": item.get_field_value("restaurant_phone"),
            "website": verify_http(item.get_field_value("website")),
            "delivery_service_websites": item.get_field_value(
                "delivery_service_websites"
            ),
            "hours": item.get_field_value("hours"),
            "social": item.get_field_value("social"),
            "notes": item.get_field_value("notes"),
        }
        post.content = item.get_field_value("notes")

        post.metadata.update(place)

        input_file.write_text(frontmatter.dumps(post))


if __name__ == "__main__":
    main()
