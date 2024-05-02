import object,os
from kivymd.toast import toast
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors import CommonElevationBehavior
from kivymd.uix.button import MDRoundFlatButton,MDFlatButton
from kivymd.uix.button import BaseButton
from kivy.utils import rgba
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivy.core.window import Window
from kivymd.uix.list import ILeftBodyTouch,TwoLineIconListItem,TwoLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivy.properties import StringProperty

# abc = MDTextField()
# abc.








from kivy.lang import Builder
Builder.load_file('UI/main.kv')
Builder.load_file('UI/AddBulkUser.kv')
Builder.load_file('UI/EditBulkUser.kv')
Builder.load_file('UI/DropDownButton.kv')
Builder.load_file('UI/UserEditListItem.kv')




# constants
_name = "name"
_dn = "dn"


# screen names
_export_adusers = "export_adusers"
_adusers = "adusers"
_add_bulk_users ="AddBulkUsersScreen"
_edit_bulk_users = "EditBulkUsersScreen" 


class FileExportWidget(MDBoxLayout):
    def export_click(self):
        print(self.parent.parent.parent.parent.ids)
        file_name = self.ids.filename_field.text
        if not file_name:
            toast("Please enter the file name")
            return
        print(os.getcwd())

class CheckedItem(MDBoxLayout):
    name = StringProperty()
    dn = StringProperty()


class UserEditListItem(TwoLineAvatarIconListItem):
    icon_left = StringProperty()
    icon_right = StringProperty()

    

class DropDownButton(MDBoxLayout,BaseButton):
    icon = StringProperty()
    text = StringProperty()

class BaseShadowWidget(CommonElevationBehavior):
    pass

class FilterWidget(MDBoxLayout):
    pass

class TitleBar(CommonElevationBehavior,MDBoxLayout):
    pass

class SpecificButton(CommonElevationBehavior,MDRoundFlatButton):
    pass

class SideBar(BaseShadowWidget,MDBoxLayout):
    pass

class CenterBar(MDBoxLayout):
    pass

class ListItemWithCheckbox(TwoLineIconListItem):
    pass

class LeftCheckBox(ILeftBodyTouch,MDCheckbox):

    def on_check(self):
        flag =self.active
        name_=self.parent.parent.text
        dn_=self.parent.parent.secondary_text
        if flag:
            self.parent.parent.parent.parent.parent.add_checked_item(name_,dn_)
        else:
            self.parent.parent.parent.parent.parent.remove_checked_item(dn_)

class AttributeField(MDBoxLayout):

    def remove_me(self):
        self.parent.remove_widget(self)
    def get_attribute(self):
        return self.children[0].text
    
class SwitchBox(MDBoxLayout):
    text = StringProperty()
    
    def get_status(self):
        return self.children[0].active

class ConditionValueItem(MDBoxLayout):

    condition = StringProperty()
    def remove_me(self):
        self.parent.remove_widget(self)
    def get_value(self):
        return self.children[0].text
           
class FilterDialog(MDDialog):

    def open(self):
        super().open()        

    def get_checked_item(self):
        return self.content_cls.checked_data
    
    def get_attribute_list(self):
        return self.content_cls.get_attribute_list()

class FilterItem(MDBoxLayout):

    text = StringProperty()
    hint_text = StringProperty()
    checked_data=None # this list contains checked data only
    data = None
    object_list = None

    def add_checked_item(self,name_,dn_):
        temp_dict = {}
        temp_dict[_name]=name_
        temp_dict[_dn]=dn_
        self.checked_data.append(temp_dict)

    def remove_checked_item(self,dn):
        for item in self.checked_data:
            if item.get(_dn)==dn:
                self.checked_data.remove(item)
                # print(self.checked_data)
                return
            
    def create_object_list(self):# to call the object list first assign the 'self.data',it contains data on which objects to be create.
        # if not self.data:
        #     raise("first assing the 'self.data' as list object")
        temp_list = list()
        for item in self.data:
            temp=ListItemWithCheckbox(text=item.get("name"),secondary_text=item.get("dn"))
            temp_list.append(temp)
        self.object_list = temp_list
                
    def remove_items(self):
        self.ids.list_container.clear_widgets()

    def add_items(self,_list=None):
        temp_list =self.object_list
        if _list:
            temp_list = _list
        for item in temp_list:
            self.ids.list_container.add_widget(item)
    
    def search_item(self,search_word:str=None):
        temp_list =[]
        if search_word:
            temp_list.append(item for item in self.object_list if item.text.upper().startswith(search_word.upper()))
            return temp_list[0] ## it gives the generator object
        return temp_list
    
    def on_text_changed(self):
        text =self.ids.search_bar.text
        self.remove_items()
        gen_obj =self.search_item(text)
        self.add_items(gen_obj)

