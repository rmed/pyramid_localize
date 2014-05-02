# -*- coding: utf-8 -*-

import unittest
import pytest
from mock import Mock


from pyramid import testing
from pyramid.request import Request
from pyramid.events import BeforeRender
from pyramid.events import NewRequest
from pyramid.i18n import Localizer

# for this tests, these will be imported internally by pyramid's config
# from pyramid_localize.subscribers.i18n import global_renderer
# from pyramid_localize.subscribers.i18n import add_localizer
# from pyramid_localize.subscribers.fake import global_renderer
# from pyramid_localize.subscribers.fake import add_localizer


@pytest.fixture
def request_i18n():
    '''i18n:Test new request'''
    config = testing.setUp()
    config.scan('pyramid_localize.subscribers.i18n')
    request = Request({})
    request.registry = config.registry
    return request


def test_i18n_new_request(request_i18n):
    """Test method are being added."""
    request_i18n.registry.notify(NewRequest(request_i18n))
    assert isinstance(request_i18n.localizer, Localizer)
    assert hasattr(request_i18n, '_')


def test_i18n_before_render(request_i18n):
    '''i18n:Test before render'''
    before_render_event = BeforeRender({'request': request_i18n}, {})
    request_i18n.registry.notify(before_render_event)
    assert 'localizer' in before_render_event
    assert '_' in before_render_event


def test_i18n_before_render_and_request(request_i18n):
    '''i18n:Test before render with new request'''
    request_i18n.registry.notify(NewRequest(request_i18n))
    before_render_event = BeforeRender({'request': request_i18n}, {})
    request_i18n.registry.notify(before_render_event)
    assert 'localizer' in before_render_event
    assert '_' in before_render_event


@pytest.fixture
def request_fake():
    '''i18n:Test new request'''
    config = testing.setUp()
    config.scan('pyramid_localize.subscribers.fake')
    request = Request({})
    request.registry = config.registry
    return request


def test_fake_new_request(request_fake):
    '''fakei18n:Test new request'''
    request_fake.registry.notify(NewRequest(request_fake))
    assert hasattr(request_fake, '_')


def test_fake_before_render(request_fake):
    '''fakei18n:Test before render'''
    request_fake.registry.notify(NewRequest(request_fake))
    before_render_event = BeforeRender({'request': request_fake}, {})
    request_fake.registry.notify(before_render_event)
    assert '_' in before_render_event


def test_fake_before_render_norequest(request_fake):
    '''fakei18n:Test before render'''
    before_render_event = BeforeRender({'request': request_fake}, {})
    request_fake.registry.notify(before_render_event)
    assert '_' in before_render_event
