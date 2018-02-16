import db_functions
import email_functions
from nova_config import config


db_functions.init(config)
print(db_functions.courses_all())
print(db_functions.courses_day('M'))
