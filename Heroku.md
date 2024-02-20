# Run on Heroku.com

- get a Heroku account
- create a new heroku app
- download the heroku CLI
- login from terminal (where you will run the app)
- `git push heroku main`

other things....

heroku git:remote -a circuscircus
heroku addons:create heroku-postgresql:hobby-dev -a circuscircus

## Changes in 2021

If you want to run postgresql on your local machine to test first.

added `heroku` branch, and the postgres support.

**NOTA BENE:** DO NOT USE _whatever_ as your database password. Pick something else.
```
CREATE USER ccuser WITH PASSWORD 'whatever';
ALTER ROLE ccuser SET client_encoding TO 'utf8';
ALTER ROLE ccuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE ccuser SET timezone TO 'UTC';

CREATE DATABASE circuscircus;
GRANT ALL PRIVILEGES ON DATABASE circuscircus TO ccuser;
```
(Remember, this stuff is ALL done ot the postgres running on your DEV box, not the app on the internet at Heroku)

edit the forum.py file and switch dbs