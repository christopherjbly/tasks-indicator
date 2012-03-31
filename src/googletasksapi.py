#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
#
#
# googletasksapi.py
#
# Copyright (C) 2011 Lorenzo Carbonell
# lorenzo.carbonell.cerezo@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#

'''
Dependencies:
python-gflags


'''

import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

import datetime
import comun 
FLAGS = gflags.FLAGS

# Set up a Flow object to be used if we need to authenticate. This
# sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
# the information it needs to authenticate. Note that it is called
# the Web Server Flow, but it can also handle the flow for native
# applications
# The client_id and client_secret are copied from the API Access tab on
# the Google APIs Console

FLOW = OAuth2WebServerFlow(
    client_id='197445608333.apps.googleusercontent.com',
    client_secret='DwhP0pHLYhjtVEJ5nIMryp-n',
    scope='https://www.googleapis.com/auth/tasks',
    user_agent='Google-Tasks-Indicator/0.0.1.0')

class GTAService():
	def __init__(self):
		# To disable the local server feature, uncomment the following line:
		# FLAGS.auth_local_webserver = False

		# If the Credentials don't exist or are invalid, run through the native client
		# flow. The Storage object will ensure that if successful the good
		# Credentials will get written back to a file.
		storage = Storage(comun.COOKIE_FILE)
		credentials = storage.get()
		if credentials is None or credentials.invalid == True:
		  credentials = run(FLOW, storage)

		# Create an httplib2.Http object to handle our HTTP requests and authorize it
		# with our good Credentials.
		http = httplib2.Http()
		http = credentials.authorize(http)

		# Build a service object for interacting with the API. Visit
		# the Google APIs Console
		# to get a developerKey for your own application.
		self.service = build(serviceName='tasks', version='v1', http=http,developerKey='AIzaSyDrzTfquQVzNGV9aOA93jMmWC4wB9bd530')

	def get_tasklists(self):
		tasklists = self.service.tasklists().list().execute()
		return tasklists['items']

	def get_tasklist(self,tasklist_id):
		tasklist = self.service.tasklists().get(tasklist=tasklist_id).execute()
		return tasklist
		
	def create_tasklist(self,title):
		tasklist = {
			'title': title
		}
		result = self.service.tasklists().insert(body=tasklist).execute()
		return result

	def update_tasklist(self, tasklist_id, new_title):
		tasklist = self.service.tasklists().get(tasklist=tasklist_id).execute()
		tasklist['title'] = new_title
		result = self.service.tasklists().update(tasklist=tasklist['id'], body=tasklist).execute()
		return result

	def delete_tasklist(self,tasklist_id):
		result = self.service.tasklists().delete(tasklist=tasklist_id).execute()
		return result
		
	def clear_completed_tasks(self,tasklist_id = '@default'):
		return self.service.tasks().clear(tasklist = tasklist_id).execute()


	
	def get_tasks(self, tasklist_id = '@default'):
		tasks = self.service.tasks().list(tasklist=tasklist_id).execute()
		if tasks and 'items' in tasks.keys():
			tasks = tasks['items']
		else:
			tasks = []
		return tasks
	
	def get_task(self, task_id, tasklist_id = '@default'):
		task = self.service.tasks().get(tasklist = tasklist_id, task = task_id).execute()
		return task

	def create_task(self, tasklist_id = '@default', title = '', notes = '', time = None, iscompleted = False):
		if iscompleted:
			status = 'completed'
		else:
			status = 'needsAction'
		if time:
			time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z')
			task = {
			  'title': title,
			  'notes': notes,
			  'status' : status,
			  'due': time
			  }
		else:
			task = {
			  'title': title,
			  'notes': notes,
			  'status' : status
			  }
		result = self.service.tasks().insert(tasklist='@default', body=task).execute()
		return result

	def move_task(self, task_id, previous_task_id,tasklist_id = '@default'):
		result = self.service.tasks().move(tasklist=tasklist_id, task=task_id,  previous=previous_task_id).execute()
		return result 
		
	def move_task_first(self,task_id, tasklist_id = '@default'):
		result = self.service.tasks().move(tasklist=tasklist_id, task=task_id).execute()
		return result 


	def edit_task(self, task_id, tasklist_id = '@default', title = None, notes = None, iscompleted = None, due = None):
		task = self.service.tasks().get(tasklist = tasklist_id, task = task_id).execute()
		if not title:
			if 'title' in task.keys():
				title = task['title']
		if not notes:
			if 'notes' in task.keys():
				notes = task['notes']
		if iscompleted!= None:
			if iscompleted == True:
				status = 'completed'
			else:
				status = 'needsAction'
		elif 'status' in task.keys():
			status = task['status']
		else:
			status = 'needsAction'
		if due:
			time = due.strftime('%Y-%m-%dT%H:%M:%S.000Z')
			task = {
				'id' : task_id,
				'title': title,
				'notes': notes,
				'status' : status,
				'due': time
			  }
		else:
			task = {
				'id' : task_id,
				'title': title,
				'notes': notes,
				'status' : status
			}	
		result = self.service.tasks().update(tasklist=tasklist_id, task=task_id, body=task).execute()
		return result
	
	def delete_task(self,task_id, tasklist_id = '@default'):
		return self.service.tasks().delete(tasklist=tasklist_id, task=task_id).execute()
		

if __name__ == '__main__':	
	gta = GTAService()
	'''
	for tasklist in gta.get_tasklists():
		print tasklist
	'''
	#print gta.create_tasklist('desde ubuntu')
	#print gta.get_tasklist('MDU4MDg5OTIxODI5ODgyMTE0MTg6MDow')
	print gta.get_tasks()
	for task in gta.get_tasks():
		print '%s -> %s'%(task['title'],task['id'])
	#print gta.create_task(title = 'prueba2 desde ubuntu',notes = 'primera prueba')
	gta.move_task_first('MDU4MDg5OTIxODI5ODgyMTE0MTg6MDoy')
