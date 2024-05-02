import subprocess,json
users = []
groups = []
computers = []
gpos = []
ous = []
containers = []
name = "Name"
dn = 'DistinguishedName'
oc = "ObjectClass"

# short commands
convert_to_json = "ConvertTo-Json"
pipe = " | "


# PowerShell command to get all objects
# powershell_command = "Get-ADUser -Filter * | Select-Object SamAccountName, DisplayName, Email"
all_users_query = "Get-ADUser -Filter * | Select-Object Name,DistinguishedName,ObjectClass | ConvertTo-Json"
all_group_query = "Get-ADGroup -Filter *| Select-Object Name,DistinguishedName,ObjectClass | ConvertTo-Json"
all_ou_query = "Get-ADOrganizationalUnit -Filter *| Select-Object Name,DistinguishedName,ObjectClass | ConvertTo-Json"
all_computer_query = "Get-ADComputer -Filter *| Select-Object Name,DistinguishedName,ObjectClass | ConvertTo-Json"
all_gpo_query = "Get-GPO -All"
# CMD = "Get-ADUser -Filter {SamAccountName -eq 'hr1'} -Properties *"


def get_query_user_properties(identity = "Guest"):
    return f"Get-ADUser -Identity '{identity}' -Properties *"+pipe+convert_to_json


def get_query_property(_dict:dict):
    # ------->>>  City, Country
    temp_str = ""
    i = 1
    for key in _dict.keys():
        temp_str += " "+key
        if len(_dict) > i:
            temp_str +=","
        i += 1
    return temp_str
# print(get_property_query({"City":"karachi","Country":"Pakistan"}))


def get_query_property_value(dict_:dict):
    # ----->>>    $_.City -eq 'karachi' -and $_.Country -eq 'Pakistan'
    temp_str = ""
    i = 1
    for key,value in dict_.items():
        temp_str +=" "+ f"$_.{key} -eq '{value}'"
        if len(dict_)>i:
            temp_str +=" -and"
        i+=1 
    return temp_str
# print(get_property_value_query({"City":"karachi","Country":"Pakistan"}))


def get_query_sp_gp_mems(gp_dn):
    query = f"Get-ADGroupMember -Identity '{gp_dn}' | ConvertTo-Json"
    return query


def get_query_sp_mems_of_gp(gp_dn,property,property_value):
    user_comparision_property = "Where-Object { "+ property_value +" }"
    user_filter_properties =  f"Get-ADUser -Properties {property}"
    user_object_filter_query = "Where-Object { $_.ObjectClass -eq 'user' }"
    query = f"Get-ADGroupMember -Identity '{gp_dn}'"    
    return query + pipe +user_object_filter_query +pipe +user_filter_properties+pipe+user_comparision_property+ pipe+convert_to_json

def get_query_gp_in_ou(ou_dn):
    return f"Get-ADGroup -Filter * -SearchBase '{ou_dn}'"+pipe+" Select-Object Name,DistinguishedName,ObjectClass"+pipe+convert_to_json

def execute(query):
    result = subprocess.run(["powershell.exe", "-Command", query], capture_output=True, text=True)
    # print(result.stdout)
    if not result.stdout:
        temp_list = list()
        # temp_list.append({"name":"Demo","dn":"CN=Demo,DC=ITX,DC=com"})
        return temp_list
    data = json.loads(result.stdout)
    if type(data) != type(list()):
        temp_list= list()
        temp_list.append(data)
        data = temp_list
    # print(data)
    return data


# temp_dict = {"City":"Karachi","Country":"PK"}
# print(execute(get_query_gp_in_ou("OU=HR,DC=DC,DC=ITX")))












def firstoptions():
    print("0-->Users")
    print("1-->Groups")
    print("2-->OU's")
    print("3-->Computers")

def show_objects(data):
    i = 0
    if data:
        for object in data:
            print(i,object.get("ObjectClass"),object.get("Name"),object.get(dn))
            print("-" * 30)
            i+=1
def get_ou_users(data):
    i = 0
    if data:
        for object in data:
            print(i,object.get("ObjectClass"),object.get("Name"),object.get(dn))
            print("-" * 30)
            i+=1
    ou_num = int(input("To see the users of OU select above num:"))
    
    if ou_num>-1 or ou_num<i:
        query = f"Get-ADUser -Filter * -SearchBase '{data[ou_num].get('DistinguishedName')}' | Select-Object Name,DistinguishedName,ObjectClass | ConvertTo-Json"
        data = execute(query)
        show_objects(data)
        user_num = int(input('if you want to see the users properties select user:'))
        if user_num>-1 or user_num<len(data):
            query = f"Get-ADUser -Identity '{data[user_num].get('DistinguishedName')}' -Properties * | ConvertTo-Json"
            data = execute(query)
            show_all_properties(data)

def show_all_properties(data):
    if data:
        for item in data:
            for key,value in item.items():
                print(key,value)



# while True:
#     firstoptions()
#     flag =int(input("enter your option:"))

#     if flag ==0:
#         data = execute(all_users_query)
#         show_objects(data)
#     elif flag ==1:
#         data =execute(all_group_query)
#         show_objects(data)
#     elif flag ==2:
#         data =execute(all_ou_query)
#         show_objects(data)
#     elif flag == 3:
#         data =execute(all_computer_query)
#         show_objects(data)