NOVA-BOT
=============
A planning bot.
Built in python using MySQL database for scheduling storage.
Can keep track of important dates and sends weekly digests.
Can also send daily alerts for events.
Includes a Discord front-end using discord py.

*Written with a School Focus. DB designed with a class structure in mind.*

DEPENDENCIES
=============
Python 3.5.2

pip install discord.py

pip install mysql-connector

MySQL 5.7 Server

TO-DO
=============
Get CLI app working (import asyncio for background tasking to remain consistent between discord and CLI app)

Deal with 0 returns

Split up upcoming day/week by homework and exams

IMPLEMENT COGS https://gist.github.com/leovoel/46cd89ed6a8f41fd09c5

Automate the creation of the DB tables (It assumes tables are setup)

Move to SQLite3

>Because of these, this is largely incomplete and shouldn't be deployed elsewhere, however it works in it's current state when the tables are properly setup
