#NOVA
#by TheDerpySage

import discord
from discord.ext import commands
import asyncio
import nova_config
import db_functions
import email_functions
from datetime import datetime

desc = '''NOVA-BOT
A planner robot.'''

bot = commands.Bot(command_prefix='n$',description=desc)

#This is a buffer for the messages sent.
#It assist with server naming and proper callbacks with the command extension.
#To load it elsewhere, call global buffer
buffer = None

#Bot Events
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name='Use n$help'))
    #In order to edit her appearence, new parameters can be entered here.
    #fp = open("assets/nova.png", "rb")
    #await bot.edit_profile(password=None, username="nova-bot", avatar=fp.read())
    db_functions.init(nova_config.sql_config)
    email_functions.init(nova_config.email_sender, nova_config.email_token)

@bot.event
async def on_message(message):
    global buffer
    buffer = message
    await bot.process_commands(message)

#Bot Background Task
async def timer():
    await bot.wait_until_ready()
    while not bot.is_closed:
        check_notify()
        await asyncio.sleep(3600) # Fires the loop every hour

#Bot Commands
@bot.command()
async def hello():
    """Greet the bot."""
    await bot.say('Hi.')

@bot.command(hidden=True)
async def reset():
    global buffer
    if(buffer.author.id == "89033229100683264"):
        await bot.say("Restarting.")
        exit()
    else:
        await bot.say("I only do that for Majora.")

@bot.command(hidden=True)
async def force_daily_send():
    await bot.say("Ok, writing mail...")
    notify_daily_force()
    await bot.say("Sent!")

@bot.command(hidden=True)
async def force_weekly_send():
    await bot.say("Ok, writing mail...")
    notify_weekly_force()
    await bot.say("Sent!")

@bot.command()
async def credits():
    '''Show credits.'''
    await bot.say("`NOVA Planner Bot created by TheDerpySage.`")
    await bot.say("`Questions/Concerns? Add via Discord`")
    await bot.say("`@TheDerpySage#3694`")

#LOOKUPS
@bot.command()
async def todays_classes():
    """Returns Today's Classes"""
    await bot.say(db_functions.courses_day(getDayToday()))

@bot.command()
async def all_classes():
    """Returns All Classes"""
    await bot.say(db_functions.courses_all())

@bot.command()
async def all_future_homeworks():
    """Returns All Future Homework"""
    await bot.say(db_functions.upcoming_homeworks())

@bot.command()
async def all_future_exams():
    """Returns All Future Exams"""
    await bot.say(db_functions.upcoming_exams())

@bot.command()
async def upcoming_week():
    """Returns All Homework and Exams for the Week"""
    await bot.say(db_functions.upcoming_this_week())

@bot.command()
async def upcoming_today():
    """Returns All Homework and Exams for Today"""
    await bot.say(db_functions.upcoming_today())

@bot.command()
async def upcoming_tomorrow():
    """Returns All Homework and Exams for Tomorrow"""
    await bot.say(db_functions.upcoming_tomorrow())

@bot.command()
async def search_homeworks(*, searchterm: str):
    """Returns Homeowkr and Exams based on search terms passed
    n$search_homework <search term>"""
    await bot.say(db_functions.search_assignments(searchterm))

#INSERTS
@bot.command()
async def add_homework(CourseID, Title, DueDate, Description, Exam = None):
    """Add an Assignement to the DB
    n$add_homework '<Course ID>' '<Title>' '<Due Date as YYYY-MM-DD>' '<Description>' '<Optional 1 for Exam, 0 for Not Exam>'"""
    if not Exam:
        Exam = 0
    row = db_functions.insert_event(CourseID, Title, DueDate, Description, Exam)
    if row == 1:
        await bot.say("Insert was Successful. " + Title + " was added.")
    else: await bot.say("Something went wrong. Nothing added.")

@bot.command()
async def add_class(CourseID, Days, Place, Notes):
    """Add a Course to the DB
    n$add_class '<Course ID>' '<Days as MTWRF>' '<Place>' '<And Notes>'"""
    row = db_functions.insert_course(CourseID, Days, Place, Notes)
    if row == 1:
        await bot.say("Insert was Successful. " + CourseID + " was added.")
    else: await bot.say("Something went wrong. Nothing added.")

