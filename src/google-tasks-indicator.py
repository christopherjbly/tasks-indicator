#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
#
__author__='lorenzo.carbonell.cerezo@gmail.com'
__date__ ='$21/02/2012'
#
# Google-Tasks-Indicator
# An indicator for Google Tasks
#
# Copyright (C) 2012 Lorenzo Carbonell
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
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gtk
from gi.repository import GdkPixbuf
from gi.repository import Notify

import time
import dbus
import locale
import gettext
import datetime
import webbrowser
#
import comun
import googletasksapi
from configurator import Configuration
from preferences_dialog import Preferences
from task_dialog import TaskDialog
from show_tasks_dialog import ShowTasksDialog
#

locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(comun.APP, comun.LANGDIR)
gettext.textdomain(comun.APP)
_ = gettext.gettext

def internet_on():
	try:
		response=urllib2.urlopen('http://google.com',timeout=1)
		return True
	except:
		pass
	return False

class MenuNote(Gtk.CheckMenuItem):
	def __init__(self,note):
		Gtk.CheckMenuItem.__init__(self)
		self.note = note
		self.get_children()[0].set_use_markup(True)
		self.get_children()[0].set_markup('<s>%s</s>'%note['title'])
		self.set_active(note['status'] == 'completed')

def add2menu(menu, text = None, icon = None, conector_event = None, conector_action = None, note = None):
	if note != None:
		menu_item = MenuNote(note)
	else:
		if text != None:
			if icon == None:
				menu_item = Gtk.MenuItem.new_with_label(text)
			else:
				menu_item = Gtk.ImageMenuItem.new_with_label(text)
				image = Gtk.Image.new_from_stock(icon, Gtk.IconSize.MENU)
				menu_item.set_image(image)
				menu_item.set_always_show_image(True)
		else:
			if icon == None:
				menu_item = Gtk.SeparatorMenuItem()
			else:
				menu_item = Gtk.ImageMenuItem.new_from_stock(icon, None)
				menu_item.set_always_show_image(True)
	if conector_event != None and conector_action != None:				
		menu_item.connect(conector_event,conector_action)
	menu_item.show()
	menu.append(menu_item)
	return menu_item

