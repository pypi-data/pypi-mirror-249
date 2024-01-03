import requests, json
from dateutil import tz
from datetime import datetime
from Task import Task,TodoistStatus
from User import User

#Define the API parameters
Base_URL = 'https://api.notion.com/v1'


#Define the headers
def getHeader(APIKey) :
    headers_data = {
        "Authorization" : APIKey,
        "Notion-version" : "2022-02-22",
        "Content-Type" : "application/json"
    }
    return headers_data

def CreateOrUpdateNotionAction(Todoist_Task: Task, NotionUser:User=None, Notion_DB_ID:str=None) -> str :

    #When there is only the Task, get the task's related user
    if (NotionUser is None): NotionUser = User.getUser(Todoist_Task.user_name)
    user_notion_technical_parameters = NotionUser.get_notion_technical_parameters()
    headers_data = getHeader(user_notion_technical_parameters['Notion_API_key'])

    #When there is no Notion_DB_ID specified, use the default one recorded for the user
    if Notion_DB_ID is None : Notion_DB_ID = user_notion_technical_parameters['Notion_Default_DB_ID']

    #Check if Notion action exists
    NotionExistingTask = getTask(NotionUser,todoistID=Todoist_Task.todoist_task_id)

    JSONstatement = {
            "parent": {
                "database_id": Notion_DB_ID
            },
            "icon": {
                "type": "external",
                "external": {
                    "url": "https://www.notion.so/icons/add_gray.svg"
                }
            },
            "properties": {
                "Status": {
                    "type": "select",
                    "select": {
                        "name": Task.get_notion_status(Todoist_Task.status).value
                    }
                },
                "Priority": {
                    "type": "select",
                    "select": {
                        "name": Task.get_notion_priority(Todoist_Task.priority).value
                    }
                },
                "TodoistID" : {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": str(Todoist_Task.todoist_task_id)
                            }
                        }
                    ]
                },
                "Todoist_ProjectID" : {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": str(Todoist_Task.todoist_project_id)
                            }
                        }
                    ]
                },
                "Action": {
                    "id": "title",
                    "type": "title",
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": Todoist_Task.content
                            }
        
                        }
                    ]
                },
                "Delegated": {
                    "checkbox" : Todoist_Task.delegation
                }, 
                "URL":{
                    "url": Todoist_Task.url
                }
            }
        }

    if Todoist_Task.due is not None:
        Todoist_Task.due = datetime.fromisoformat(Todoist_Task.due).replace(tzinfo=tz.gettz("Europe/Paris")).isoformat()
        JSONstatement['properties']['Due date'] = {
            "type": "date",
            "date": {
                "start": Todoist_Task.due
            }
        }
    else:
        JSONstatement['properties']['Due date'] = {
            "type": "date",
            "date": None
        }

    if (Todoist_Task.status == TodoistStatus.CLOSED.value):
        JSONstatement['icon'] = {
             "type": "external",
             "external": {
                 "url": "https://www.notion.so/icons/checkmark_green.svg"
             }
         }
        

    #Pas de gestion des parents pour le moment
    
    # if Todoist_Task.todoist_parent_id is not None:
    #     NotionParentTask = FindNotionAction(Todoist_Task.todoist_parent_id, NotionUser)
    #     if NotionParentTask is not None : 
    #         JSONstatement['properties']['Parent'] = {
    #             "relation": [
    #                 {
    #                 "id": NotionParentTask.notion_task_id
    #                 }
    #             ]
    #         }

    new_line = json.dumps(JSONstatement)
    response = None
    #Compare
    
    if NotionExistingTask is not None:
        if not Todoist_Task == NotionExistingTask :
            response = requests.patch(f"{Base_URL}/pages/{NotionExistingTask.notion_task_id}", data=new_line,headers=headers_data)
            task_created = response.json()

        else:
            return Todoist_Task.todoist_task_id

    else : 
        #create the task
        response = requests.post(f"{Base_URL}/pages", data=new_line, headers=headers_data)
        task_created = response.json()

    #If there is a positive responses, return the Notion taks ID. Otherwise return None
    if response.status_code == 200: 
        return task_created['id']
    else:
        return None

def getTask(user:User, notionID:str=None, todoistID=None):
    user_notion_technical_parameters = user.get_notion_technical_parameters()
    headers_data = getHeader(user_notion_technical_parameters['Notion_API_key'])
    response = None
    
    if notionID is not None :
        #In the case we get the task with a notion ID
        response = requests.get(f"{Base_URL}/pages/{notionID}", headers=headers_data)
        return Task.fromNotionJSON(response.json(), user.UserName)

        #In the case we get the task with a todoist ID
    elif notionID is None and todoistID is not None:
        NotionAction = {} #Initiate my dict
        JSONstatement = {
            "filter" : {
                "property" : "TodoistID",
                "rich_text" : {
                    "equals" : str(todoistID)
                }
            }
        }
    
        filter = json.dumps(JSONstatement)
        databaseID = user_notion_technical_parameters['Notion_Default_DB_ID']
        response = requests.post(f"{Base_URL}/databases/{databaseID}/query", data=filter, headers=headers_data)
        NotionTaskJSON = response.json()

        if response.status_code == 200:
            if len(NotionTaskJSON["results"])==1: return Task.fromNotionJSON(NotionTaskJSON['results'][0], user.UserName)
            else: return None
        else : return None

# def DeleteTask(TodoistTask,NotionUser:User):
#     #Search for Notion task based on todoist ID
#     NotionTask = FindNotionAction(TodoistTask.todoist_task_id)
#     headers_data = getHeader(NotionUser.notionApikey)

#     if NotionTask is not None:
#         response = requests.delete(f"{Base_URL}/blocks/{NotionTask.notion_task_id}", headers=headers_data)
#         task_deleted = response.json()

#         if response.status_code == 200:
#             logging.info(f"[NotionAPI] Notion task deleted. ID = {task_deleted['id']}")
#             Log("[DELETE]","[NotionAPI]", TodoistTask)
#             return task_deleted['id']
#         else:
#             logging.info(f"[NotionAPI] issue with the deletion of the task. {task_deleted['content']}")
#             return None
#     else:
#         return None