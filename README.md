# CircusCircus
This is a minimal forum written in python with Flask. It supports only the bare minumum of features to allow discussions, including user accounts, threads, and comments.

On first run, the default subforums will be created. Although custom subforums are not supported through any user interface, it is possible to modify forum/setup.py to create custom subforums.

## Create a Github Organization

- create an org
- make all group members collaborators
- clone/branch from group's org's repo.
- maintain two branches,`main` & `dev` (plus a different branch for each group member)

## Features to Add

- divide `forum.py` into multiple modules (eg. `posts`, `comments`, `auth (login etc)`)
- migrate from sqlite3 to MySQL
- comments on each post (many comments to one post)
- like/dislike/heart/etc emojis on posts
- direct messages from one user to another
- insert pix links and/or video links
- a nice style based on Bootstrap
  - a logo on every page
  - copyright, about etc on footer of each page
- user settings
- public/private posts
  - public posts can be seen by people not logged in
  - private posts can only be seen by users logged in
- posts can be plain text or markdown

## Changes in 2020

I had to make a bunch of changes in this code to get it running. Took far longer than it should.
But now, if I have it right, you need to clone this and then

This currently puts a sqlite3 db in the /tmp directory.

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ ./run.sh
```

and it should appear on port 5000

`http://localhost:5000`

## Changes in 2023

database is now in `instance/` directory
removed version labels from `requirements.txt`

The Heroku file is broken.
The Procfile is broken too.

## Changes in 2024

Procfile is fixed.
