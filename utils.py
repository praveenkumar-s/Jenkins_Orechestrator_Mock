Queries = {
    "insert_job": "insert into data (project , job , parameters , CreatedAt , status, uuid ) values (?,?,?,?,?,?)",
    "get_build_id":"select ID from data where uuid =?",
    "get_build_by_id":"select * from data where id = ?",
    "update_status":"update data set status = ?, EndTime=? where ID =?",
    "get_status":"select project,job,status,createdAt, EndTime from data where ID=?"
}



def search_job( project , job):
    for items in project['jobs']:
        if(items['name']==job):
            return items
    return None

