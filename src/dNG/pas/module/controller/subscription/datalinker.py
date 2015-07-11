# -*- coding: utf-8 -*-
##j## BOF

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;http;subscription

The following license agreement remains valid unless any additions or
changes are being made by direct Netware Group in a written form.

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc.,
59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;gpl
----------------------------------------------------------------------------
#echo(pasHttpSubscriptionVersion)#
#echo(__FILEPATH__)#
"""

import re

from dNG.pas.controller.predefined_http_request import PredefinedHttpRequest
from dNG.pas.data.data_linker import DataLinker
from dNG.pas.data.ownable_mixin import OwnableMixin as OwnableInstance
from dNG.pas.data.subscribable_mixin import SubscribableMixin as SubscribableInstance
from dNG.pas.data.http.translatable_error import TranslatableError
from dNG.pas.data.text.input_filter import InputFilter
from dNG.pas.data.text.l10n import L10n
from dNG.pas.data.xhtml.link import Link
from dNG.pas.data.xhtml.notification_store import NotificationStore
from dNG.pas.database.nothing_matched_exception import NothingMatchedException
from .module import Module

class Datalinker(Module):
#
	"""
Service for "m=subscription;s=datalinker"

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: datalinker
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	def execute_subscribe(self):
	#
		"""
Action for "subscribe"

:since: v0.1.00
		"""

		_id = InputFilter.filter_file_path(self.request.get_dsd("oid", ""))

		source_iline = InputFilter.filter_control_chars(self.request.get_dsd("source", "")).strip()

		L10n.init("pas_http_datalinker")
		L10n.init("pas_http_subscription")

		if (self.response.is_supported("html_css_files")): self.response.add_theme_css_file("mini_default_sprite.min.css")

		if (len(source_iline) > 0):
		#
			Link.set_store("servicemenu",
			               Link.TYPE_RELATIVE_URL,
			               L10n.get("core_back"),
			               { "__query__": re.sub("\\_\\_\\w+\\_\\_", "", source_iline) },
			               icon = "mini-default-back",
			               priority = 7
			              )
		#

		session = self.request.get_session()
		subscription_handler = self._get_subscription_handler(_id)

		if (subscription_handler is None): NotificationStore.get_instance().add_error(L10n.get("errors_pas_http_subscription_not_subscribable"))
		elif (not subscription_handler.is_subscribable_for_session_user(session)): NotificationStore.get_instance().add_error(L10n.get("errors_pas_http_subscription_not_subscribable"))
		else:
		#
			subscription_handler.set_session(session)
			if (not subscription_handler.is_subscribed()): subscription_handler.subscribe()

			NotificationStore.get_instance().add_completed_info(L10n.get("pas_http_subscription_done_subscribe"))
		#

		source_iline = re.sub("\\_\\_\\w+\\_\\_", "", source_iline)

		Link.clear_store("servicemenu")

		redirect_request = PredefinedHttpRequest()
		redirect_request.set_iline(source_iline)
		self.request.redirect(redirect_request)
	#

	def execute_unsubscribe(self):
	#
		"""
Action for "unsubscribe"

:since: v0.1.00
		"""

		_id = InputFilter.filter_file_path(self.request.get_dsd("oid", ""))

		source_iline = InputFilter.filter_control_chars(self.request.get_dsd("source", "")).strip()

		L10n.init("pas_http_datalinker")
		L10n.init("pas_http_subscription")

		if (self.response.is_supported("html_css_files")): self.response.add_theme_css_file("mini_default_sprite.min.css")

		if (len(source_iline) > 0):
		#
			Link.set_store("servicemenu",
			               Link.TYPE_RELATIVE_URL,
			               L10n.get("core_back"),
			               { "__query__": re.sub("\\_\\_\\w+\\_\\_", "", source_iline) },
			               icon = "mini-default-back",
			               priority = 7
			              )
		#

		session = self.request.get_session()
		subscription_handler = self._get_subscription_handler(_id)

		if (subscription_handler is None): NotificationStore.get_instance().add_error(L10n.get("errors_pas_http_subscription_not_subscribable"))
		elif (not subscription_handler.is_subscribable_for_session_user(session)): NotificationStore.get_instance().add_error(L10n.get("errors_pas_http_subscription_not_subscribable"))
		else:
		#
			subscription_handler.set_session(session)
			if (subscription_handler.is_subscribed()): subscription_handler.unsubscribe()

			NotificationStore.get_instance().add_completed_info(L10n.get("pas_http_subscription_done_unsubscribe"))
		#

		source_iline = re.sub("\\_\\_\\w+\\_\\_", "", source_iline)

		Link.clear_store("servicemenu")

		redirect_request = PredefinedHttpRequest()
		redirect_request.set_iline(source_iline)
		self.request.redirect(redirect_request)
	#

	def _get_subscription_handler(self, _id):
	#
		"""
Action for "subscribe"

:since: v0.1.00
		"""

		datalinker_object = None

		try: datalinker_object = DataLinker.load_id(_id)
		except NothingMatchedException: pass

		session = self.request.get_session()

		if (datalinker_object is None): raise TranslatableError("pas_http_datalinker_oid_invalid", 404)
		elif (isinstance(datalinker_object, OwnableInstance)
		      and (not datalinker_object.is_readable_for_session_user(session))
		     ): raise TranslatableError("core_access_denied", 403)

		return (datalinker_object.get_subscription_handler()
		        if (isinstance(datalinker_object, SubscribableInstance)) else
		        None
		       )
	#
#

##j## EOF