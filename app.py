from flask import Flask
from flask import request
import json
import sqlite3
import utils
from datetime import datetime, timedelta
from flask import jsonify
from uuid import uuid1
import time
app = Flask(__name__)


import jenkins


job_templates  = json.load(open('jobtemplates.json', 'r') )

@app.route('/api/<project>/<job>/start',methods =['POST'])
def start(project, job):
    incoming_data = request.get_json()
    row=-1
    try:
        job_details  = utils.search_job(job_templates[project] , job)
        if(job_details is None):
            return 'job not found',404
        else:
            uuid = str(uuid1())
            conn = sqlite3.connect('cache.db')
            cursor = conn.cursor()
            cursor.execute(utils.Queries['insert_job'], (project , job , json.dumps(incoming_data) , datetime.now(), 'started', uuid))
            cursor.execute(utils.Queries['get_build_id'], (uuid,) )
            row = cursor.fetchone()[0]
            conn.commit()
            conn.close()    
    except:
        pass
    return jsonify({'id':row})

@app.route('/api/<project>/<job>/<build_number>/status',methods = ['GET'])
def get_status(project, job, build_number):
    running_time =  utils.search_job( job_templates[project] , job )['running_time']
    
    conn  = sqlite3.connect('cache.db')
    cursor = conn.cursor()
    cursor.execute(utils.Queries['get_build_by_id'], (build_number , ) )
    
    rows = cursor.fetchone()
    if(running_time is None or len(rows)==0 or rows[1]!=project or rows[2]!=job):
        conn.close()
        return "data not found",404
    created_at= datetime.strptime( rows[4] , "%Y-%m-%d %H:%M:%S.%f" )
    if(datetime.now() >= created_at+timedelta(minutes = running_time) and rows[5] not in ('completed','aborted')):
        cursor.execute(utils.Queries['update_status'] , ('completed' ,datetime.now(), build_number))
        conn.commit()
    cursor.execute(utils.Queries['get_status'] , (build_number,))
    data = cursor.fetchall()

    conn.close()
    
    return jsonify({
        "project":data[0][0],
        "job":data[0][1],
        "status":data[0][2],
        "created_at":data[0][3],
        "completed_at":data[0][4]
    })


@app.route('/api/<project>/<job>/<build_number>/stop', methods = ['GET'])
def stop(project, job , build_number):
    conn  = sqlite3.connect('cache.db')
    cursor = conn.cursor()
    cursor.execute(utils.Queries['get_build_by_id'], (build_number , ) )
    rows = cursor.fetchone()
    if(len(rows)==0 or rows[1]!=project or rows[2]!=job):
        conn.close()
        return "data not found",404
    else:
        cursor.execute(utils.Queries['update_status'] , ('aborted' ,datetime.now(), build_number))
        conn.commit()
    cursor.execute(utils.Queries['get_status'] , (build_number,))
    data = cursor.fetchall()

    conn.close()
    
    return jsonify({
        "project":data[0][0],
        "job":data[0][1],
        "status":data[0][2],
        "created_at":data[0][3],
        "completed_at":data[0][4]
    })
    
@app.route('/api/projects',methods=['GET'])
def get_projects():
    projects={"projects":[]}
    for items  in job_templates.keys():
        projects['projects'].append(items)
    return jsonify(projects)

@app.route('/api/projects/<project>/jobs' , methods=['GET'])
def get_jobs_for_project(project):
    if(project in job_templates.keys()):
        return jsonify(job_templates[project])
    else:
        return "project not found",404

@app.route('/api/projects/<project>/<jobs>', methods=['GET'])
def get_builds_for_job(project , jobs):
    out_data ={
        "project":project,
        "job":{
            "name":jobs,
            "builds":[]
        }
    }
    conn=sqlite3.connect('cache.db')
    cursor = conn.cursor()
    cursor.execute(utils.Queries['get_builds_for_job'], (jobs , project) )
    result_set = cursor.fetchall()
    for items in result_set:
        out_data['job']['builds'].append({
            "ID":items[0],
            "status":items[1],
            "createdAt":str(items[2]),
            "endTime":str(items[3])
        })
    conn.close()
    return jsonify(out_data)

if __name__ == '__main__':
    app.run()
