from utils.db import create_students_table
from utils.db import create_daily_updates_table

create_students_table()
create_daily_updates_table()

print("All tables created successfully!")