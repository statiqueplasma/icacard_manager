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



s_code = "E-123"
u_code = "E-123"

class CreateScreen(Screen):
    def add_user(self):
        conn = sqlite3.connect('icacard.db')
        cur = conn.cursor()
        nom = self.ids.nom.text 
        prenom = self.ids.prenom.text
        tel =self.ids.tel.text
        nbr=self.ids.nbr.text
        #############################################################----------------------still need date------------------------#######################################################################
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
        #############################################################----------------------still need date------------------------#######################################################################
        cur.execute("INSERT INTO students VALUES (?,?,?,?,?)",(nom,prenom,'E-200',tel,u_code))
        conn.commit()
        conn.close()
        
class ManageUsers(Screen):
    pass
class Home(Screen):
    pass

class StudentProfile(Screen):
    def viewStudProfile(self):
        conn = sqlite3.connect('icacard.db')
        cur = conn.cursor()
        #############################################################----------------------still need date------------------------#######################################################################     
        cur.execute("SELECT nom,prénom,tel,code,code_affilié FROM students WHERE code=?",(s_code,))
        stud = cur.fetchall()
        self.ids.profil_s_nom.text = stud[0][0]
        self.ids.profil_s_prenom.text = stud[0][1]
        self.ids.profil_s_tel.text = str(stud[0][2])
        self.ids.profil_s_code.text = stud[0][3]
        self.ids.profil_s_par.text = stud[0][4]
        u_code = stud[0][4]
        cur.execute("SELECT nom,prénom FROM users WHERE code=?",(stud[0][4],))
        users = cur.fetchall()
        self.ids.profil_s_par_nom.text = users[0][0]
        self.ids.profil_s_par_prenom.text = users[0][1]
        conn.commit()
        conn.close()
        

class UserProfile(Screen):
    def viewUserProfile(self):
        conn = sqlite3.connect('icacard.db')
        cur = conn.cursor()
        #############################################################----------------------still need date------------------------#######################################################################     
        cur.execute("SELECT nom,prénom,tel,code,nombre_etudiants FROM users WHERE code=?",(u_code,))
        users = cur.fetchall()
        print(u_code)
        print(users)
        self.ids.profil_u_nom.text = users[0][0]
        self.ids.profil_u_prenom.text = users[0][1]
        self.ids.profil_u_tel.text = str(users[0][2])
        self.ids.profil_u_code.text = u_code
        self.ids.profil_u_nbr.text = str(users[0][4])
        conn.commit()
        conn.close()

sm = ScreenManager()

sm.add_widget(CreateScreen(name='create'))
sm.add_widget(Home(name='home'))
sm.add_widget(ManageStudents(name='manage_students'))
sm.add_widget(ManageUsers(name='manage_users'))
sm.add_widget(Student_Code(name='student_code'))
sm.add_widget(CreateStudent(name='create_stud'))
sm.add_widget(StudentProfile(name='student_profile'))
sm.add_widget(UserProfile(name='user_profile'))




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
        u_code = code

        self.help_str.ids.screen_manager.get_screen('student_code').ids.box_layout.add_widget(self.stud_code_tables)
        self.help_str.ids.screen_manager.current = "student_code"
        
        
    def check_press(self,instance_table,current_row):
        s_code = current_row[2]
        self.help_str.ids.screen_manager.get_screen('student_profile').viewStudProfile()          
        self.help_str.ids.screen_manager.current = "student_profile"

    def row_press(self,instance_table,current_row):
        pass

    conn.commit()
    conn.close()   
    

if __name__== "__main__":
    MainApp().run()