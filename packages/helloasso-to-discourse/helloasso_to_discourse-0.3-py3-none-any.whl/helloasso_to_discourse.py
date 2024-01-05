import argparse
import json
import re
import sys
from itertools import count, groupby
from pathlib import Path
from typing import Any, Dict, Set
from urllib.parse import urljoin

import requests
from helloasso_api import HaApiV5
from tabulate import tabulate


def parse_args():
    parser = argparse.ArgumentParser(description="Hello backup to Discourse badge")
    subparsers = parser.add_subparsers(help="Choose a command")

    fetch_parser = subparsers.add_parser(
        "fetch", help="Fetch HelloAsso data from the HelloAsso API to a file."
    )
    fetch_parser.add_argument("client_id")
    fetch_parser.add_argument("client_secret")
    fetch_parser.add_argument("org")
    fetch_parser.set_defaults(func=main_fetch)

    sync_parser = subparsers.add_parser(
        "sync", help="Sync the backup file to a given Discourse instance"
    )
    sync_parser.add_argument("discourse_url")
    sync_parser.add_argument("discourse_api_key")
    sync_parser.add_argument("helloasso_backup_file")
    sync_parser.add_argument(
        "form_slug",
        help="See the `list-forms` subcommand to learn which one you can use.",
    )
    sync_parser.add_argument("badge_slug")
    sync_parser.set_defaults(func=main_sync)

    list_form_parser = subparsers.add_parser(
        "list-forms", help="List HelloAsso forms, to use with `sync`"
    )
    list_form_parser.set_defaults(func=main_list_form)
    list_form_parser.add_argument("helloasso_backup_file")

    list_badges_parser = subparsers.add_parser(
        "list-badges", help="List Discourse badges, to use with `sync`"
    )
    list_badges_parser.set_defaults(func=main_list_badges)
    list_badges_parser.add_argument("discourse_url")
    list_badges_parser.add_argument("discourse_api_key")

    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(1)
    return args


class Discourse:
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key
        self.session = None
        self._email_to_user_map = None

    def __enter__(self):
        self.session = requests.Session()
        self.session.headers.update({"Api-Key": self.api_key, "Api-Username": "system"})
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

    def post(self, url, data=None, json=None, **kwargs):
        response = self.session.post(urljoin(self.url, url), data, json, **kwargs)
        response.raise_for_status()
        return response.json()

    def get(self, url, **kwargs):
        response = self.session.get(urljoin(self.url, url), **kwargs)
        response.raise_for_status()
        return response.json()

    def get_badge(self, badge_id):
        return self.get(f"/user_badges.json?badge_id={badge_id}")

    def get_badges(self):
        badges_info = self.get(f"/badges.json")
        badge_types = {
            badge_type["id"]: badge_type for badge_type in badges_info["badge_types"]
        }
        badge_groups = {
            badge_group["id"]: badge_group
            for badge_group in badges_info["badge_groupings"]
        }
        badges = badges_info["badges"]
        for badge in badges:
            badge["type"] = badge_types[badge["badge_type_id"]]
            badge["group"] = badge_groups[badge["badge_grouping_id"]]
        return {badge["slug"]: badge for badge in badges}

    def users(self, flag="active"):
        all_users = []
        for page in count(1):
            users = self.get(
                f"/admin/users/list/{flag}.json",
                params={"page": page, "show_emails": "true"},
            )
            if not users:
                break
            all_users.extend(users)
        return all_users

    @property
    def email_to_user_map(self) -> Dict[str, Dict[str, Any]]:
        if self._email_to_user_map:
            return self._email_to_user_map
        email_to_user = {}
        for user in self.users():
            email_to_user[remove_email_tag(user["email"])] = user
            for secondary_email in user["secondary_emails"]:
                email_to_user[remove_email_tag(secondary_email)] = user
        self._email_to_user_map = email_to_user
        return email_to_user

    def assign_badge(self, badge_id, username):
        return self.post(
            "/user_badges", data={"badge_id": badge_id, "username": username}
        )


