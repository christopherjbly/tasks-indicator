#!/usr/bin/python
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
from gi.repository import Pango
import os

import locale
import urllib
import gettext
import comun
from task_dialog import TaskDialog
from tasklist_dialog import TaskListDialog

locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(comun.APP, comun.LANGDIR)
gettext.textdomain(comun.APP)
_ = gettext.gettext


class ShowTasksListsDialog(Gtk.Dialog):
	def __init__(self,tasks):
		Gtk.Dialog.__init__(self)
		self.set_title(comun.APPNAME + ' | '+_('Show tasklists'))
		self.set_modal(True)
		self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT)	
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
		self.store = Gtk.ListStore(object)
		self.treeview = Gtk.TreeView(model=self.store)
		cellrenderer = Gtk.CellRendererText()
		treeviewcolumn = Gtk.TreeViewColumn('Text', cellrenderer)
		treeviewcolumn.set_cell_data_func(cellrenderer, self.func)
		self.treeview.append_column(treeviewcolumn)		
		scrolledwindow.add(self.treeview)
		#
		vbox2 = Gtk.VBox(spacing = 0)
		vbox2.set_border_width(5)
		hbox.pack_start(vbox2,False,False,0)
		#
		self.button1 = Gtk.Button()
		self.button1.set_size_request(40,40)
		self.button1.set_tooltip_text(_('Add'))	
		self.button1.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_ADD,Gtk.IconSize.BUTTON))
		self.button1.connect('clicked',self.on_button_add_clicked)
		vbox2.pack_start(self.button1,False,False,0)
		#
		self.button2 = Gtk.Button()
		self.button2.set_size_request(40,40)
		self.button2.set_tooltip_text(_('Remove'))	
		self.button2.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_REMOVE,Gtk.IconSize.BUTTON))
		self.button2.connect('clicked',self.on_button_remove_clicked)
		vbox2.pack_start(self.button2,False,False,0)
		#
		self.tasks = tasks
		self.read_tasklists()
		#
		self.show_all()	

	def func(self,column, cell_renderer, tree_model, iter, user_data):
		tasklist = tree_model[iter][0]
		if tasklist is not None:
			cell_renderer.set_property('text', tasklist['title'])
	
	def read_tasklists(self):
		for tasklist in self.tasks.get_tasklists():
			self.store.append([tasklist])
			
	def on_button_add_clicked(self,widget):
		tld = TaskListDialog()
		if tld.run() == Gtk.ResponseType.ACCEPT:
			tld.hide()
			newtasklist = self.tasks.create_tasklist(tld.get_title())
			self.store.append([newtasklist])
		tld.destroy()

	def on_button_remove_clicked(self,widget):
		selection = self.treeview.get_selection()
		if selection:
			previous_path = None
			model,iter = selection.get_selected()
			tasklist = model.get_value(iter,0)
			self.tasks.remove_tasklist(tasklist)
			model.remove(iter)

	def close_application(self,widget):
		self.hide()
		
if __name__ == "__main__":
	p = ShowTasksDialog()
	if p.run() == Gtk.ResponseType.ACCEPT:
		p.hide()
	p.destroy()
	exit(0)
		
