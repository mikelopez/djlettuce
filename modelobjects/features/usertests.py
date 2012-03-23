from django.core.urlresolvers import reverse
from lettuce import step, before, world
from lxml import html
from django.test.client import Client
from nose.tools import assert_equals, assert_true

from lettuce.django import django_url
import httplib
import urllib, urllib2
import json
import os
from xml.dom import minidom

import httplib
from settings import TEST_UPLOAD_HOST, TEST_UPLOAD_SELECTOR, TEST_UPLOAD_FILENAME, PROJECT_ROOTDIR
from web.models import *
from lib.http_post_upload import *

from django.contrib.auth.models import *

@before.all
def setbrowser():
  world.browser = Client()

@step(u'I should have group "(.*)"')
def i_should_have_group_group1(step, groupname):
  try:
    group = Group.objects.get(name=groupname)
  except Group.DoesNotExist:
    group = Group.objects.create(name=groupname)
    group.save()
  assert_true(group)


@step(u'I should have user "(.*)" with password "(.*)" and group "(.*)"')
def i_should_have_user_group1_with_password_group2_and_group_group3(step, username, password, groupname):
  try:
    u = User.objects.get(username=username)
  except User.DoesNotExist:
    u = User.objects.create(username=username)
    u.set_password(password)
    u.save()

  try:
    up=UserProfile.objects.get(user=u)
  except UserProfile.DoesNotExist:
    up = UserProfile(user=u)
    up.save()

  
  try:
    g = Group.objects.get(name=groupname)
  except Group.DoesNotExist:
    g = Group.objects.create(name=groupname)
    g.save()

  u.groups.add(g)
  u.save()
	assert True