def remove_email_tag(email):
    return re.sub(r"\+.*@", "@", email)


def main():
    args = parse_args()
    return args.func(args)


def main_list_form(args):
    helloasso_backup = json.loads(
        Path(args.helloasso_backup_file).read_text(encoding="UTF-8")
    )
    forms = [
        (item["order"]["formType"], item["order"]["formSlug"])
        for item in helloasso_backup
        if item["state"] == "Processed" and "payer" in item and "email" in item["payer"]
    ]
    table = [key + (len(list(group)),) for key, group in groupby(sorted(forms))]
    print(
        "Here are the available HelloAsso forms you can you with the `sync` command ",
        "to link a form to a badge:\n",
        sep="\n",
    )
    print(tabulate(table, headers=("Type", "Name", "Members")))
    print()
    print("Use the `name` for the `sync` command, like:")
    print(
        f'helloasso-to-discourse sync https://discuss.afpy.org "$(pass discuss.afpy.org-api-key)" ./afpy form-slug badge-slug'
    )


def main_list_badges(args):
    discourse = Discourse(args.discourse_url, args.discourse_api_key)
    table = []
    with discourse:
        for slug, badge in discourse.get_badges().items():
            table.append(
                (
                    badge["group"]["name"],
                    badge["type"]["name"],
                    slug,
                    badge["grant_count"],
                )
            )
    table.sort()
    print(tabulate(table, headers=("Group", "Type", "Slug", "Grant count")))
    print()
    print("Use the tag `slug` for the `sync` command, like:")
    print(
        f'helloasso-to-discourse sync https://discuss.afpy.org "$(pass discuss.afpy.org-api-key)" ./afpy form-slug badge-slug'
    )


def main_sync(args):
    helloasso_backup = json.loads(
        Path(args.helloasso_backup_file).read_text(encoding="UTF-8")
    )
    discourse = Discourse(args.discourse_url, args.discourse_api_key)
    with discourse:
        from_helloasso = {
            remove_email_tag(item["payer"]["email"])
            for item in helloasso_backup
            if item["order"]["formSlug"] == args.form_slug
            and item["state"] == "Processed"
            and "payer" in item
            and "email" in item["payer"]
        }
        print(f"Found {len(from_helloasso)} emails in HelloAsso")
        badges = discourse.get_badges()
        badge = badges[args.badge_slug]
        badge_users = discourse.get_badge(badges[args.badge_slug]["id"])["users"]
        already_assigned = {user["username"] for user in badge_users}
        print(f"Found {len(discourse.email_to_user_map)} emails in Discourse")
        common_emails = set(discourse.email_to_user_map) & from_helloasso
        print(f"Found {len(common_emails)} in common")
        already_assigned_count = 0
        for email in common_emails:
            discourse_user = discourse.email_to_user_map[email]
            if discourse_user["username"] in already_assigned:
                already_assigned_count += 1
                continue
            print(f"Assigning {badge['name']!r} to {discourse_user['username']!r}")
            discourse.assign_badge(badge["id"], discourse_user["username"])
        print(
            f"{already_assigned_count} Discourse users already have the badge {badge['name']!r}"
        )


def main_fetch(args):
    api = HaApiV5(
        api_base="api.helloasso.com",
        client_id=args.client_id,
        client_secret=args.client_secret,
        timeout=60,
    )

    backup = []
    endpoint = f"/v5/organizations/{args.org}/items"
    params = {"pageSize": 100}
    items = api.call(endpoint, params=params).json()
    while items["data"]:
        backup.extend(items["data"])
        params["continuationToken"] = items["pagination"]["continuationToken"]
        items = api.call(endpoint, params=params).json()
    Path(args.org).write_text(
        json.dumps(backup, indent=4, ensure_ascii=False), encoding="UTF-8"
    )


if __name__ == "__main__":
    main()
