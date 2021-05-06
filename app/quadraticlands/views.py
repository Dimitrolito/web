# -*- coding: utf-8 -*-
"""Define the quadraticlands views.

Copyright (C) 2020 Gitcoin Core

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

"""

import json
import logging
import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.templatetags.static import static
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from quadraticlands.helpers import (
    get_FAQ, get_initial_dist, get_initial_dist_breakdown, get_mission_status, get_stewards,
)
from ratelimit.decorators import ratelimit

logger = logging.getLogger(__name__)


def index(request):
    '''render template for base index page'''
    context, game_status = get_initial_dist(request), get_mission_status(request)
    context.update(game_status)
    return TemplateResponse(request, 'quadraticlands/index.html', context)


def base(request, base):
    '''render templates for /quadraticlands/'''
    context, game_status = get_initial_dist(request), get_mission_status(request)
    context.update(game_status)
    if base == 'faq':
        context.update(get_FAQ(request))
    return TemplateResponse(request, f'quadraticlands/{base}.html', context)


@login_required
def base_auth(request, base):
    '''render templates for /quadraticlands/'''
    context, game_status = get_initial_dist(request), get_mission_status(request)
    context.update(game_status)
    if base == 'stewards':
        context.update(get_stewards())
    return TemplateResponse(request, f'quadraticlands/{base}.html', context)


def mission_index(request):
    '''render quadraticlands/mission/index.html'''
    context, game_status = get_initial_dist(request), get_mission_status(request)
    context.update(game_status)
    return TemplateResponse(request, 'quadraticlands/mission/index.html', context)


@login_required
def mission_base(request, mission_name):
    '''used to handle quadraticlands/<mission_name>'''
    context, game_status = get_initial_dist(request), get_mission_status(request)
    context.update(game_status)
    return TemplateResponse(request, f'quadraticlands/mission/{mission_name}/index.html', context)


@login_required
def dashboard_index(request):
    '''render quadraticlands/dashboard/index.html'''
    context, game_status = get_initial_dist(request), get_mission_status(request)
    context.update(game_status)
    return TemplateResponse(request, 'quadraticlands/dashboard/index.html', context)


@login_required
def mission_state(request, mission_name, mission_state):
    '''quadraticlands/<mission_name>/<mission_state>'''
    context, game_status = get_initial_dist(request), get_mission_status(request)
    context.update(game_status)
    if mission_state == 'delegate':
        context.update(get_stewards())
    if mission_state == 'claim':
        context.update(get_initial_dist_breakdown(request))
    return TemplateResponse(request, f'quadraticlands/mission/{mission_name}/{mission_state}.html', context)


@login_required
def mission_question(request, mission_name, question_num):
    '''Used to handle quadraticlands/<mission_name>/<mission_state>/<question_num>'''
    context, game_status = get_initial_dist(request), get_mission_status(request)
    context.update(game_status)
    return TemplateResponse(request, f'quadraticlands/mission/{mission_name}/question_{question_num}.html', context)


@login_required
def mission_answer(request, mission_name, question_num, answer):
    '''Used to handle quadraticlands/<mission_name>/<mission_state>/<question_num>/<answer>'''
    context, game_status = get_initial_dist(request), get_mission_status(request)
    context.update(game_status)
    return TemplateResponse(request, f'quadraticlands/mission/{mission_name}/question_{question_num}_{answer}.html', context)


def workstream_index(request):
    '''Use to render quadraticlands/workstream/index.html'''
    return TemplateResponse(request, 'quadraticlands/workstream/index.html')


def workstream_base(request, stream_name):
    '''Used to render quadraticlands/workstream/<stream_name>.html'''
    return TemplateResponse(request, f'quadraticlands/workstream/{stream_name}.html')


@login_required
def mission_postcard(request):
    '''Used to handle quadraticlands/<mission_name>/<mission_state>/<question_num>'''
    attrs = {
        'front_frame': ['1', '2', '3', '4'],
        'front_background': ['a', 'b', 'c', 'd'],
        'back_background': ['a', 'b', 'c', 'd'],
    }
    context = {
        'attrs': attrs,
    }
    return TemplateResponse(request, f'quadraticlands/mission/postcard/postcard.html', context)


@ratelimit(key='ip', rate='1/s', method=ratelimit.UNSAFE, block=True)
def mission_postcard_svg(request):
    import xml.etree.ElementTree as ET
    from django.http import HttpResponse

    width = 100
    height = 100
    viewBox = ''
    tags = ['{http://www.w3.org/2000/svg}style']
    ET.register_namespace('', "http://www.w3.org/2000/svg")
    prepend = f'''<?xml version="1.0" encoding="utf-8"?>
<svg width="{width}%" height="{height}%" viewBox="{viewBox}" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
'''
    postpend = '''
</svg>
'''

    package = request.GET.dict()
    file = 'assets/v2/images/quadraticlands/postcard.svg'
    with open(file) as file:
        elements = []
        tree = ET.parse(file)
        for item in tree.getroot():
            output = ET.tostring(item).decode('utf-8')

            _id = item.attrib.get('id')
            include_item = None
            if _id == 'text':

                # get text
                replace_text = package.get('text')

                # chop up the text by word length to create line breaks.
                line_words_length = 7
                include_item = True
                end_wrap = '</tspan>'
                words = replace_text.split(' ')
                new_words = []
                line_offset = 0
                line_counter_for_newline_insert = 0
                for i in range(0, len(words)):
                    line_counter_for_newline_insert += 1
                    if words[i] == 'NEWLINE':
                        line_counter_for_newline_insert = 0
                    insert_newline = line_counter_for_newline_insert % line_words_length == 0
                    if words[i] == 'NEWLINE':
                        insert_newline = True
                    if insert_newline:
                        line_offset += 1

                    y = 26 + (line_offset) * 26
                    start_wrap = f'<tspan x="0" y="{y}">'

                    if i == 0:
                        new_words.append(start_wrap)
                    if insert_newline:
                        new_words.append(end_wrap)
                        new_words.append(start_wrap)
                    if words[i] != 'NEWLINE':
                        new_words.append(words[i])
                    if i == (len(words) - 1):
                        new_words.append(end_wrap)

                # actually insert the text
                replace_text = " ".join(new_words)
                output = output.replace('POSTCARD_TEXT_GOES_HERE', replace_text)
            if _id:
                val = _id.split(":")[-1]
                key = _id.split(":")[0]
                if val == package.get(key):
                    include_item = True
            if include_item:
                elements.append(output)
        output = prepend + "".join(elements) + postpend

        response = HttpResponse(output, content_type='image/svg+xml')
        return response


def handler403(request, exception=None):
    return error(request, 403)


def handler404(request, exception=None):
    return error(request, 404)


def handler500(request, exception=None):
    return error(request, 500)


def handler400(request, exception=None):
    return error(request, 400)


def error(request, code):
    context = {
        'code': code,
        'title': "Error {}".format(code)
    }
    return_as_json = 'api' in request.path

    if return_as_json:
        return JsonResponse(context, status=code)
    return TemplateResponse(request, f'quadraticlands/error.html', context, status=code)