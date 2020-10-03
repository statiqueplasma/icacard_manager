from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.button import MDRectangleFlatButton
from kivy.core.window import Window
from kivy.metrics import dp
import sqlite3
import os




Window.size = (300,500)


class CreateScreen(Screen):
    def add_user(self):
        conn = sqlite3.connect('icacard.db')
        cur = conn.cursor()
        nom = self.ids.nom.text 
        prenom = self.ids.prenom.text
        tel =self.ids.tel.text
        nbr=self.ids.nbr.text
        print(nom,prenom,tel,nbr)   
        cur.execute("INSERT INTO users VALUES (?,?,?,?,?)",(nom,prenom,'E-189',tel,nbr))
        conn.commit()
        conn.close()

class ManageStudents(Screen):
    pass
class Student_Code(Screen):
    pass
class CreateStudent(Screen):
    def add_student(self):
        conn = sqlite3.connect('icacard.db')
        cur = conn.cursor()
        nom = self.ids.stud_nom.text 
        prenom = self.ids.stud_prenom.text
        tel = self.ids.stud_tel.text
        print(code_mem)
        cur.execute("INSERT INTO students VALUES (?,?,?,?,?)",(nom,prenom,'E-200',tel,code_mem))
        conn.commit()
        conn.close()
        

class ManageUsers(Screen):
    pass
class Home(Screen):
    pass

sm = ScreenManager()

sm.add_widget(CreateScreen(name='create'))
sm.add_widget(Home(name='home'))
sm.add_widget(ManageStudents(name='manage_students'))
sm.add_widget(ManageUsers(name='manage_users'))
sm.add_widget(Student_Code(name='student_code'))
sm.add_widget(CreateStudent(name='create_stud'))




class MainApp(MDApp):
    conn = sqlite3.connect('icacard.db')
    cur = conn.cursor()     

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    def build(self):
        
        screen = Screen()

        self.help_str = Builder.load_file("main.kv")

        
        screen.add_widget(self.help_str)
        users_tables = MDDataTable(
                        pos_hint={'center_x':0.5,'center_y':0.5},
                        size_hint=(1, 1),
                        use_pagination=True,
                        check=True,
                        column_data=[
                            ("Nom", dp(30)),
                            ("Prenom", dp(30)),
                            ("Code", dp(30)),
                            ("Tel", dp(30)),
                            ("Nombre d'étudiants", dp(30)),
                        ],
                        row_data = self.users,
                    )
        
        users_tables.bind(on_check_press = self.user_check_press)
        users_tables.bind(on_row_press = self.row_press)

        students_tables = MDDataTable(
                        pos_hint={'center_x':0.5,'center_y':0.5},
                        size_hint=(1, 1),
                        use_pagination=True,
                        check=True,
                        column_data=[
                            ("Nom", dp(30)),
                            ("Prenom", dp(30)),
                            ("Code", dp(30)),
                            ("Tel", dp(30)),
                            ("code paraints", dp(30)),
                        ],
                        row_data = self.students
                    )
        
        students_tables.bind(on_check_press = self.check_press)
        students_tables.bind(on_row_press = self.row_press)


        self.help_str.ids.screen_manager.get_screen('manage_users').children[0].add_widget(users_tables)
        self.help_str.ids.screen_manager.get_screen('manage_students').add_widget(students_tables)
            
        
        return screen
    def user_check_press(self,instance_table,current_row):
        self.help_str.ids.screen_manager.get_screen('student_code').ids.box_layout.clear_widgets()
        conn = sqlite3.connect('icacard.db')
        cur = conn.cursor()   
        code = current_row[2]
        cur.execute("SELECT nom,prénom,code,tel FROM students WHERE code_affilié= ?",(code,))
        stud_per_code = cur.fetchall()

        self.stud_code_tables = MDDataTable(
                        pos_hint={'center_x':0.5,'center_y':0.5},
                        size_hint=(1, 1),
                        use_pagination=True,
                        check=True,
                        column_data=[
                            ("Nom", dp(30)),
                            ("Prenom", dp(30)),
                            ("Code", dp(30)),
                            ("Tel", dp(30)),
                        ],
                        row_data = stud_per_code,
                    )
        
        self.stud_code_tables.bind(on_check_press = self.check_press)
        self.stud_code_tables.bind(on_row_press = self.row_press)

        self.help_str.ids.screen_manager.get_screen('student_code').ids.stud_code_title.text = code
        global code_mem
        code_mem = code
        print(code_mem)
        self.help_str.ids.screen_manager.get_screen('student_code').ids.box_layout.add_widget(self.stud_code_tables)
        self.help_str.ids.screen_manager.current = "student_code"
        
        
    def check_press(self,instance_table,current_row):
        pass
    def row_press(self,instance_table,current_row):
        pass

    conn.commit()
    conn.close()   
    

if __name__== "__main__":
    MainApp().run()