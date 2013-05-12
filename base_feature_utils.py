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

#from mainweb.models import *
# lettuce feature testing template

""" Phrases:
Given I access the "something" page - returns html content to world.dom, world.response, world.full_url
I should be redirected to page "pagename" - makes sure a redirect to a page was done
I should have a textfield "fieldname" and put value "value-of-text"
I should submit the data

"""

@before.all
def setstuff():
    world.data = {}
    world.browser = Client()


@step(u'I should reset the data')
def i_should_reset_the_data(step):
    world.data = {}
    assert True, "ok"


@step(u'Given I access the "(.*)" page')
def given_i_access_the_group1_page(step, group1):
    """ access a page by pagename expect 200"""
    pageurl = reverse(group1)
    world.full_url = django_url(pageurl)
    world.response = world.browser.get(pageurl, follow=True)
    world.dom = html.fromstring(world.response.content)
    assert_true(world.response.status_code == 200)


@step(u'I should have a textfield "(.*)" and put value "(.*)"')
def i_should_have_a_textfield_group1_and_put_value_group2(step, group1, group2):
    world.data[group1] = group2

    formfield = None
    for form in world.dom.forms:
        for html_input in form.inputs:
            if html_input.name == group1:
                formfield = html_input

    assert_true(formfield.type == "password" or formfield.type == "text")
    assert_equals(group1, formfield.name)


@step(u'I should have a textfield "(.*)" with value "(.*)"')
def i_should_have_a_textfield_group1_with_value_group2(step, group1, group2):
    world.data[group1] = group2

    formfield = None
    for form in world.dom.forms:
        for html_input in form.inputs:
            if html_input.name == group1:
                formfield = html_input

    assert_true(formfield.type == "password" or formfield.type == "text")
    assert_equals(group1, formfield.name)
    assert_equals(group2, formfield.value)

@step(u'I should have a hiddenfield "(.*)" with value "(.*)"')
def i_should_have_a_hiddenfield_group1_with_value_group2(step, group1, group2):
    world.data[group1] = group2

    formfield = None
    for form in world.dom.forms:
        for html_input in form.inputs:
            if html_input.name == group1:
                formfield = html_input

    assert_true(formfield.type == "hidden")
    assert_equals(group1, formfield.name)
    assert_equals(group2, formfield.value)


 
@step(u'I should be redirected to page "(.*)"')
def i_should_be_redirected_to_page_group1(step, group1):
    """ check pageurl matches the redirect url set from submit data """
    pageurl = reverse(group1)
    u = django_url(pageurl)
    assert_true(str(group1) in str(world.full_redirect_url))


# submit a post form
@step(u'I should submit the data')
def i_should_submit_the_data(step):
    """ uses world.full_url that is set in access-page function 
    this funciton is used assuming its trying to post to the last page that was accessed"""
    world.post_response = world.browser.post(world.full_url, world.data, follow=True)
    assert_true(world.post_response.status_code, 200)
    foundpage = False
    for url, status_code in world.post_response.redirect_chain:
        if status_code == 302:
            foundpage = url
            world.full_redirect_url = url



