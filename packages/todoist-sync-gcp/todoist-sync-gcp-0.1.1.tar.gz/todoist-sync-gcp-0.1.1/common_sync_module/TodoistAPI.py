from Task import Task, TodoistStatus
from User import User
import uuid, requests, json

Base_URL = "https://api.todoist.com/rest/v2"
DELEGATED_LABEL = "delegated_🚀"
ON_GOING_LABEL = "On-Going"
WAITING_LABEL = "Waiting"


def getHeader(APIKey) :
    headers_data = {
        "Authorization" : f"Bearer {APIKey}",
        "X-Request-Id" : str(uuid.uuid4()),
        "Content-Type" : "application/json"
    }
    return headers_data

def CreateOrUpdateTodoistAction(myTask: Task, TodoistUser:User=None, TodoistProjectID:str=None) -> str :
    
    #When there is only the Task, get the task's related user
    if (TodoistUser is None): TodoistUser = User.getUser(myTask.user_name)
    user_notion_technical_parameters = TodoistUser.get_todoist_technical_parameters()
    headers_data = getHeader(user_notion_technical_parameters['Todoist_API_Key'])

    #When there is no Notion_DB_ID specified, use the default one recorded for the user
    if TodoistProjectID is None : TodoistProjectID = user_notion_technical_parameters['Todoist_default_Project']

    JsonStatement = {
        'project_id': str(TodoistProjectID),
        'priority': myTask.priority,
        'content': myTask.content,
        'due_datetime': myTask.due,
    }
    labels = []
    if (myTask.status == TodoistStatus.ON_GOING.value) : labels.append(ON_GOING_LABEL)
    if (myTask.delegation == True): labels.append(DELEGATED_LABEL)
    JsonStatement['labels'] = labels

    if (myTask.todoist_parent_id is not None):JsonStatement['parent_id'] = str(myTask.todoist_parent_id) #Not allowed on the API for Update.
    else: JsonStatement['parent_id'] = None
    
    print(JsonStatement)

    task_json = json.dumps(JsonStatement)
    response = ""

    #Check if task need to be created or updated
    match myTask.event_name:
        case "Task_Add": response = requests.post(f"{Base_URL}/tasks", data=task_json, headers=headers_data)
        case "Task_Update": response = requests.post(f"{Base_URL}/tasks/{myTask.todoist_task_id}", data=task_json, headers=headers_data)
        case "Task_Complete": response = requests.post(f"{Base_URL}/tasks/{myTask.todoist_task_id}/close", headers=headers_data)
        case "Task_Delete": response = requests.delete(f"{Base_URL}/tasks/{myTask.todoist_task_id}", headers=headers_data)
        case _ :
            return
    #prise en compte à prévoir des delete

    return response

def getTask(user:User, todoistID=None):
    pass