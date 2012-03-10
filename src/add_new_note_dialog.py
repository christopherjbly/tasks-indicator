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

from gi.repository import Gtk
import os

import locale
import gettext
import comun

locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(comun.APP, comun.LANGDIR)
gettext.textdomain(comun.APP)
_ = gettext.gettext


class AddNewNoteDialog(Gtk.Dialog):
	def __init__(self):
		title = comun.APPNAME + ' | '+_('Add New Note')
		Gtk.Dialog.__init__(self,title,None,Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,(Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT,Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL))
		self.set_size_request(250, 160)
		self.set_resizable(False)
		self.set_icon_from_file(comun.ICON)
		self.connect('destroy', self.close_application)
		#
		vbox0 = Gtk.VBox(spacing = 5)
		vbox0.set_border_width(5)
		self.get_content_area().add(vbox0)
		#
		table1 = Gtk.Table(rows = 4, columns = 2, homogeneous = False)
		table1.set_border_width(5)
		table1.set_col_spacings(5)
		table1.set_row_spacings(5)
		vbox0.add(table1)
		#
		label11 = Gtk.Label(_('Title')+':')
		label11.set_alignment(0,.5)
		table1.attach(label11,0,1,0,1, xoptions = Gtk.AttachOptions.FILL, yoptions = Gtk.AttachOptions.FILL)
		#
		label12 = Gtk.Label(_('Notes')+':')
		label12.set_alignment(0,0)
		table1.attach(label12,0,1,1,2, xoptions = Gtk.AttachOptions.FILL, yoptions = Gtk.AttachOptions.FILL)
		#
		label13 = Gtk.Label(_('Completed')+':')
		label13.set_alignment(0,.5)
		table1.attach(label13,0,1,2,3, xoptions = Gtk.AttachOptions.FILL, yoptions = Gtk.AttachOptions.SHRINK)
		#
		label14 = Gtk.Label(_('Date due')+':')
		label14.set_alignment(0,0)
		table1.attach(label14,0,1,3,4, xoptions = Gtk.AttachOptions.FILL, yoptions = Gtk.AttachOptions.SHRINK)
		#
		self.entry1 = Gtk.Entry()
		self.entry1.set_width_chars(60)
		table1.attach(self.entry1,1,2,0,1, xoptions = Gtk.AttachOptions.EXPAND, yoptions = Gtk.AttachOptions.SHRINK)
		#
		scrolledwindow2 = Gtk.ScrolledWindow()
		scrolledwindow2.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scrolledwindow2.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
		table1.attach(scrolledwindow2,1,2,1,2, xoptions = Gtk.AttachOptions.FILL, yoptions = Gtk.AttachOptions.FILL)
		self.entry2 = Gtk.TextView()
		self.entry2.set_wrap_mode(Gtk.WrapMode.WORD)
		scrolledwindow2.set_size_request(450,450)
		scrolledwindow2.add(self.entry2)
		#
		self.entry3 = Gtk.Switch()
		table1.attach(self.entry3,1,2,2,3, xoptions = Gtk.AttachOptions.SHRINK, yoptions = Gtk.AttachOptions.SHRINK)
		#
		self.entry4 = Gtk.Calendar()
		table1.attach(self.entry4,1,2,3,4, xoptions = Gtk.AttachOptions.SHRINK, yoptions = Gtk.AttachOptions.SHRINK)
		'''
		#
		self.entry2 = Gtk.Entry()
		self.entry2.set_width_chars(60)
		self.entry2.set_sensitive(False)
		table1.attach(self.entry2,1,2,2,3, xoptions = Gtk.AttachOptions.EXPAND, yoptions = Gtk.AttachOptions.SHRINK)
		#
		self.button1 = Gtk.Button('Load')
		self.button1.connect('clicked',self.on_button1_clicked)
		table1.attach(self.button1,2,3,2,3, xoptions = Gtk.AttachOptions.EXPAND, yoptions = Gtk.AttachOptions.SHRINK)
		'''
		self.show_all()
	def on_button1_clicked(self,widget):
			dialog = Gtk.FileChooserDialog(_('Select one image to add to the Note'),
											self,
										   Gtk.FileChooserAction.OPEN,
										   (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
											Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
			dialog.set_default_response(Gtk.ResponseType.OK)
			dialog.set_select_multiple(True)
			dialog.set_current_folder(os.getenv('HOME'))
			filter = Gtk.FileFilter()
			filter.set_name(_('Imagenes'))
			filter.add_mime_type('image/png')
			filter.add_mime_type('image/jpeg')
			filter.add_mime_type('image/gif')
			filter.add_mime_type('image/x-ms-bmp')
			filter.add_mime_type('image/x-icon')
			filter.add_mime_type('image/tiff')
			filter.add_mime_type('image/x-photoshop')
			filter.add_mime_type('x-portable-pixmap')
			filter.add_pattern('*.png')
			filter.add_pattern('*.jpg')
			filter.add_pattern('*.gif')
			filter.add_pattern('*.bmp')
			filter.add_pattern('*.ico')
			filter.add_pattern('*.tiff')
			filter.add_pattern('*.psd')
			filter.add_pattern('*.ppm')
			dialog.add_filter(filter)
			preview = Gtk.Image()
			dialog.set_preview_widget(preview)
			dialog.connect('update-preview', self.update_preview_cb, preview)
			response = dialog.run()
			if response == Gtk.ResponseType.OK:
				filename = dialog.get_filename()
				self.entry2.set_text(filename)
			dialog.destroy()
	def close_application(self,widget):
		self.ok = False
	
	def update_preview_cb(self,file_chooser, preview):
		filename = file_chooser.get_preview_filename()
		try:
			pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(filename, 128, 128)
			preview.set_from_pixbuf(pixbuf)
			have_preview = True
		except:
			have_preview = False
		file_chooser.set_preview_widget_active(have_preview)
		return
		
	def get_text(self):
		tbuffer =self.entry1.get_buffer()
		inicio = tbuffer.get_start_iter()
		fin = tbuffer.get_end_iter()
		return tbuffer.get_text(inicio,fin,True)

	def get_file(self):
		if len(self.entry2.get_text())>0:
			return self.entry2.get_text()
		return None
		
		
if __name__ == "__main__":
	p = AddNewNoteDialog()
	if p.run() == Gtk.ResponseType.ACCEPT:
		p.hide()
	p.destroy()
	exit(0)
		