class GoogleTasksIndicator():
	def __init__(self):
		if dbus.SessionBus().request_name("es.atareao.google-tasks-indicator") != dbus.bus.REQUEST_NAME_REPLY_PRIMARY_OWNER:
			print "application already running"
			exit(0)
		self.indicator = appindicator.Indicator.new('Google-Tasks-Indicator', 'Google-Tasks-Indicator', appindicator.IndicatorCategory.APPLICATION_STATUS)
		self.read_preferences()
		#
		self.gta = googletasksapi.GTAService()
		self.events = []
		self.set_menu()
		
	def read_preferences(self):
		error = True
		while error:
			try:
				configuration = Configuration()
				self.tasklist_id = configuration.get('tasklist_id')
				self.theme = configuration.get('theme')
				error = False
			except Exception,e:
				print e
				error = True
				p = Preferences()
				if p.run() == Gtk.ResponseType.ACCEPT:
					p.save_preferences()
				else:
					exit(1)
				p.destroy()

	def set_menu(self,check=False):
		#
		normal_icon = os.path.join(comun.ICONDIR,'google-tasks-indicator-%s-normal.svg'%(self.theme))
		starred_icon = os.path.join(comun.ICONDIR,'google-tasks-indicator-%s-starred.svg'%(self.theme))
		#
		self.indicator.set_icon(normal_icon)
		self.indicator.set_attention_icon(starred_icon)		
		#
		menu = Gtk.Menu()
		#
		self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
		#self.indicator.set_status(appindicator.IndicatorStatus.ATTENTION)
		add2menu(menu, text = _('Add new Note'), conector_event = 'activate',conector_action = self.menu_add_new_task)			
		add2menu(menu)
		add2menu(menu, text = _('Refresh'), conector_event = 'activate',conector_action = self.menu_refresh)			
		add2menu(menu, text = _('Clear completed tasks'), conector_event = 'activate',conector_action = self.menu_clear_completed_tasks)			
		add2menu(menu, text = _('Show Notes'), conector_event = 'activate',conector_action = self.menu_show_tasks)
		add2menu(menu)
		add2menu(menu, text = _('Preferences'), conector_event = 'activate',conector_action = self.menu_preferences_response)
		add2menu(menu)
		menu_help = add2menu(menu, text =_('Help'))
		menu_help.set_submenu(self.get_help_menu())
		add2menu(menu)
		add2menu(menu, text = _('Exit'), conector_event = 'activate',conector_action = self.menu_exit_response)
		add2menu(menu)
		for note in self.gta.get_tasks(tasklist_id = self.tasklist_id)[0:10]:
			add2menu(menu, text = note['title'], conector_event = 'activate',conector_action = self.menu_check_item, note = note)
		menu.show()
		self.indicator.set_menu(menu)
		while Gtk.events_pending():
			Gtk.main_iteration()
		

	def get_help_menu(self):
		help_menu =Gtk.Menu()
		#		
		add2menu(help_menu,text = _('Web...'),conector_event = 'activate',conector_action = lambda x: webbrowser.open('https://launchpad.net/google-tasks-indicator'))
		add2menu(help_menu,text = _('Get help online...'),conector_event = 'activate',conector_action = lambda x: webbrowser.open('https://answers.launchpad.net/google-tasks-indicator'))
		add2menu(help_menu,text = _('Translate this application...'),conector_event = 'activate',conector_action = lambda x: webbrowser.open('https://translations.launchpad.net/google-tasks-indicator'))
		add2menu(help_menu,text = _('Report a bug...'),conector_event = 'activate',conector_action = lambda x: webbrowser.open('https://bugs.launchpad.net/google-tasks-indicator'))
		add2menu(help_menu)
		self.menu_about = add2menu(help_menu,text = _('About'),conector_event = 'activate',conector_action = self.menu_about_response)
		#
		help_menu.show()
		#
		return help_menu

	def menu_preferences_response(self,widget):
		widget.set_sensitive(False)
		p = Preferences()
		if p.run() == Gtk.ResponseType.ACCEPT:
			p.save_preferences()
		p.destroy()
		self.read_preferences()
		widget.set_sensitive(True)
	
	def menu_edit_note(self,widget):
		widget.set_sensitive(False)
		annd = NoteDialog(note = widget.note)
		if annd.run() == Gtk.ResponseType.ACCEPT:
			title = annd.get_title()
			notes = annd.get_notes()
			completed = annd.is_completed()
			due = annd.get_due_date()
			self.gta.edit_task(task_id = widget.note['id'], tasklist_id = self.tasklist_id, title = title, notes = notes, iscompleted = completed, due = due)			
			#
			self.set_menu()
		annd.destroy()
		widget.set_active(widget.note['status'] == 'completed')
		widget.set_sensitive(True)	
			
	def menu_check_item(self,widget):
		completed = not widget.get_active()
		widget.note = self.gta.edit_task(task_id = widget.note['id'], tasklist_id = self.tasklist_id, iscompleted = not completed)			
		widget.set_active(widget.note['status'] == 'completed')
				
	def menu_add_new_task(self,widget):
		widget.set_sensitive(False)
		annd = TaskDialog()
		if annd.run() == Gtk.ResponseType.ACCEPT:
			title = annd.get_title()
			notes = annd.get_notes()
			completed = annd.is_completed()
			due = annd.get_due_date()
			#
			self.gta.create_task(tasklist_id = self.tasklist_id, title = title, notes = notes, time = due, iscompleted = completed)
			self.set_menu()
		annd.destroy()
		widget.set_sensitive(True)
		
	def menu_clear_completed_tasks(self,widget):
		widget.set_sensitive(False)
		self.gta.clear_completed_tasks(tasklist_id = self.tasklist_id)
		self.set_menu()
		widget.set_sensitive(True)
		
	def menu_refresh(self,widget):
		widget.set_sensitive(False)
		self.set_menu()
		widget.set_sensitive(True)
		
	def menu_show_tasks(self,widget):
		widget.set_sensitive(False)
		snd = ShowTasksDialog(self.gta, self.tasklist_id)
		snd.run()
		snd.destroy()
		self.set_menu()
		widget.set_sensitive(True)

	def menu_exit_response(self,widget):
		exit(0)

	def menu_about_response(self,widget):
		widget.set_sensitive(False)
		ad=Gtk.AboutDialog()
		ad.set_name(comun.APPNAME)
		ad.set_version(comun.VERSION)
		ad.set_copyright('Copyrignt (c) 2012\nLorenzo Carbonell')
		ad.set_comments(_('An indicator for Google Tasks'))
		ad.set_license(''+
		'This program is free software: you can redistribute it and/or modify it\n'+
		'under the terms of the GNU General Public License as published by the\n'+
		'Free Software Foundation, either version 3 of the License, or (at your option)\n'+
		'any later version.\n\n'+
		'This program is distributed in the hope that it will be useful, but\n'+
		'WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY\n'+
		'or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for\n'+
		'more details.\n\n'+
		'You should have received a copy of the GNU General Public License along with\n'+
		'this program.  If not, see <http://www.gnu.org/licenses/>.')
		ad.set_website('http://www.atareao.es')
		ad.set_website_label('http://www.atareao.es')
		ad.set_authors(['Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'])
		ad.set_documenters(['Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'])
		ad.set_logo(GdkPixbuf.Pixbuf.new_from_file(comun.ICON))
		ad.set_program_name(comun.APPNAME)
		ad.run()
		ad.destroy()
		widget.set_sensitive(True)

if __name__ == "__main__":
	Notify.init("google-tasks-indicator")
	gti=GoogleTasksIndicator()
	Gtk.main()

