import ckan.lib.base as base
import ckan.model as model
import ckan.logic as logic
import ckan.lib.render as lib_render
import datetime
import time
from flask import Blueprint
import logging
import json


# from ckan.common import _, c, response, config
from ckan.common import _, c, config
#TODO: Remove above line and find alternative source for response

import pprint

get_action = logic.get_action
render = base.render
log = logging.getLogger('ckanext.edc_rss')


class RSSController(base.BaseController):

    def recent(self):

        context =  {
            'model': model,
            'session': model.Session,
            'user': c.user
        }

        data_dict = {
            'q' : '+metadata_visibility:Public',
            'fq': '+publish_state:("PUBLISHED" OR "PENDING ARCHIVE")',
            'start': 0,
            'rows': 50,
            'sort': 'record_publish_date desc, metadata_modified desc',
        }

        query = get_action('package_search')(context, data_dict)
        count = query['count']
        results = query['results']
        log.info('Results: ' + json.dumps(results))
        for result in results:
            if 'record_publish_date' in result:
                timestamp = time.mktime(datetime.datetime.strptime(result['record_publish_date'], "%Y-%m-%d").timetuple())
                result['record_publish_date'] = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%a, %d %b %Y %H:%M:%S PST')


        base_url = config.get('ckan.site_url')

        vars = { 'results': results, 'count': count, 'base_url': base_url }

        response.content_type = 'xml'

        return render('recent.html', extra_vars=vars)