#REMOVES
@bot.command()
async def remove_homework(givenCourseID, givenTitle):
    """Removes an Assignment from the DB by Title
    n$remove_homework '<Title>'"""
    row = db_functions.remove_event(givenCourseID, givenTitle)
    if row == 1:
        await bot.say("Remove was Successful. " + givenTitle + " was removed.")
    else: await bot.say("Something went wrong. Nothing removed.")

@bot.command()
async def remove_class(givenCourseID):
    """Removes a Course and associated Assignments from the DB by Course ID
    n$remove_course '<Course ID>'"""
    row = db_functions.remove_course(givenCourseID)
    if row == 1:
        await bot.say("Remove was Successful. " + givenCourseID + " was removed.")
    else: await bot.say("Something went wrong. Nothing removed.")

#Misc Methods
def getDayToday():
    d = datetime.now()
    if d.weekday() == 0:
        return 'M'
    elif d.weekday() == 1:
        return 'T'
    elif d.weekday() == 2:
        return 'W'
    elif d.weekday() == 3:
        return 'R'
    elif d.weekday() == 4:
        return 'F'
    else: return 'S'

def check_notify():
    print("checked notify")
    if datetime.now().hour == 7: #Checks for 7am
        print("daily notify")
        message = ""
        temp = db_functions.courses_day(getDayToday())
        if temp != 0:
            message += "Classes Today:\n" + temp + "\n"
        else : message += "No Classes Today.\n\n"
        temp = db_functions.passed_due()
        if temp != 0:
            message += "Passed Due Assignments:\n" + temp
            rows = prune_assigments()
            message += str(rows) + " deleted.\n\n"
        else: message += "No Passed Due Assignments.\n\n"
        temp = db_functions.upcoming_today()
        if temp != 0:
            message += "Due Today:\n" + temp + "\n"
        else: message += "Nothing Due Today.\n\n"
        temp = db_functions.upcoming_tomorrow()
        if temp != 0:
            message += "Due Tomorrow:\n" + temp + "\n"
        else: message += "Nothing Due Tomorrow.\n\n"
        message += "~NOVA-BOT~"
        email_functions.send_email(nova_config.email_reciever, "Daily Update - NOVA", message)
        print("mail sent")
    if datetime.now().hour == 20 and datetime.now().weekday() == 6: #Checks for Sunday at 8pm
        print("weekly notify")
        temp = db_functions.upcoming_this_week()
        if temp != 0:
            message = "Upcoming This Week:\n" + temp
            message += "\n~NOVA-BOT~"
            email_functions.send_email(nova_config.email_reciever, "Weekly Digest - NOVA", message)
            print("mail sent")

def notify_daily_force():
    print("notify daily forced")
    message = ""
    temp = db_functions.courses_day(getDayToday())
    if temp != 0:
        message += "Classes Today:\n" + temp + "\n"
    else : message += "No Classes Today.\n\n"
    temp = db_functions.passed_due()
    if temp != 0:
        message += "Passed Due Assignments:\n" + temp
        rows = prune_assigments()
        message += str(rows) + " deleted.\n\n"
    else: message += "No Passed Due Assignments.\n\n"
    temp = db_functions.upcoming_today()
    if temp != 0:
        message += "Due Today:\n" + temp + "\n"
    else: message += "Nothing Due Today.\n\n"
    temp = db_functions.upcoming_tomorrow()
    if temp != 0:
        message += "Due Tomorrow:\n" + temp + "\n"
    else: message += "Nothing Due Tomorrow.\n\n"
    message += "~NOVA-BOT~"
    email_functions.send_email(nova_config.email_reciever, "Daily Update - NOVA", message)
    print("mail sent")

def notify_weekly_force():
    print("notify weekly forced")
    temp = db_functions.upcoming_this_week()
    if temp != 0:
        message = "Upcoming This Week:\n" + temp
        message += "\n~NOVA-BOT~"
        email_functions.send_email(nova_config.email_reciever, "Weekly Digest - NOVA", message)
        print("mail sent")

def prune_assigments():
    row = db_functions.prune_events()
    if row > 0:
        return row;
    else: return 0;

bot.loop.create_task(timer())
bot.run(nova_config.discord_token)
#I love you, sincerely
#Yours truly, 2095
