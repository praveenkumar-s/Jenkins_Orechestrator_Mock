import requests
import urllib.parse
import time

class jenkins():
    def __init__(self,url , user=None , password=None, default_project_name ='project_panamera'):
        self.url= url
        self.default_project_name=default_project_name
    
    def build_job(self, job_name , project_name=None, parameters={}, async_=True):
        if(project_name is None):
            project_name = self.default_project_name
        url = urllib.parse.urljoin(self.url , 'api/projects/'+project_name+'/'+job_name+'/start')
        rs = requests.post(url = url , json= parameters)
        if(async_):
            return rs.json()
        else:
            id = rs.json()['id']
            status=self.get_status(job_name , id ,project_name ) 
            while( status == None or status['status'] =='started' ):
                time.sleep(10)                
                status=self.get_status(job_name , id ,project_name )
            return status
                
    def get_status(self, job_name ,build_number, project_name = None):
        if(project_name is None):
            project_name = self.default_project_name
        status_url = urllib.parse.urljoin(self.url , 'api/'+project_name+'/'+job_name+'/'+str(build_number)+'/status')
        rs = requests.get(status_url)
        if(rs.status_code == 200):
            return rs.json()
        else:
            return None
        
    def get_build_info(self, job_name , build_number , project_name = None):
        if(project_name is None):
            project_name = self.default_project_name
        return self.get_status(job_name , build_number , project_name)

    def stop_build(self, job_name , build_number , project_name=None):
        if(project_name is None):
            project_name = self.default_project_name
        stop_url = urllib.parse.urljoin(self.url , '/api/'+project_name+'/'+job_name+'/'+build_number+'/stop')
        rs = requests.get(stop_url)
        if(rs.status_code==200):
            return rs.json()
        else:
            return str(rs.status_code)+' : '+rs.content