class ConditionFilterBox(MDBoxLayout):

    def add_click(self):
        attribute = self.ids.condition_bar.text
        if attribute:
            #create codition value item with attribute value and insert into condition container
            self.ids.condition_bar.text=""
            temp_condition_value_item = ConditionValueItem(condition=attribute)
            self.ids.condition_container.add_widget(temp_condition_value_item)
    
    def get_condition_items(self):
        '''this function return dict object of condition : value'''
        _like_or_equal = " -eq "
        _and_or_OR = " -or "

        if self.ids.like_switch.get_status():
            _like_or_equal =" -like "
        
        if self.ids.and_switch.get_status():
            _and_or_OR = " -and "

        length = len(self.ids.condition_container.children)
        temp_list = []
        i = 0
        for item in self.ids.condition_container.children:
            i += 1
            temp_str = item.condition + _like_or_equal  +"'"+ item.get_value()+"'"
            temp_list.append(temp_str)
            if length % 2 ==0 and not i >= length:
                temp_list.append(_and_or_OR)
        return temp_list
        
class AttributeFilterBox(MDBoxLayout):
    
    def add_attribute(self):
        attr_ = AttributeField()
        self.ids.attribute_container.add_widget(attr_)

    def get_attribute_list(self):
        temp_list = list()
        for obj in self.ids.attribute_container.children:
            if obj.get_attribute()!="":
                temp_list.append(obj.get_attribute())
        return temp_list

class HomeScreen(MDScreen):
    # item = ListItemWithCheckbox()
    
    ou_dialog=None
    condition_dialog=None
    users_dialog = None
    prev_ou_state=None

    def OU_click(self):
        temp_list = [{"name":"HR","dn":"CN=HR,DC=ITX,DC=com"},{"name":"Admin","dn":"CN=Admin,DC=ITX,DC=com"},{"name":"Finance","dn":"CN=Finance,DC=ITX,DC=com"},
                         {"name":"Security","dn":"CN=Security,DC=ITX,DC=com"},{"name":"IT","dn":"CN=IT,DC=ITX,DC=com"},{"name":"Management","dn":"CN=Management,DC=ITX,DC=com"},
                         {"name":"Staff","dn":"CN=Staff,DC=ITX,DC=com"},{"name":"Technical","dn":"CN=Technical,DC=ITX,DC=com"}]
        if not self.ou_dialog:

            filter_item = FilterItem(hint_text = "Search OU")
            self.ou_dialog = FilterDialog(
                                        title="Filter OU",
                                        size_hint=(0.5,None),
                                        content_cls=filter_item,
                                        type="custom",
                                        buttons=[
                                                MDFlatButton(
                                                    text="OK",
                                                    theme_text_color="Custom",
                                                    text_color=rgba("#3333CC"),
                                                    on_release=lambda x: self.ok_click(1)
                                                ),
                                            ],
                                        )
            self.ou_dialog.content_cls.data=temp_list
            self.ou_dialog.content_cls.create_object_list()
            self.ou_dialog.content_cls.add_items()
            self.ou_dialog.content_cls.checked_data=list()
        self.ou_dialog.open()


    def condition_click(self):

        if not self.condition_dialog:
            condition_filter_box = ConditionFilterBox()
            self.condition_dialog = FilterDialog(
                                                title = "Add Conditions",
                                                size_hint=(0.5,None),
                                                content_cls=condition_filter_box,
                                                type="custom",
                                                buttons=[
                                                        MDFlatButton(
                                                            text="OK",
                                                            theme_text_color="Custom",
                                                            text_color=rgba("#3333CC"),
                                                            on_release=lambda x: self.ok_click(2)
                                                        ),
                                                    ],
                                            )
        self.condition_dialog.open()
    


    def users_click(self):
        if not self.users_dialog:
            attr_filter_box = AttributeFilterBox()
            self.users_dialog = FilterDialog(
                size_hint=(0.3,None),
                content_cls=attr_filter_box,
                type="custom",
                title="Attribute Filter",
                buttons=[
                        MDFlatButton(
                            text="OK",
                            theme_text_color="Custom",
                            text_color=rgba("#3333CC"),
                            on_release=lambda x: self.ok_click(3)
                        ),
                    ],
                ) 
        self.users_dialog.open()

    def ok_click(self,flag):
        if flag==1:### ok click of ou dialog
            self.add_checked_OU()
            # print(self.ou_dialog.content_cls.checked_data)
            self.ou_dialog.dismiss()
        elif flag==2: ### ok click of group dialog
            self.add_conditions()
            # print(self.group_dialog.content_cls.checked_data)
            self.condition_dialog.dismiss()
        elif flag==3:### ok click of user dialog
            self.add_attribute()
            self.users_dialog.dismiss()

    def add_checked_OU(self):
        self.ids.ou_checked_item_box.clear_widgets()
        list_ = self.ou_dialog.get_checked_item()
        if list_:
            self.ids.ou_checked_item_box.add_widget(
                MDLabel(
                            text="OU",
                            size_hint=(None,None),
                            adaptive_size=True,
                            font_style ="H6",
                            bold = True)
            )
        for item in list_:
            self.ids.ou_checked_item_box.add_widget(CheckedItem(name=item.get(_name),dn=item.get(_dn)))


    def add_conditions(self):
        self.ids.condition_item_box.clear_widgets()
        list_ = self.condition_dialog.content_cls.get_condition_items()
        if list_:
            self.ids.condition_item_box.add_widget(
                MDLabel(
                        text="Condition",
                        size_hint=(None,None),
                        adaptive_size=True,
                        font_style ="H6",
                        bold = True)
            )

        for item in list_:
            self.ids.condition_item_box.add_widget(MDLabel( text=item,
                                                            size_hint=(None,None),
                                                            adaptive_size=True,
                                                            font_style ="Caption"
                                                            ))

    def add_checked_group(self):
        self.ids.group_checked_item_box.clear_widgets()
        list_=self.group_dialog.get_checked_item()
        if list_:
            self.ids.group_checked_item_box.add_widget(
                MDLabel(
                        text="Group",
                        size_hint=(None,None),
                        adaptive_size=True,
                        font_style ="H6",
                        bold = True)
            )
        for item in list_:
            self.ids.group_checked_item_box.add_widget(CheckedItem(name=item.get(_name),dn=item.get(_dn)))

    
    def add_attribute(self):
        self.ids.attribute_box.clear_widgets()
        list_=self.users_dialog.get_attribute_list()

        if list_:
            self.ids.attribute_box.add_widget(
                MDLabel(
                        text="Attributes",
                        size_hint=(None,None),
                        adaptive_size=True,
                        font_style ="H6",
                        bold = True)
            )
        for item in list_:
            self.ids.attribute_box.add_widget(MDLabel(text=item,font_style='Caption',
                                                            size_hint=(None,None),adaptive_size=True))
    
    def submit_click(self):
        self.ids.div1_2_1.clear_widgets()
        if not self.ids.attribute_box.children or not self.ids.condition_item_box.children or not self.ids.ou_checked_item_box.children:
            self.ids.div1_2_1.add_widget(MDLabel(
                text = "NothingToExport",
                pos_hint={'center_x':0.5,'center_y':0.5},
                font_style='H4',
                size_hint=(None,None),
                adaptive_size = True

            ))
            return

        self.ids.div1_2_1.add_widget(FileExportWidget())
        pass
        
