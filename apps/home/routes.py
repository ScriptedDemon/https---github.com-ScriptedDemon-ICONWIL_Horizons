
import os
from apps.home import blueprint
from flask import render_template, request , flash, url_for, request, redirect
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.home.models import Model
from flask import send_file
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from flask import jsonify
from apps.authentication.forms import LoginForm, CreateAccountForm
import json
import ast
import asyncio
import signal
import sys

from flask import Markup
from dotenv import load_dotenv
load_dotenv()



@blueprint.route('/index')
@login_required
def index():
    
    Model_obj = Model()
    dash_data=Model_obj.getTask_details(current_user)
    return render_template('home/index.html', segment='index',data=dash_data)



@blueprint.route('/tasks' , methods = ['GET','POST'])
@login_required
def tasks():
    Model_obj = Model()
    Model_obj.tasks_db_init()
    Model_obj.store_category_db_init()
    try:
        if(request.args['view']):
            scan_id=request.args['view']
            print(scan_id)
            scan_data=Model_obj.getScan_id_details(current_user,scan_id)
            print(scan_data)
            return render_template('home/scan.html', segment='scans',data=scan_data)
    except:
        pass
    if request.method == 'POST':
        type_req= request.form['type']  
        
        if type_req =="task_create":
            try:
                EstimatedHrs= request.form['EstimatedHrs']  
                category_sub= request.form['category_sub']  
                taskName = request.form['taskName']  
                print(EstimatedHrs)
                Model_obj.store_tasks("TEACHER",taskName,EstimatedHrs,category_sub)
                tasks_data=Model_obj.getTask_details(current_user)
                flash("Task Create Successfully...", "success")
                return render_template('home/tasks.html', segment='tasks',data=tasks_data)
            except:
                flash("Failed to Create Tasks..", "error")
                tasks_data=Model_obj.getTask_details(current_user)
                return render_template('home/tasks.html', segment='tasks',data=tasks_data)

        if type_req =="category_create":
            try:
                catName= request.form['catName']  
                Model_obj.store_category("TEACHER",catName)
                tasks_data=Model_obj.getTask_details(current_user)
                flash("Category Create Successfully...", "success")
                return render_template('home/tasks.html', segment='tasks',data=tasks_data)
            except:
                flash("Failed to Create category..", "error")
                tasks_data=Model_obj.getTask_details(current_user)
                return render_template('home/tasks.html', segment='tasks',data=tasks_data)
    try:
        if(request.args['delete']):
            delete=request.args['delete']
            delete_res=Model_obj.Delete_Scan(current_user,delete)
            tasks_data=Model_obj.getTask_details(current_user)
            return render_template('home/tasks.html', segment='tasks',data=tasks_data)
    except:
        pass
    
    tasks_data=Model_obj.getTask_details(current_user)
    print(tasks_data)
    return render_template('home/tasks.html', segment='tasks',data=tasks_data)

@blueprint.route('/Utilization' , methods = ['GET','POST'])
@login_required
def Utilization():
    Model_obj = Model()
    Model_obj.active_tasks_db_init()
    try:
        if(request.args['Add_active_tasks']):
            try:
                task_id=request.args['Add_active_tasks']
                print(task_id)
                Model_obj.add_active_tasks(current_user,task_id)
                tasks_data=Model_obj.getUtilization_details(current_user)
                flash("Task Added Successfully...", "success")
                return render_template('home/Utilization.html', segment='Utilization',data=tasks_data)
            except:
                flash("Failed to Add Tasks..", "error")
                tasks_data=Model_obj.getUtilization_details(current_user)
                return render_template('home/Utilization.html', segment='Utilization',data=tasks_data)

    except:
        pass

    if request.method == 'POST':
        type_req= request.form['type']  
        if type_req =="tracker_update":
            try:
                task_name= request.form['task_name'] 
                usedhrs= request.form['usedhrs']   
                Model_obj.update_active_hrs(current_user,task_name,usedhrs)
                tasks_data=Model_obj.getUtilization_details(current_user)
                flash("Tracker updated Successfully...", "success")
                return render_template('home/Utilization.html', segment='Utilization',data=tasks_data)
            except:
                flash("Failed to update tracker..", "error")
                tasks_data=Model_obj.getUtilization_details(current_user)
                return render_template('home/Utilization.html', segment='Utilization',data=tasks_data)
        
        if type_req =="task_create":
            try:
                EstimatedHrs= request.form['EstimatedHrs']  
                category_sub= request.form['category_sub']  
                taskName = request.form['taskName']  
                Model_obj.store_tasks(current_user,taskName,EstimatedHrs,category_sub)
                tasks_data=Model_obj.getUtilization_details(current_user)
                flash("Task Create Successfully...", "success")
                return render_template('home/Utilization.html', segment='Utilization',data=tasks_data)
            except:
                flash("Failed to Create Tasks..", "error")
                tasks_data=Model_obj.getUtilization_details(current_user)
                return render_template('home/Utilization.html', segment='Utilization',data=tasks_data)

    Utilization_data=Model_obj.getUtilization_details(current_user)
    return render_template('home/Utilization.html', segment='Utilization',data=Utilization_data)


@blueprint.route('/api/v1/status_update', methods = ['POST'])
def status_update_db():
    try:
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            json_out = request.json
            print(json_out["query"])
            Model_obj = Model()
            Model_obj.scans_db_engine_update(json_out["query"])
            data = {"Success" : "Succesfully updated status"}
            return jsonify(data)
            
    except:
        data = {"Failed" : "Failed to update status"}
        return jsonify(data)
      

def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
