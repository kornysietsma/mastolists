# mastolists

Very basic Python code for reviewing my followers and followings, including list membership

**THIS IS ALPHA QUALITY** - I'm mostly tinkering, but also trying to get my lists under control.

It is full of duplication, hardcoded constants, and probably terrible non-idiomatic code.  I'm not a python developer!  Well, I was in the '90s, but not now - a lot of this has been google-driven-development

You shouldn't run this without editing the code as usernames and instances are hardcoded!

Credentials aren't.

If you want to run it, the steps are:

- edit the code with your instance etc.
- set MASTODON_PASSWORD in the environment, ideally from a password safe
- run `poetry run register` to register the app - ONLY DO THIS ONCE, credentials are saved to a file
- run `poetry run login` to log in - You probably only need to do this once, login credentials are saved to a file but they might expire? It's safe to run again, anyway
- run `poetry run main` to generate CSV output
- run `poetry run dump` to dump everything to JSON

Then I suggest loading the CSV files into Google Sheets (handy as URLs will open in the same browser) and having a play.

The CSV has a bunch of columns:

- username - their short name
- acct - their full mastodon name e.g. 'foo@mastodon.social'
- display_name - their full name
- bot - are they a bot
- url - the URL to their page on _their_ instance
- local_page - the URL of their page on _your_ instance - from here you can add/remove to lists, etc
- followers_count
- following_count

then one column for each user list you have, with a value 'TRUE' if the user is in that list.

## Notes to self

I'm new to Python (well, this is a lie, I was proficient in python in the 1990s! But I'm new to the ecosystem these days) so keeping notes on things I need to do - especially relating to Poetry, the project tool I'm using.

### Poetry commands

`poetry shell` to open a virtual env in a shell

`poetry run main` to run the main entry point.  Or just `main` if in a shell (and `poetry install` has been run to update the entry points)

`exit` to exit the shell
