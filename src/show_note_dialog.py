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

from gi.repository import Gtk,GdkPixbuf
import os

import locale
import gettext
import comun
import urllib

locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(comun.APP, comun.LANGDIR)
gettext.textdomain(comun.APP)
_ = gettext.gettext


class ShowNoteDialog(Gtk.Dialog):
	def __init__(self,user,id):
		title = comun.APPNAME + ' | '+_('Show Note')
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
		table1 = Gtk.Table(rows = 1, columns = 2, homogeneous = False)
		table1.set_border_width(5)
		table1.set_col_spacings(5)
		table1.set_row_spacings(5)
		vbox0.add(table1)
		#
		scrolledwindow1 = Gtk.ScrolledWindow()
		scrolledwindow1.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scrolledwindow1.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
		scrolledwindow1.set_size_request(450,450)
		table1.attach(scrolledwindow1,0,1,0,1, xoptions = Gtk.AttachOptions.FILL, yoptions = Gtk.AttachOptions.FILL)
		entry1 = Gtk.TextView()
		entry1.set_wrap_mode(Gtk.WrapMode.WORD)
		scrolledwindow1.add(entry1)
		entry1.set_editable(False)
		#
		scrolledwindow2 = Gtk.ScrolledWindow()
		scrolledwindow2.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scrolledwindow2.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
		scrolledwindow2.set_size_request(450,450)
		table1.attach(scrolledwindow2,1,2,0,1, xoptions = Gtk.AttachOptions.FILL, yoptions = Gtk.AttachOptions.FILL)
		entry2 = Gtk.Viewport()
		scrolledwindow2.add(entry2)
		#
		note = user.get_note(id)
		print note['text']
		buffer = Gtk.TextBuffer()
		buffer.set_text(note['text'])
		entry1.set_buffer(buffer)
		#
		if len(note['media'])>0:
			data = user.get_media(note['id'],note['media'][0]['id'])
			print data
			if data and data['status'] == 'ok':
				print '#################################################'
				print 'si'
				print '#################################################'
				f = urllib.urlopen(data['src'])
				data = f.read()
				pbl = GdkPixbuf.PixbufLoader()
				pbl.write(data)
				self.pbuf = pbl.get_pixbuf()
				pbl.close()
				self.image = Gtk.Image()
				w=int(450)
				h=int(450)
				self.pbuf=self.pbuf.scale_simple(w,h,GdkPixbuf.InterpType.BILINEAR)
				self.image.set_from_pixbuf(self.pbuf)
				entry2.add(self.image)
		#
		self.scale = 100
		self.connect('key-release-event',self.on_key_release_event)
		#
		self.show_all()	

	def close_application(self,widget):
		self.ok = False

	def on_key_release_event(self,widget,event):
		print event.keyval
		if event.keyval == 65451 or event.keyval == 43:
			self.scale=self.scale*1.1
		elif event.keyval == 65453 or event.keyval == 45:
			self.scale=self.scale*.9
		elif event.keyval == 65456 or event.keyval == 48:
			self.scale = 100
		if self.pbuf != None:
			w=int(self.pbuf.get_width()*self.scale/100)
			h=int(self.pbuf.get_height()*self.scale/100)
			pixbuf=self.pbuf.scale_simple(w,h,GdkPixbuf.InterpType.BILINEAR)
			self.image.set_from_pixbuf(pixbuf)		
		
		
if __name__ == "__main__":
	p = ShowNoteDialog()
	if p.run() == Gtk.ResponseType.ACCEPT:
		p.hide()
	p.destroy()
	exit(0)
		
