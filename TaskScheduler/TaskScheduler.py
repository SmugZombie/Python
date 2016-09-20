import win32com.client, os, time

def create_scheduled_task(name, path, arguments, description, author, daily_interval, hour):
	computer_name = "" #leave all blank for current computer, current user
	computer_username = ""
	computer_userdomain = ""
	computer_password = ""
	action_id = str(name)
	action_path = r""+str(path) #executable path
	action_arguments = r'' #arguments
	action_workdir = r"" + str(os.path.dirname( path ) + "\\") #working directory for action executable
	author = str(author) #so that end users know who you are
	description = str(description) #so that end users can identify the task
	task_id = str(name)
	task_hidden = False #set this to True to hide the task in the interface
	username = ""
	password = ""
	run_flags = "TASK_RUN_NO_FLAGS" #see dict below, use in combo with username/password
	#define constants
	TASK_TRIGGER_DAILY = 2
	TASK_CREATE = 2
	TASK_CREATE_OR_UPDATE = 6
	TASK_ACTION_EXEC = 0
	IID_ITask = "{148BD524-A2AB-11CE-B11F-00AA00530503}"
	RUNFLAGSENUM = {
	    "TASK_RUN_NO_FLAGS"              : 0,
	    "TASK_RUN_AS_SELF"               : 1,
	    "TASK_RUN_IGNORE_CONSTRAINTS"    : 2,
	    "TASK_RUN_USE_SESSION_ID"        : 4,
	    "TASK_RUN_USER_SID"              : 8 
	}
	#connect to the scheduler (Vista/Server 2008 and above only)
	scheduler = win32com.client.Dispatch("Schedule.Service")
	scheduler.Connect(computer_name or None, computer_username or None, computer_userdomain or None, computer_password or None)
	rootFolder = scheduler.GetFolder("\\")
	#(re)define the task
	taskDef = scheduler.NewTask(0)
	colTriggers = taskDef.Triggers
	trigger = colTriggers.Create(TASK_TRIGGER_DAILY)
	trigger.DaysInterval = daily_interval

	timezone_offset = get_timezone_offset()
	offset = (hour - timezone_offset)
	if len(str(offset)) < 2: offset = str("0") + str(offset)

	trigger.StartBoundary = "2000-01-01T" + str(offset) + ":00:00-00:00"
	trigger.Enabled = False
	colActions = taskDef.Actions
	action = colActions.Create(TASK_ACTION_EXEC)
	action.ID = action_id
	action.Path = action_path
	action.WorkingDirectory = action_workdir
	action.Arguments = action_arguments
	info = taskDef.RegistrationInfo
	info.Author = author
	info.Description = description
	settings = taskDef.Settings
	settings.Enabled = False
	settings.Hidden = task_hidden
	#register the task (create or update, just keep the task name the same)
	result = rootFolder.RegisterTaskDefinition(task_id, taskDef, TASK_CREATE_OR_UPDATE, "", "", RUNFLAGSENUM[run_flags] ) #username, password
	#run the task once
	task = rootFolder.GetTask(task_id)
	task.Enabled = True
	runningTask = task.Run("")
	task.Enabled = True
	return

def get_timezone_offset():
	offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone; 
	return offset / 60 / 60 * -1

create_scheduled_task("Test","C:\\Users\\roneg\\Dropbox\\Work\\TaskScheduler\\test.ahk","","Test Event","BreachRadar",10,14)
