class Translation(object):
    START_TXT = """ <b> HEY {}\n IAM A FILTER BOT CURRENTLY MY ADMIN  BUILDING ME !</b> \n
<b>Bot Maintained By: @mdadmin2 </b> \n 
"""
    ABOUT_TXT = """ <b>CURRENTLY BUILDING </b> \n
"""

# temp db for banned 
class temp(object):
    
    ME = None
    CURRENT=int(os.environ.get("SKIP", 2))
    CANCEL = False 
    U_NAME = None
