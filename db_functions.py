import mysql.connector
from mysql.connector import errorcode

#QUERYS
queryThisWeek = "SELECT events.CourseID, events.Title, events.DueDate, events.Description FROM events WHERE WEEK(events.DueDate)=WEEK(CURRENT_DATE);"
queryToday = "SELECT events.CourseID, events.Title, events.DueDate, events.Description FROM events WHERE events.DueDate=CURRENT_DATE;"
queryTomorrow = "SELECT events.CourseID, events.Title, events.DueDate, events.Description FROM events WHERE events.DueDate=(CURRENT_DATE + INTERVAL 1 DAY)"
queryPassedDue = "SELECT events.CourseID, events.Title, events.DueDate, events.Description FROM events WHERE events.DueDate<CURRENT_DATE;"
queryFutureHomework = "SELECT events.CourseID, events.Title, events.DueDate, events.Description FROM events WHERE events.DueDate>=CURRENT_DATE AND events.Exam=0;"
queryFutureExams = "SELECT events.CourseID, events.Title, events.DueDate, events.Description FROM events WHERE events.DueDate>=CURRENT_DATE AND events.Exam=1;"
queryEventSearch = "SELECT events.CourseID, events.Title, events.DueDate, events.Description FROM events WHERE INSTR(events.Title, '%s') OR INSTR(events.Description, '%s');"
queryAllCourses = "SELECT courses.CourseID, courses.Place, courses.Notes FROM courses;"
queryCourseByDay = "SELECT courses.CourseID, courses.Place, courses.Notes FROM courses WHERE INSTR(courses.Days, '%s');"

#INSERTS
insertCourse = "INSERT INTO courses (CourseID, Days, Place, Notes) VALUES ('%s', '%s', '%s', '%s');"
insertEvent = "INSERT INTO events (CourseID, Title, DueDate, Description, Exam) VALUES ('%s', '%s', '%s', '%s', '%s');"

#REMOVES
removeCourse1 = "DELETE FROM courses WHERE courses.CourseID='%s';"
removeCourse2 = "DELETE FROM events WHERE events.CourseID='%s';"
removeEvent = "DELETE FROM events WHERE events.CourseID='%s' AND events.Title='%s';"
removePassedDue = "DELETE FROM events WHERE events.DueDate<CURRENT_DATE;"

#CONFIG LOADED AT INIT
config = ""

def init(loadedConfig):
    global config
    config = loadedConfig
    print("Testing DB connection... ")
    #REDUNDANT
    cnx = cur = None
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Something is wrong with your user name or password')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return 0
    else:
        cur = cnx.cursor(buffered=True)
        cur.execute('use schedule;')
        print("OK!")
        return 1
    #TECHNICALLY REDUNDANT, PYTHON CLOSES ON END OF DEF
    finally:
        if cur:
            cur.close()
        if cnx:
            cnx.close()

#LOOKUPS
def upcoming_homeworks():
    global config
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor(buffered=True)
    cur.execute('use schedule;')
    cur.execute(queryFutureHomework)
    if not cur.rowcount:
        return 0
    else: return format_result_events_wDate(cur)

def upcoming_exams():
    global config
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor(buffered=True)
    cur.execute('use schedule;')
    cur.execute(queryFutureExams)
    if not cur.rowcount:
        return 0
    else: return format_result_events_wDate(cur)

def upcoming_this_week():
    global config
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor(buffered=True)
    cur.execute('use schedule;')
    cur.execute(queryThisWeek)
    if not cur.rowcount:
        return 0
    else: return format_result_events_wDate(cur)

def upcoming_today():
    global config
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor(buffered=True)
    cur.execute('use schedule;')
    cur.execute(queryToday)
    if not cur.rowcount:
        return 0
    else: return format_result_events(cur)

def upcoming_tomorrow():
    global config
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor(buffered=True)
    cur.execute('use schedule;')
    cur.execute(queryTomorrow)
    if not cur.rowcount:
        return 0
    else: return format_result_events(cur)

def passed_due():
    global config
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor(buffered=True)
    cur.execute('use schedule;')
    cur.execute(queryPassedDue)
    if not cur.rowcount:
        return 0
    else: return format_result_events(cur)

def search_assignments(searchTerm):
    global config
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor(buffered=True)
    cur.execute('use schedule;')
    cur.execute(queryEventSearch  % (searchTerm, searchTerm))
    if not cur.rowcount:
        return 0
    else: return format_result_events_wDate(cur)

def courses_all():
    global config
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor(buffered=True)
    cur.execute('use schedule;')
    cur.execute(queryAllCourses)
    if not cur.rowcount:
        return 0
    else: return format_result_courses(cur);

def courses_day(givenDay):
    global config
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor(buffered=True)
    cur.execute('use schedule;')
    cur.execute(queryCourseByDay % (givenDay))
    if not cur.rowcount:
        return 0
    else: return format_result_courses(cur);


#INSERTS
def insert_course(givenCourseID, givenDays, givenPlace, givenNotes):
    global config
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor(buffered=True)
    cur.execute('use schedule;')
    cur.execute(insertCourse % (givenCourseID, givenDays, givenPlace, givenNotes))
    if not cur.rowcount:
        return 0
    else:
        cnx.commit()
        return cur.rowcount;

def insert_event(givenCourseID, givenTitle, givenDueDate, givenDescription, givenExam = None):
    if givenExam is None:
        givenExam = 0
    global config
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor(buffered=True)
    cur.execute('use schedule;')
    cur.execute(insertEvent % (givenCourseID, givenTitle, givenDueDate, givenDescription, givenExam))
    if not cur.rowcount:
        return 0
    else:
        cnx.commit()
        return cur.rowcount

#REMOVES
def remove_course(givenCourseID):
    global config
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor(buffered=True)
    cur.execute('use schedule;')
    cur.execute(removeCourse1 % (givenCourseID))
    if not cur.rowcount:
        return 0
    else:
        cur.execute(removeCourse2 % (givenCourseID))
        cnx.commit()
        return 1

def remove_event(givenCourseID, givenTitle):
    global config
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor(buffered=True)
    cur.execute('use schedule;')
    cur.execute(removeEvent % (givenCourseID, givenTitle))
    if not cur.rowcount:
        return 0
    else:
        cnx.commit()
        return cur.rowcount

def prune_events():
    global config
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor(buffered=True)
    cur.execute('use schedule;')
    cur.execute(removePassedDue)
    if not cur.rowcount:
        return 0
    else:
        cnx.commit()
        return cur.rowcount


#FORMATTING
def format_result_events(cursor):
    temp = ""
    for (CourseID, Title, DueDate, Description) in cursor:
        temp+=("{}: {}, {}\n".format(CourseID, Title, Description))
    return temp

def format_result_events_wDate(cursor):
    temp = ""
    for (CourseID, Title, DueDate, Description) in cursor:
        temp+=("{}, {}, Due on {:%d %b %Y}: {}.\n".format(CourseID, Title, DueDate, Description))
    return temp

def format_result_courses(cursor):
    temp = ""
    for (CourseID, Place, Notes) in cursor:
        temp+=("{} at {}: {}\n".format(CourseID, Place, Notes))
    return temp
