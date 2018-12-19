# Copyright 2015 - Alcatel-Lucent
#
# Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from django.views import generic
import logging
from openstack_dashboard.api.rest import urls
from openstack_dashboard.api.rest import utils as rest_utils
from vitrage_dashboard.api import vitrage

LOG = logging.getLogger(__name__)


@urls.register
class Topolgy(generic.View):
    """API for vitrage topology."""

    url_regex = r'vitrage/topology/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a single volume's details with the volume id.

        The following get parameters may be passed in the GET

        :param volume_id the id of the volume

        The result is a volume object.
        """

        ''' original default is graph '''

        LOG.info("--------- reques --------------- %s", str(request))

        graph_type = 'tree'
        all_tenants = 'false'
        root = None
        limit = None

        if 'graph_type' in request.GET:
            graph_type = request.GET.get('graph_type')
        if 'all_tenants' in request.GET:
                        all_tenants = request.GET.get('all_tenants')
        if 'root' in request.GET:
                        root = request.GET.get('root')
        if 'depth' in request.GET:
                        limit = int(request.GET.get('depth'))

        query = None
        if 'query' in request.GET:
            query = request.GET.get('query')
            LOG.info("--A request QUERY -- %s", str(query))
        elif graph_type == 'tree':
            ''' Default tree query - get computes, used by Sunburst'''
            query = '{"and": [{"==": {"vitrage_category": "RESOURCE"}},' \
                    '{"==": {"vitrage_is_deleted": false}},' \
                    '{"==": {"vitrage_is_placeholder": false}},' \
                    '{"or": [{"==": {"vitrage_type": "openstack.cluster"}},' \
                    '{"==": {"vitrage_type": "nova.instance"}},' \
                    '{"==": {"vitrage_type": "nova.host"}},' \
                    '{"==": {"vitrage_type": "nova.scheduler"}},' \
                    '{"==": {"vitrage_type": "nova.zone"}}]}]}'

        return vitrage.topology(request=request,
                                query=query,
                                graph_type=graph_type,
                                all_tenants=all_tenants,
                                root=root,
                                limit=limit)


@urls.register
class Alarms(generic.View):
    """API for vitrage alarms."""

    url_regex = r'vitrage/alarm/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a single entity's alarm with the vitrage id.

        The following get alarm may be passed in the GET

        :param vitrage_id the id of the vitrage entity

        The result is a alarms object.
        """
        vitrage_id = request.GET.get('vitrage_id', 'all')
        all_tenants = request.GET.get('all_tenants', False)
        limit = request.GET.get('limit', 1000)
        sort_by = request.GET.get('sort_by', ['start_timestamp', 'vitrage_id'])
        sort_dirs = request.GET.get('sort_dirs', ['asc', 'asc'])
        filter_by = request.GET.get('filter_by', None)
        filter_vals = request.GET.get('filter_vals', None)
        next_page = request.GET.get('next_page', True)
        marker = request.GET.get('marker', None)

        return vitrage.alarms(request, vitrage_id, all_tenants,
                              limit,
                              sort_by,
                              sort_dirs,
                              filter_by,
                              filter_vals,
                              next_page,
                              marker
                              )


@urls.register
class History(generic.View):
    """API for vitrage alarms history."""

    url_regex = r'vitrage/history/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of alarms history based on the input parameters.

        The following get alarm may be passed in the GET

        The result is a alarms object.
        """
        all_tenants = request.GET.get('all_tenants', False)
        start = request.GET.get('start', None)
        end = request.GET.get('end', None)
        limit = request.GET.get('limit', 1000)
        sort_by = request.GET.get('sort_by', ['start_timestamp', 'vitrage_id'])
        sort_dirs = request.GET.get('sort_dirs', ['asc', 'asc'])
        filter_by = request.GET.get('filter_by', None)
        filter_vals = request.GET.get('filter_vals', None)
        next_page = request.GET.get('next_page', True)
        marker = request.GET.get('marker', None)

        return vitrage.history(request, all_tenants,
                               start, end,
                               limit,
                               sort_by,
                               sort_dirs,
                               filter_by,
                               filter_vals,
                               next_page,
                               marker
                               )


@urls.register
class Rca(generic.View):
    """API for vitrage rca."""

    url_regex = r'vitrage/rca/(?P<alarm_id>.+|default)/' \
                '(?P<all_tenants>.+|default)/$'

    @rest_utils.ajax()
    def get(self, request, alarm_id, all_tenants):
        """Get rca graph for an alarm.

        :param alarm_id the id of the alarm

        The result is an rca graph.
        """

        return vitrage.rca(request, alarm_id, all_tenants)


@urls.register
class Templates(generic.View):
    """API for vitrage templates."""

    url_regex = r'vitrage/template/(?P<template_id>.+|default)/$'

    @rest_utils.ajax()
    def get(self, request, template_id):
        """Get a single template with the vitrage id.

        The following get template may be passed in the GET

        :param template_id the id of the vitrage template

        The result is a template object.
        """
        return vitrage.template_show(request, template_id)

    @rest_utils.ajax()
    def delete(self, request, template_id):
        """Delete a single template with the vitrage id.

        :param template_id the id of the vitrage template
        """
        return vitrage.template_delete(request, template_id)

    @rest_utils.ajax()
    def post(self, request, **kwargs):
        """Add a single template.

        request.body holds template in format:
        {template: template_string
         type: template_type}

        """

<<<<<<< HEAD
        return vitrage.template_add(request)
=======
        return vitrage.templates(request, template_id)


@urls.register
class Actions(generic.View):
    """API for actions."""

    url_regex = r'vitrage/actions/(?P<action>.+|default)/' \
                '(?P<nodetype>.+|default)/$'

    @rest_utils.ajax()
    def get(self, request, action, nodetype):
        return vitrage.actions(request, action, nodetype)


@urls.register
class Requests(generic.View):
    """API for action requests."""

    url_regex = r'vitrage/requests/(?P<action>.+|default)/' \
                '(?P<requestdict>.+|default)$'

    @rest_utils.ajax()
    def post(self, request, action, requestdict):
        return vitrage.action_request(request, action, requestdict)


@urls.register
class Settings(generic.View):
    """API for action settings."""

    url_regex = r'vitrage/settings$'

    @rest_utils.ajax()
    def get(self, request):
        return vitrage.action_setting(request)
>>>>>>> 69eb3d91ebc1c869257348d83e86e65cfae036f1