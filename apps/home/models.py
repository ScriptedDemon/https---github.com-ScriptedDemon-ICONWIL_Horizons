import json
import sys, os
import sqlite3
import datetime
import uuid
import json
import os
import shutil
DB_FOLDER = "./apps/DB/"

class Model:
    def __init__(self):
        self.nama = "Coding"

    def tasks_db_init(self):
        try:
            conn = sqlite3.connect(DB_FOLDER+'tasks.db')
            conn.execute('''CREATE TABLE tasks
                    (ID TEXT PRIMARY KEY     NOT NULL,
                    EstimatedHrs           int    NOT NULL,
                    category_sub           TEXT    NOT NULL,
                    taskName           TEXT    NOT NULL,
                    customer TEXT NOT NULL,
                    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);''')
            conn.commit()
            print ("tasks Table created successfully")
            conn.close()
        except:
            pass

    def store_category_db_init(self):
        try:
            conn = sqlite3.connect(DB_FOLDER+'tasks.db')
            conn.execute('''CREATE TABLE category
                    (ID TEXT PRIMARY KEY     NOT NULL,
                    category           TEXT    NOT NULL,
                    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);''')
            conn.commit()
            print ("tasks Table created successfully")
            conn.close()
        except:
            pass
    
    def active_tasks_db_init(self):
        try:
            conn = sqlite3.connect(DB_FOLDER+'tasks.db')
            conn.execute('''CREATE TABLE active_tasks
                    (ID TEXT PRIMARY KEY     NOT NULL,
                    customer TEXT NOT NULL,
                    remaining_hrs int NOT NULL,
                    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);''')
            conn.commit()
            print ("tasks Table created successfully")
            conn.close()
        except:
            pass

    def store_tasks(self,current_user,taskName,EstimatedHrs,category_sub):
        ID=uuid.uuid4().hex
        try:
            print ("Records creating")
            conn = sqlite3.connect(DB_FOLDER+'tasks.db')
            currentDateTime = datetime.datetime.now()
            print (currentDateTime)
            conn.execute("insert into tasks values(?,?,?,?,?,?)",(ID, EstimatedHrs,str(category_sub),str(taskName),str(current_user),currentDateTime))
            conn.commit()
            print ("Records created successfully")
            conn.close()
            return 1
        except:
            return -1
            
    def store_category(self,current_user,catName):
        ID=uuid.uuid4().hex
        print ("Records creating")
        conn = sqlite3.connect(DB_FOLDER+'tasks.db')
        currentDateTime = datetime.datetime.now()
        print (currentDateTime)
        conn.execute("insert into category values(?,?,?,?)",(ID,str(catName),str(current_user),currentDateTime))
        conn.commit()
        print ("Records created successfully")
        conn.close()
        return 1

    def add_active_tasks(self,current_user,task_id):
        ID=task_id
        print ("Records creating")
        conn = sqlite3.connect(DB_FOLDER+'tasks.db')
        currentDateTime = datetime.datetime.now()
        print (currentDateTime)
        conn.execute("insert into active_tasks values(?,?,?,?)",(ID,str(current_user),0,currentDateTime))
        conn.commit()
        print ("Records created successfully")
        conn.close()
        return 1
    def update_active_hrs(self,current_user,task_id,used_hrs):
        ID=task_id
        print("dhdh")
        print(used_hrs)
        conn = sqlite3.connect(DB_FOLDER+'tasks.db')
        cur = conn.cursor()
        cur.execute("select * from active_tasks where ID="+"'"+str(task_id)+"'")
        rows = cur.fetchall()
        conn.close()
        
        
        for row in rows:
            print(row[2])
            EstimatedHrs=row[2]
            used_hrs=int(EstimatedHrs)+int(used_hrs)
        print(used_hrs)
        conn = sqlite3.connect(DB_FOLDER+'tasks.db')
        cursor = conn.cursor()
        update_query = """
        UPDATE active_tasks
        SET remaining_hrs = ?
        WHERE ID = ?
        """
        try:
            cursor.execute(update_query, (used_hrs,ID))
            conn.commit()
            print("Record updated successfully")
        except sqlite3.Error as error:
            print("Error occurred:", error)
        return 1

    def getTask_details(self,customer):
        conn = sqlite3.connect(DB_FOLDER+'tasks.db')
        cur = conn.cursor()
        cur.execute("select * from tasks where customer="+"'"+str("TEACHER")+"'")
        rows = cur.fetchall()
        conn.close()
        data=[]
        for row in rows:
            tmp={}
            tmp["ID"]=row[0]
            tmp["EstimatedHrs"]=row[1]
            tmp["category_sub"]=row[2]
            tmp["taskName"]=row[3]
            data.append(tmp)
        conn = sqlite3.connect(DB_FOLDER+'tasks.db')
        cur = conn.cursor()
        cur.execute("select * from category where customer="+"'"+str("TEACHER")+"'")
        rows = cur.fetchall()
        conn.close()
        category=[]
        for row in rows:
            category.append(row[1])
        final_data={}
        final_data["tasks"]=data
        final_data["category"]=category
        return final_data

    def getUtilization_details(self,customer):
        conn = sqlite3.connect(DB_FOLDER+'tasks.db')
        cur = conn.cursor()
        cur.execute("select * from active_tasks where customer="+"'"+str(customer)+"'")
        rows = cur.fetchall()
        conn.close()
        
        active_tmp=[]
        active_hrs=[]
        for row in rows:
            tmp={}
            tmp["ID"]=row[0]
            tmp["EstimatedHrs"]=row[2]
            active_tmp.append(row[0])
            active_hrs.append(tmp)
        active_tasks=[]
        conn = sqlite3.connect(DB_FOLDER+'tasks.db')
        cur = conn.cursor()
        cur.execute("select * from tasks where customer="+"'"+str("TEACHER")+"'")
        rows = cur.fetchall()
        conn.close()
        data=[]
        for row in rows:
            tmp={}
            tmp["ID"]=row[0]
            tmp["EstimatedHrs"]=row[1]
            tmp["category_sub"]=row[2]
            tmp["taskName"]=row[3]
            if tmp["ID"] in active_tmp:
                for i in active_hrs:
                    print(i["ID"])
                    print(i["EstimatedHrs"])
                    if i["ID"]==tmp["ID"]:
                        cal= int(row[1])-int(i["EstimatedHrs"])
                        tmp["remaining_hrs"]=cal
                        active_tasks.append(tmp)

            else:
                data.append(tmp)
        conn = sqlite3.connect(DB_FOLDER+'tasks.db')
        cur = conn.cursor()
        cur.execute("select * from tasks where customer="+"'"+str(customer)+"'")
        rows = cur.fetchall()
        conn.close()
        for row in rows:
            tmp={}
            tmp["ID"]=row[0]
            tmp["EstimatedHrs"]=row[1]
            tmp["category_sub"]=row[2]
            tmp["taskName"]=row[3]
            if tmp["ID"] in active_tmp:
                for i in active_hrs:
                    if i["ID"]==tmp["ID"]:
                        cal= int(row[1])-int(i["EstimatedHrs"])
                        tmp["remaining_hrs"]=cal
                        active_tasks.append(tmp)
            else:
                data.append(tmp)
        conn = sqlite3.connect(DB_FOLDER+'tasks.db')
        cur = conn.cursor()
        cur.execute("select * from category where customer="+"'"+str("TEACHER")+"'")
        rows = cur.fetchall()
        conn.close()
        
        category=[]
        for row in rows:
            category.append(row[1])
        
        conn = sqlite3.connect(DB_FOLDER+'tasks.db')
        cur = conn.cursor()
        cur.execute("select * from category where customer="+"'"+str(customer)+"'")
        rows = cur.fetchall()
        conn.close()
        
        category=[]
        for row in rows:
            category.append(row[1])
        

        final_data={}
        final_data["tasks"]=data
        final_data["active_tasks"]=active_tasks
        final_data["category"]=category

        return final_data
    
  