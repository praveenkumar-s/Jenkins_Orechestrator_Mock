# Jenkins Orchestrator Mock Service
#### This project is helps to test orchestrator with Jenkins without the need for having an actual Jenkins server
#### This helps us to easily configure and simulate events as in Jenkins server quickly

### Components:
#### - Server
#### - Client Library


### Server: 
     An instance of the jenkins server that can start / stop / get status of builds

#### Create a project:
    Each project is a key on the Jobtemplates.json file. Add a key there to create a project

#### Create a job:
    Jobs can be created under the jobs[] of the project in the Jobtemplates.json file. Job can store the name, running time and params that needs to be passed to the job

#### To Start the server:
    python app.py

### Client Library:
    To create an instance of the client, copy the fakejenkins.py file to the root directory and use:

    import fakeJenkins
    server = fakeJenkins.jenkins(<url of jenkins server>, <user>, <password>)
    #if url is local host , use http://127.0.0.1:5000/
#### To start a build:
   ##### Async:
        server.build_job(<job_name>,<project_name>(optional))
        #Async does not wait for the job to complete
        
   ##### Sync:
        server.build_job(<job_name>,<project_name>(optional),async_=False)
        #Sync returns control after the job execution is complete from jenkins
    
#### To Get Status of a Build:
        server.get_build_info(<job_name>,<build_number>,<project_name>(Optional))

#### To Abort a Build: 
        server.stop_build(<job_name>,<build_number>,<project_name>Optional)
    
#### To Get List of all projects:
        server.get_projects()
    
 #### To Get List of all jobs under a project:
        server.get_jobs(<project_name>Optional)
    
 #### To Get List of all builds and their status under a job:
        server.get_builds(<job_name>,<project_name>Optional)
        #Pagination is not implemented, when there are >10000 records performance may suffer
