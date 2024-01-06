"""Parse andOTP backup into URIs optionally creating pass entries"""


import argparse
from sys import stdout
from json import load
from typing import IO, Any
from urllib.parse import quote
from subprocess import run


def item_to_uri(data: dict[str, Any]) -> str:
    return (
        f"otpauth://totp/{quote(data['label'] or data['issuer'], safe=':')}"
        f"?secret={data['secret']}&issuer={quote(data['issuer'])}"
    )


def print_uris(file: IO, output_file: IO | None = None) -> None:
    for item in load(file):
        print(item_to_uri(item), file=output_file)


def generate_pass_entries(file: IO, name_prefix: str = "otp_uri_generated/") -> None:
    for item in load(file):
        uri = item_to_uri(item)
        folder_name = item["issuer"] or item["thumbnail"] or item["label"].split()[0]
        file_name = item["label"] or folder_name
        run(
            ["pass", "otp", "insert", f"{name_prefix}{folder_name}/{file_name}"],
            input=uri,
            text=True,
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "json_backup",
        type=argparse.FileType("r"),
        help="Unencrypted JSON backup created by andOTP. Use '-' to read from stdin",
    )
    parser.add_argument("--generate-pass-entries", "-g", action="store_true")
    parser.add_argument(
        "--output-file", "-o", default=stdout, type=argparse.FileType("w")
    )
    parser.add_argument(
        "--pass-name-prefix", "-p", default="otp_uri_generated/", type=str
    )

    args = parser.parse_args()

    if args.generate_pass_entries:
        generate_pass_entries(args.json_backup, name_prefix=args.pass_name_prefix)
    else:
        print_uris(args.json_backup, output_file=args.output_file)


if __name__ == "__main__":
    main()
