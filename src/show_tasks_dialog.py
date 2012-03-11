#! /usr/bin/python
# -*- coding: iso-8859-15 -*-
#
__author__='atareao'
__date__ ='$19/02/2012$'
#
#
# Copyright (C) 2011,2012 Lorenzo Carbonell
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

from gi.repository import Gtk, Gdk, GdkPixbuf
import os

import locale
import urllib
import gettext
import comun
from task_dialog import TaskDialog

locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(comun.APP, comun.LANGDIR)
gettext.textdomain(comun.APP)
_ = gettext.gettext


class ShowTasksDialog(Gtk.Dialog):
	def __init__(self,gta,tasklist_id):
		title = comun.APPNAME + ' | '+_('Show Tasks')
		Gtk.Dialog.__init__(self,title,None,Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,(Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))
		self.set_size_request(450, 300)
		self.set_resizable(False)
		self.set_icon_from_file(comun.ICON)
		self.connect('destroy', self.close_application)
		#
		vbox0 = Gtk.VBox(spacing = 5)
		vbox0.set_border_width(5)
		self.get_content_area().add(vbox0)
		#
		hbox = Gtk.HBox()
		vbox0.pack_start(hbox,True,True,0)
		#
		scrolledwindow = Gtk.ScrolledWindow()
		scrolledwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scrolledwindow.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
		scrolledwindow.set_size_request(450,300)
		hbox.pack_start(scrolledwindow,True,True,0)
		#
		# id, text, image
		self.store = Gtk.ListStore(str,str)
		self.treeview = Gtk.TreeView(model=self.store)	
		self.treeview.append_column(Gtk.TreeViewColumn('Text', Gtk.CellRendererText(), markup=1))		
		scrolledwindow.add(self.treeview)
		self.treeview.connect('button-press-event',self.on_treeview_button_press_event)
		#
		vbox2 = Gtk.VBox(spacing = 0)
		vbox2.set_border_width(5)
		hbox.pack_start(vbox2,False,False,0)
		#
		self.button1 = Gtk.Button()
		self.button1.set_size_request(40,40)
		self.button1.set_tooltip_text(_('Up'))	
		self.button1.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_GO_UP,Gtk.IconSize.BUTTON))
		self.button1.connect('clicked',self.on_button_up_clicked)
		vbox2.pack_start(self.button1,False,False,0)
		#
		self.button2 = Gtk.Button()
		self.button2.set_size_request(40,40)
		self.button2.set_tooltip_text(_('Down'))	
		self.button2.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_GO_DOWN,Gtk.IconSize.BUTTON))
		self.button2.connect('clicked',self.on_button_down_clicked)
		vbox2.pack_start(self.button2,False,False,0)
		#
		self.button3 = Gtk.Button()
		self.button3.set_size_request(40,40)
		self.button3.set_tooltip_text(_('Mark as completed'))		
		self.button3.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_APPLY,Gtk.IconSize.BUTTON))
		self.button3.connect('clicked',self.on_button_completed_clicked)
		vbox2.pack_start(self.button3,False,False,0)
		#
		self.button4 = Gtk.Button()
		self.button4.set_size_request(40,40)
		self.button4.set_tooltip_text(_('Edit'))		
		self.button4.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_EDIT,Gtk.IconSize.BUTTON))
		self.button4.connect('clicked',self.on_button_edit_clicked)
		vbox2.pack_start(self.button4,False,False,0)
		#
		self.button5 = Gtk.Button()
		self.button5.set_size_request(40,40)
		self.button5.set_tooltip_text(_('Clear completed tasks'))		
		self.button5.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_CLEAR,Gtk.IconSize.BUTTON))
		self.button5.connect('clicked',self.on_button_clear_clicked)
		vbox2.pack_start(self.button5,False,False,0)
		#
		self.gta = gta
		self.tasklist_id = tasklist_id
		self.offset = 0
		self.read_notes()
		#
		self.show_all()	
	
	def on_treeview_button_press_event(self,widget,event):
		#
		# if event.button==1 and event.type==Gdk.BUTTON_PRESS:
		#
		# Gdk.EventType.2BUTTON_PRESS is not working in python because
		# it starts with number so use Gdk.EventType(value = 5) to construct
		# 2BUTTON_PRESS event type
		if event.button == 1 and event.type == Gdk.EventType(value=5):		
				model,iter = self.treeview.get_selection().get_selected()
				id = model.get_value(iter,0)
				snd = ShowNoteDialog(self.user,id)
				snd.run()
				snd.destroy()
				print id
		
	def read_notes(self):
		for note in self.gta.get_tasks(tasklist_id = self.tasklist_id):
			if note['status'] == 'completed':
				text = '<span foreground="red"><s>%s</s></span>'%note['title']
			else:
				text = '<span foreground="blue">%s</span>'%note['title']
			self.store.append([note['id'],text])
			
	def on_button_up_clicked(self,widget):
		selection = self.treeview.get_selection()
		if selection:
			previous_path = None
			model,iter = selection.get_selected()
			treepath = model.get_path(iter)
			path = int(str(treepath))
			id = model.get_value(iter,0)
			if path > 1:
				previous_path = Gtk.TreePath.new_from_string(str(path - 2))
				previous_iter = model.get_iter(previous_path)
				previous_id = model.get_value(previous_iter,0)
				note = self.gta.move_task(id, previous_id,tasklist_id = self.tasklist_id)
				previous_path = Gtk.TreePath.new_from_string(str(path - 1))
			elif path == 1:
				previous_path = Gtk.TreePath.new_from_string('0')
				note = self.gta.move_task_first(id,tasklist_id = self.tasklist_id)
			if previous_path:
				self.store.clear()
				self.read_notes()
				selection.select_path(previous_path)					
					

	def on_button_down_clicked(self,widget):
		selection = self.treeview.get_selection()
		if selection:
			previous_path = None
			model,iter = selection.get_selected()
			treepath = model.get_path(iter)
			path = int(str(treepath))
			id = model.get_value(iter,0)
			iter_next = model.iter_next(iter)
			if iter_next:
				path_next = model.get_path(iter_next)
				next_id = model.get_value(iter_next,0)
				note = self.gta.move_task(id, next_id,tasklist_id = self.tasklist_id)
				if note:
					self.store.clear()
					self.read_notes()
					selection.select_path(path_next)
					
	def on_button_completed_clicked(self,widget):
		selection = self.treeview.get_selection()
		if selection:
			model,iter = selection.get_selected()
			path = model.get_path(iter)
			id = model.get_value(iter,0)
			note = self.gta.get_task(id, tasklist_id = self.tasklist_id)
			if note['status'] == 'completed':
				self.gta.edit_task(id,tasklist_id = self.tasklist_id,iscompleted = False)
			else:
				self.gta.edit_task(id,tasklist_id = self.tasklist_id,iscompleted = True)
			self.store.clear()
			self.read_notes()
			selection.select_path(path)

	def on_button_clear_clicked(self,widget):
		self.gta.clear_completed_tasks(tasklist_id = self.tasklist_id)
		selection = self.treeview.get_selection()
		if selection:
			model,iter = selection.get_selected()
			path = model.get_path(iter)
		self.store.clear()
		self.read_notes()
		if selection:
			if path:
				selection.select_path(path)

	def on_button_edit_clicked(self,widget):
		selection = self.treeview.get_selection()
		if selection:
			model,iter = selection.get_selected()
			path = model.get_path(iter)
			id = model.get_value(iter,0)
			task = self.gta.get_task(id, tasklist_id = self.tasklist_id)
			p = TaskDialog(task = task)
			if p.run() == Gtk.ResponseType.ACCEPT:
				title = p.get_title()
				notes = p.get_notes()
				completed = p.is_completed()
				due = p.get_due_date()
				print title
				print notes
				print completed
				print due
				note = self.gta.edit_task(id, tasklist_id = self.tasklist_id, title = title, notes = notes, iscompleted = completed, due = due)
				if note:
					self.store.clear()
					self.read_notes()
					selection.select_path(path)
			p.destroy()

	def close_application(self,widget):
		self.hide()
		
if __name__ == "__main__":
	p = ShowNotesDialog()
	if p.run() == Gtk.ResponseType.ACCEPT:
		p.hide()
	p.destroy()
	exit(0)
		
