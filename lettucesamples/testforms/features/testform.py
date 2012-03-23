from django.core.urlresolvers import reverse
from lettuce import step, before, world
from lxml import html
from django.test.client import Client
from nose.tools import assert_equals, assert_true, assert_false

from lettuce.django import django_url
import httplib
import urllib, urllib2
import json
import os
from xml.dom import minidom
from django.contrib.auth.models import *
from web.models import *

import settings

# Marcos Lopez - dev@scidentify.info
# lettuce tests using browser get requests, login
# Parses dom html and checks for form elements supplied from features

@before.all
def set_browser():
  world.browser = Client()


@step(u'I should login with "(.*)" and "(.*)"')
def i_should_login_with_group1_and_group2(step, user, password_var):
  passwd = getattr(settings, password_var)
  assert_true(world.browser.login(username=user, password=passwd))

@step(u'Given I access the "(.*)" page')
def given_i_access_the_group1_page(step, pagename):
  pageurl = reverse(pagename)
  world.response = world.browser.get(pageurl, follow=True)
  world.dom = html.fromstring(world.response.content)

@step(u'I should have a form field "(.*)" of type "(.*)"')
def i_should_have_a_form_field_group1_of_type_group2(step, fieldname, type):
  form_field = None
  for form in world.dom.forms:
    for htmlinput in form.inputs:
      if htmlinput.name == fieldname:
        form_field = htmlinput

  assert_true(form_field.type == type)
  assert_equals(form_field.name, fieldname)

@step(u'Then I logout')
def then_i_logout(step):
  world.browser.logout()
  assert True, "YOURE AWESOME"

