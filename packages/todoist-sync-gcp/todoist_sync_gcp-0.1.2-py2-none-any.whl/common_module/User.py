from dataclasses import dataclass
from google.cloud import bigquery

client = bigquery.Client(project="notionsync-397719") #à mettre en variable d'environnement

@dataclass
class User:
    todoist_ID: int=None
    notion_ID: str=None
    UserName: str=None

    @classmethod
    def getUser(cls, name:str=None, todoist_id:int=None,notion_id:str=None):
        if (name is not None) : 
            query = "select * from `User_sync.User` where Name = @name"
            query_param = "name"
            query_param_type = "STRING"
            query_value = name
        elif (todoist_id is not None):
            query = "select * from `User_sync.User` where Todoist_User_Id = @todoist_id"
            query_param = "todoist_id"
            query_param_type = "INT64"
            query_value = todoist_id
        elif (notion_id is not None):
            query = "select * from `User_sync.User` where Notion_User_Id = @notion_id"
            query_param = "notion_id"
            query_param_type = "STRING"
            query_value = notion_id
        else : return cls()

        users = User.__request_big_query__(query,[query_param],[query_param_type],[query_value])
        if (users is not None):return cls(todoist_ID=users[0]['Todoist_User_Id'], notion_ID=users[0]['Notion_User_Id'], UserName=users[0]['Name'])
        else : return cls()


    def getTodoistSynchronizedProjects(self):
        projects = []
        query = """select distinct Todoist_Project_Id from `User_sync.Synchonization`
         inner join `User_sync.Todoist_Projects` on `User_sync.Todoist_Projects`.Project_Id = `User_sync.Synchonization`.Todoist_Project_Id
        where `User_sync.Todoist_Projects`.Todoist_User_Id = @todoist_user_id"""
    
        results = User.__request_big_query__(query,['todoist_user_id'], ['INT64'], [self.todoist_ID])
        if results is not None : 
            for row in results:
                projects.append(row['Todoist_Project_Id'])
            return projects

    def getNotionSynchronizedDB(self):
        projects = []
        query = """select distinct `User_sync.Synchonization`.Notion_Database_Id from `User_sync.Synchonization`
        inner join `User_sync.Notion_Databases` on `User_sync.Notion_Databases`.Notion_Database_Id = `User_sync.Synchonization`.Notion_Database_Id
        where `User_sync.Notion_Databases`.Notion_User_Id = @notion_user_id"""
    
        results = User.__request_big_query__(query,['notion_user_id'], ['STRING'], [self.notion_ID])
        if results is not None : 
            for row in results:
                projects.append(row['Notion_Database_Id'])
            return projects

    def get_notion_technical_parameters(self):
        DB = []
        query = """select Notion_Default_DB_ID, Notion_API_key from `User_sync.Notion_User`
        inner join `User_sync.User` on `User_sync.Notion_User`.Notion_User_Id = `User_sync.User`.Notion_User_Id
        where `User_sync.User`.Name = @user_name"""
    
        results = User.__request_big_query__(query,['user_name'], ['STRING'], [self.UserName])
        if results is not None : 
            for row in results:
                DB.append(row)
            return DB[0]
        
    def get_todoist_technical_parameters(self):
        DB = []
        query = """select Todoist_API_Key, Todoist_default_Project  from `User_sync.Notion_User`,`User_sync.Todoist_User`
        inner join `User_sync.User` on `User_sync.Todoist_User`.Todoist_Id = `User_sync.User`.Todoist_User_Id
        where `User_sync.User`.Name = @user_name"""
    
        results = User.__request_big_query__(query,['user_name'], ['STRING'], [self.UserName])
        if results is not None : 
            for row in results:
                DB.append(row)
            return DB[0]

    def __request_big_query__(query:str,parameter_name:list, parameter_type:list, parameter_value:list):
        query_results=[]
        if len(parameter_name) == len(parameter_type) == len(parameter_value):
            query_parameters = []
            for i in range(len(parameter_name)):
                query_parameters = [bigquery.ScalarQueryParameter(parameter_name[i],parameter_type[i], parameter_value[i])]

            job_config = bigquery.QueryJobConfig(query_parameters=query_parameters)
            query_job = client.query(query, job_config=job_config)

            if (query_job.result().total_rows != 0):
                for row in query_job:
                    query_results.append(row)
                return query_results
            else: return

    