class AddBulkUsers(MDScreen):
    pass

class EditBulkUsers(MDScreen):
    OuDialog = None
    entered = False
    user_list = None

    def FilterClick(self):
        print("Filter Click")
        temp_list = [{"name":"HR","dn":"CN=HR,DC=ITX,DC=com"},{"name":"Admin","dn":"CN=Admin,DC=ITX,DC=com"},{"name":"Finance","dn":"CN=Finance,DC=ITX,DC=com"},
                            {"name":"Security","dn":"CN=Security,DC=ITX,DC=com"}]
        if not self.OuDialog:
            filter_item = FilterItem(hint_text = "Search OU")
            filter_item.data = temp_list
            filter_item.create_object_list()
            filter_item.add_items()
            filter_item.checked_data=list()
            self.OuDialog = MDDialog(
                size_hint=(0.5,None),
                type="custom",
                title="Filter",
                content_cls=filter_item,
                buttons=[
                        MDFlatButton(
                            text="OK",
                            theme_text_color="Custom",
                            text_color=rgba("#3333CC"),
                            on_release=lambda x: self.ok_click()
                        ),
                    ],

            )
        self.OuDialog.open()

    def ok_click(self):
        Clock.schedule_once(lambda dt: self.search_users_according_checked_ou(self.OuDialog.content_cls.checked_data,
                                                                              object.OU_LIST), 0.5)

    def search_users_according_checked_ou(self,checked_ou_list,user_list):
        print("funct called")
        pass

    def on_enter(self):
        if not self.entered:
            self.user_list = list(object.USER_LIST)
            self.AddUsers(self.user_list)
            self.entered = True

    def AddUsers(self,temp_list):

        if temp_list:
            for user in temp_list:
                self.ids.user_list.add_widget(self.create_user_edit_list_item(user["name"],user["dn"]))

    def remove_items(self):
        self.ids.user_list.clear_widgets()

    def on_text_change(self,search_bar):
        self.remove_items()
        text = search_bar.text
        gen_obj = self.search_item(self.user_list,text)
        if gen_obj:
            self.AddUsers(gen_obj)
        elif text=="":
            self.AddUsers(self.user_list)
        

    def search_item(self,_list,search_word:str=None):
        temp_list =[]
        if search_word:
            temp_list.append(item for item in _list if item['name'].upper().startswith(search_word.upper()))
            return temp_list[0] ## it gives the generator object
        return temp_list        

    
    def create_user_edit_list_item(self,name,dn):
        return UserEditListItem(text=name,
                                secondary_text=dn,
                                icon_left="account",
                                icon_right="square-edit-outline"
                            )



