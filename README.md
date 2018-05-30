NOVA-BOT
=============
Designed to address a problem I had with remembering class schedules and deadlines.

Written in Python with a Chat Client front-end and MySQL back-end, NOVA was initially written in the span of a few weeks. The idea would be at the beginning of a semester when you get your class syllabuses that you'd take some time and enter all that information into NOVA, which would then store it into the MySQL DB. Then, every morning it'd send an e-mail containing things due that day, the next day, and things that you might've missed the previous day. Every Sunday it sends a weekly digest instead of the normal daily report to give you an idea of what you can expect for the week.

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

IMPLEMENT COGS https://gist.github.com/leovoel/46cd89ed6a8f41fd09c5 OR Completely remove discord.py.

Automate the creation of the DB tables (It assumes tables are setup)

Move to SQLite3

>Because of these, this is largely incomplete and shouldn't be deployed elsewhere, however it works in it's current state when the tables are properly setup
