import threading,object
from ad_script import all_ou_query,execute



#threads
def create_OU_thread(func):
    thread = threading.Thread(target=func)
    thread.start()




def get_users():
    print("users")




# getter functions
def get_all_OU():
    object.OU_LIST = execute(all_ou_query)
    print(object.OU_LIST)