class UsersScreen(MDScreen):
    def AddBulkUsers_Screen(self,button):
        button.line_color="#3333CC"
        if self.ids.EditBulkUsersButton.line_color:
            self.ids.EditBulkUsersButton.line_color=[0,0,0,0]
        self.ids.user_sm.current = _add_bulk_users

    def EditBulkUsers_Screen(self,button):
        button.line_color="#3333CC"
        if self.ids.AddBulkUsersButton.line_color:
            self.ids.AddBulkUsersButton.line_color=[0,0,0,0]
        self.ids.user_sm.current = _edit_bulk_users

   



class ITX_AD(MDApp):
    
    def build(self):
        super().build()
        Window.set_icon('UI/images/icon.png')
        Window.maximize()
        self.box = MDBoxLayout(md_bg_color=rgba("#3333CC"))
        self.box.padding = "20dp","10dp","20dp","0dp"
        self.subbox= MDBoxLayout(
                                md_bg_color=rgba("#FFFFFF"),
                                orientation="horizontal",
                                pos_hint={'center_x':0.5,'bottom':1}
                                 )
        self.sidebar = SideBar()
        self.subbox.add_widget(self.sidebar)
        self.centerbar = CenterBar()
        self.subbox.add_widget(self.centerbar)
        self.box.add_widget(self.subbox)
        

        return self.box
    
    def Export_ADUsers_clicked(self):
        self.centerbar.ids.sm.current = _export_adusers
        
    def ADUsers_clicked(self):
        self.centerbar.ids.sm.current = _adusers


print(__name__)
app = ITX_AD()
app.run()
# if __name__ =="__main__":
#     app = ITX_AD()
#     app.run()
    



# ListItemWithCheckbox:
#     text:"[size=14]Text[/size]"
#     secondary_text: "[size=14]Secondary text here[/size]"
# ListItemWithCheckbox:
#     text: "[size=14]Two-line item[/size]"
#     secondary_text: "[size=14]Secondary text here[/size]"
# ListItemWithCheckbox:
#     text: "[size=14]Two-line item[/size]"
#     secondary_text: "[size=14]Secondary text here[/size]"
    






    # def group_click(self):
    #     temp_list = [{"name":"G1","dn":"CN=G1,DC=ITX,DC=com"},{"name":"G2","dn":"CN=G2,DC=ITX,DC=com"},{"name":"G3","dn":"CN=G3,DC=ITX,DC=com"}]
        
    #     if self.ou_dialog:# this checks ou_dialog created or not.
            
    #         if self.prev_ou_state==self.ou_dialog.get_checked_item():
    #             print(self.prev_ou_state,self.ou_dialog.get_checked_item())
    #             print("prev state same")
    #             self.create_group_dialog()
    #         else:
    #             t_list =[{"name":"s1","dn":"CN=s1,DC=ITX,DC=com"},{"name":"s1","dn":"CN=s1,DC=ITX,DC=com"}]
    #             if len(self.ou_dialog.get_checked_item())==0:#this condition creates all group objects of AD in filter
    #                 t_list = temp_list
    #             print("prev state change")
    #             '''{
    #                 get data from ou_dialog.checked_data and create t_list as required.
    #             }'''
                
    #             self.group_dialog=None
    #             self.create_group_dialog(t_list)
    #             self.prev_ou_state = list(self.ou_dialog.get_checked_item())
    #     else:# if ou_dialog not created it creates group dialog with all objects.
    #         self.create_group_dialog(temp_list)
            
        
    # def create_group_dialog(self,list_:list=None):
    #     if not self.group_dialog:
    #         filter_item = FilterItem(hint_text = "Search group")
    #         self.group_dialog = FilterDialog(
    #             size_hint=(0.5,None),
    #             content_cls=filter_item,
    #             type="custom",
    #             title="Filter Group",
    #             buttons=[
    #                     MDFlatButton(
    #                         text="OK",
    #                         theme_text_color="Custom",
    #                         text_color=rgba("#3333CC"),
    #                         on_release=lambda x: self.ok_click(2)
    #                     ),
    #                 ],
    #             )
    #         self.group_dialog.content_cls.data=list_ 
    #         self.group_dialog.content_cls.create_object_list()
    #         self.group_dialog.content_cls.add_items()
    #         self.group_dialog.content_cls.checked_data=list() 
    #     self.group_dialog.open()