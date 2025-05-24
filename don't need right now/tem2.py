# daily work
import threading
import time
def walk_the_dog():
    time.sleep(8)
    print("you finish walking the dog")
def take_out_trash():
    time.sleep(2)
    print("you take out the trash")
def get_mail():
    time.sleep(4)
    print("you get the mail")
walk_the_dog()
take_out_trash()
get_mail()


chore1=threading.Thread(target=walk_the_dog)
chore1.start()
chore2=threading.Thread(target=take_out_trash)
chore2.start()
chore3=threading.Thread(target=get_mail)
chore3.start()