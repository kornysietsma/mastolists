"""List management"""

import csv
import json
import os
import pprint
import sys
import html2text
from dotenv import load_dotenv
from mastodon import Mastodon

load_dotenv()

MY_INSTANCE = os.environ["INSTANCE"]
MY_USERNAME = os.environ["USERNAME"]


def register():
    """register the app (once only)"""
    Mastodon.create_app(
        "mastolists",
        api_base_url=MY_INSTANCE,
        to_file="mastolists_clientcred.secret",
    )


def login():
    """log in and save credentials"""
    password = os.getenv("MASTODON_PASSWORD")

    if password is None:
        raise "No password in environment"

    mastodon = Mastodon(
        api_base_url=MY_INSTANCE, client_id="mastolists_clientcred.secret"
    )
    mastodon.log_in(
        MY_USERNAME,
        password,
        to_file="mastolists_usercred.secret",
    )


def dump():
    """dump all data"""

    mastodon = Mastodon(
        access_token="mastolists_usercred.secret", api_base_url=MY_INSTANCE
    )

    me = mastodon.me()
    my_id = me.id

    following = mastodon.account_following(my_id)
    if hasattr(following, "_pagination_next"):
        following = mastodon.fetch_remaining(following)
    followers = mastodon.account_followers(my_id)
    if hasattr(followers, "_pagination_next"):
        followers = mastodon.fetch_remaining(followers)
    lists = mastodon.lists()
    for list in lists:
        accounts = mastodon.list_accounts(list.id)
        if hasattr(accounts, "_pagination_next"):
            accounts = mastodon.fetch_remaining(accounts)
        with open(f"list_{list.title}.json", "w") as outfile:
            json.dump(accounts, outfile, indent=2, default=str)

    bookmarks = mastodon.bookmarks()
    if hasattr(bookmarks, "_pagination_next"):
        bookmarks = mastodon.fetch_remaining(bookmarks)

    relationships = {
        user.acct: mastodon.account_relationships(user.id) for user in following
    }

    with open("following.json", "w") as outfile:
        json.dump(following, outfile, indent=2, default=str)

    with open("followers.json", "w") as outfile:
        json.dump(followers, outfile, indent=2, default=str)

    with open("bookmarks.json", "w") as outfile:
        json.dump(bookmarks, outfile, indent=2, default=str)

    with open("relationships.json", "w") as outfile:
        json.dump(relationships, outfile, indent=2, default=str)


def clean_notes(html):
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_tables = True
    h.ignore_emphasis = True
    h.ignore_images = True
    text = h.handle(html)
    # remove blank lines entirely
    return os.linesep.join([s for s in text.splitlines() if s])


def cli(args=None):
    """Process command line arguments."""
    if not args:
        args = sys.argv[1:]

    mastodon = Mastodon(
        access_token="mastolists_usercred.secret", api_base_url=MY_INSTANCE
    )

    me = mastodon.me()
    my_id = me.id
    following = mastodon.account_following(my_id)
    if hasattr(following, "_pagination_next"):
        following = mastodon.fetch_remaining(following)
    followers = mastodon.account_followers(my_id)
    if hasattr(followers, "_pagination_next"):
        followers = mastodon.fetch_remaining(followers)
    lists = mastodon.lists()
    list_members = {}
    for list in lists:
        accounts = mastodon.list_accounts(list.id)
        if hasattr(accounts, "_pagination_next"):
            accounts = mastodon.fetch_remaining(accounts)
        list_members[list.title] = [account.acct for account in accounts]
        for f in following:
            if f.acct in list_members[list.title]:
                f[list.title] = True
        for f in followers:
            if f.acct in list_members[list.title]:
                f[list.title] = True

    #  LOCAL PAGE FORMAT VARIES BY INSTANCE - check this:

    for f in following:
        f["local_page"] = f"{MY_INSTANCE}/@{f.acct}"
        f["note"] = clean_notes(f["note"])
    for f in followers:
        f["local_page"] = f"{MY_INSTANCE}/@{f.acct}"
        f["note"] = clean_notes(f["note"])

    with open("followers.csv", "w", newline="") as csvfile:
        fieldnames = [
            "username",
            "acct",
            "display_name",
            "bot",
            "url",
            "local_page",
            "followers_count",
            "following_count",
            "note",
        ]
        for list in lists:
            fieldnames.append(list.title)
        fwriter = csv.DictWriter(
            csvfile, fieldnames, dialect="excel", extrasaction="ignore"
        )
        fwriter.writeheader()
        fwriter.writerows(followers)

    with open("following.csv", "w", newline="") as csvfile:
        fieldnames = [
            "username",
            "acct",
            "display_name",
            "bot",
            "url",
            "local_page",
            "followers_count",
            "following_count",
            "note",
        ]
        for list in lists:
            fieldnames.append(list.title)
        fwriter = csv.DictWriter(
            csvfile, fieldnames, dialect="excel", extrasaction="ignore"
        )
        fwriter.writeheader()
        fwriter.writerows(following)
