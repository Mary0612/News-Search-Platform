import datetime
import sqlite3
from definition import check_result

check_result()

d_end = input("From which date (yyyy/mm/dd) would you like to delete older news?\n")

confirm = input("Are you sure about deleting news before {}? (Enter \"yes\" to continue.)\n".format(d_end))
if confirm == "yes":
    con = sqlite3.connect('news_info.db')
    cursor = con.cursor()
    cursor.execute("DELETE FROM news WHERE date < ?;", (d_end,))
    con.commit()
    con.close()
    print("Complete the deletion process")
else:
    print("Cancel the deletion process")
    
check_result()