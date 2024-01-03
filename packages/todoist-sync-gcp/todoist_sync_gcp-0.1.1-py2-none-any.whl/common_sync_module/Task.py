from dataclasses import dataclass
import datetime, json
from dateutil import tz
from enum import Enum

DELEGATED_LABEL = "delegated_🚀"
ONGOING_LABEL = "On-Going"
WAITING_LABEL = "Waiting"

class NotionPriority(Enum):
    LOW = "Priority 4"
    MEDIUM = "Priority 3"
    HIGH = "Priority 2"
    CRITICAL = "Priority 1"

class TodoistPriority(Enum):
    LOW, MEDIUM, HIGH, CRITICAL = range(1, 5)

class NotionStatus(Enum):
    ON_GOING = "En cours"
    NOT_STARTED = "Non demarré"
    WAITING = "En attente"
    CLOSED = "Terminé"

class TodoistStatus(Enum):
    ON_GOING = "On-Going"
    NOT_STARTED = "Not started"
    WAITING = "Waiting"
    CLOSED = "Completed"


@dataclass
class Task:

    content:str
    user_name:str=None
    due:str = None
    priority:int = 4
    todoist_project_id:int = None
    todoist_task_id:int = None
    notion_task_id:str = None
    status:str = "Not started"
    delegation:bool =False
    event_name:str=None
    url:str=None
    notion_parent_id:str=None
    todoist_parent_id:int=None
    labels = []
    
    #STATUS - Valeurs possibles : "Not started" ; "On-Going" ; "Completed"
    if status == "On-Going" :
        labels.append("On-Going")
    elif status == "Waiting":
        labels.append("Waiting")
    elif status != "Not started" or status !="Completed":
        status = "Not started"

    #DUE - Available values : iso format with or without time.
    if due != None:
        if "Z" in due:
            due = datetime.strptime(due,'%Y-%m-%dT%H:%M:%SZ').isoformat()
        elif "T" in due:   
            due = datetime.fromisoformat(due).replace(tzinfo=tz.gettz("Europe/Paris")).isoformat()
    
    #DELEGATION - Available values : True, False.
        if isinstance(delegation, bool):
            if delegation: labels.append('delegated_🚀')
        else:
            delegation = False


    @classmethod
    def fromTodoistWebhook(cls, webhook_result, user_name:str):
        
        todoist_task_id = webhook_result['event_data']['id']
        priority = webhook_result['event_data']['priority']
        content = webhook_result['event_data']['content']
        labels = webhook_result['event_data']['labels']
        todoist_project_id = webhook_result['event_data']['project_id']
        todoist_url = webhook_result['event_data']['url']
        todoist_parent_id = webhook_result['event_data']['parent_id']

        if  webhook_result['event_data']['due'] is not None:
                due = webhook_result['event_data']['due']['date']
        else:
            due = None
        
        if DELEGATED_LABEL in labels : 
            delegation = True
        else:
            delegation = False
        
        if ONGOING_LABEL in labels or WAITING_LABEL in labels :
            if ONGOING_LABEL in labels: status = "On-Going"
            else : status = "Waiting"
        elif webhook_result['event_data']['checked'] == True :
            status = "Completed"
        else:
            status = "Not started"

        
        return cls(content=content, user_name=user_name, due=due, priority=priority, todoist_project_id=todoist_project_id, todoist_task_id=todoist_task_id, status=status, delegation=delegation, url=todoist_url, todoist_parent_id=todoist_parent_id)

    def __str__(self) -> str:
        #return str(dict(self))
        return json.dumps(
            {
            "event_name" : self.event_name,
            "todoist_task_ID" : self.todoist_task_id,
            "notion_ID" : self.notion_task_id, 
            "todoist_projectID" : self.todoist_project_id,
            "priority" : self.priority,
            "content" : self.content,
            "status" : self.status,
            "due" : self.due,
            "delegation": self.delegation,
            "user": self.user_name,
            "todoist_url" : self.url,
            "notion_parent_id": self.notion_parent_id,
            "todoist_parent_id":self.todoist_parent_id
            }
        )

    def __eq__(self, other_task) -> bool:
        if isinstance(other_task,Task):
            return (self.todoist_task_id, self.todoist_project_id, self.priority, self.content,self.status, self.due, self.delegation, self.user_name, self.todoist_parent_id)==(other_task.todoist_task_id, other_task.todoist_project_id, other_task.priority, other_task.content,other_task.status, other_task.due, other_task.delegation, other_task.user_name, other_task.todoist_parent_id)
        else: return False


    def get_notion_priority(todoist_priority: TodoistPriority | int) -> NotionPriority:
    #Get the corresponding Notion priority from a Todoist priority.
        if isinstance(todoist_priority, int):
            todoist_priority = TodoistPriority(todoist_priority)
        return NotionPriority[todoist_priority.name]


    def get_todoist_priority(notion_priority: NotionPriority | str) -> TodoistPriority:
        #Get the corresponding Todoist priority from a Notion priority.
        if isinstance(notion_priority, str):
            notion_priority = NotionPriority(notion_priority)
        return TodoistPriority[notion_priority.name]

    def get_notion_status(todoist_status: TodoistStatus | str) -> NotionStatus:
    #Get the corresponding Notion status from a Todoist status.
        if isinstance(todoist_status, str):
            todoist_status = TodoistStatus(todoist_status)
        return NotionStatus[todoist_status.name]
        
    def get_todoist_status(notion_status: NotionStatus | str) -> TodoistStatus:
    #Get the corresponding Todoist status from a Notion status.
        if isinstance(notion_status, str):
            notion_status = NotionStatus(notion_status)
        return TodoistStatus[notion_status.name]
        
    @classmethod
    def fromJson(cls, data):

        if 'event_name' in data : event_name = data['event_name'] 
        else: event_name=None
        
        todoist_task_id = data['todoist_task_ID']
        notion_task_id = data['notion_ID']
        todoist_project_id = data['todoist_projectID']
        priority = data['priority']
        content = data['content']
        status = data['status']
        due = data['due']
        delegation = data['delegation']
        todoist_url = data['todoist_url']
        todoist_parent_id = data['todoist_parent_id']
        notion_parent_id = data['notion_parent_id']
        user = data["user"]
                
        return cls(content=content, user_name=user,due=due, priority=priority, todoist_project_id=todoist_project_id, todoist_task_id=todoist_task_id, notion_task_id=notion_task_id, status=status, delegation=delegation, event_name=event_name, url=todoist_url, notion_parent_id=notion_parent_id, todoist_parent_id=todoist_parent_id)
        

    @classmethod
    def fromNotionJSON(cls, NotionJSON, user_name:str):
        
    #Required : NotionJSON is result of x.json() and only one object.
        if NotionJSON is not None and NotionJSON['object']!= "error":
            notion_task_id = NotionJSON['id']
            content = NotionJSON['properties']['Action']['title'][0]['text']['content']
            delegation = NotionJSON['properties']['Delegated']['checkbox']
            todoist_url = NotionJSON['properties']['URL']['url']

            if NotionJSON['properties']['Priority']['select'] is not None:
                priority = NotionJSON['properties']['Priority']['select']['name']                
                priority = Task.get_todoist_priority(priority).value
            else:
                priority = TodoistPriority.LOW.value

            if (NotionJSON['properties']['Due date']['date'] is not None):
                    due = NotionJSON['properties']['Due date']['date']['start']
            else:
                due = None

            if len(NotionJSON['properties']['TodoistID']['rich_text']) != 0:
                todoist_task_id = str(NotionJSON['properties']['TodoistID']['rich_text'][0]['text']['content'])
            else:
                todoist_task_id = None
            
            if len(NotionJSON['properties']['Todoist_ProjectID']['rich_text']) != 0:
                    todoist_project_id = str(NotionJSON['properties']['Todoist_ProjectID']['rich_text'][0]['text']['content'])
            else:
                todoist_project_id = None

            if NotionJSON['properties']['Status']['select'] is not None:
                Status_Notion = NotionJSON['properties']['Status']['select']['name']
                status = Task.get_todoist_status(Status_Notion).value
            else:
                status = TodoistStatus.NOT_STARTED.value

            if len(NotionJSON['properties']['Parent']['relation']) == 1:
                notion_parent_ID = NotionJSON['properties']['Parent']['relation'][0]['id']
            else: notion_parent_ID = None
            
            return cls(content=content, user_name=user_name, due=due, priority=priority, todoist_project_id=todoist_project_id, todoist_task_id=todoist_task_id, notion_task_id=notion_task_id, status=status, delegation=delegation, url=todoist_url, notion_parent_id=notion_parent_ID)
        else:
            return None
