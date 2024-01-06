import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from routes.mapper import SubMapper
from flask import Blueprint


rss_blueprint = Blueprint('rss_blueprint', __name__)
@rss_blueprint.route('/feeds/recent.rss', endpoint='recent')
def recent():

    context =  {
        'model': model,
        'session': model.Session,
        'user': c.user
    }

    data_dict = {
        'q' : '+metadata_visibility:Public',
        'fq': '+edc_state:("PUBLISHED" OR "PENDING ARCHIVE")',
        'start': 0,
        'rows': 50,
        'sort': 'record_publish_date desc, metadata_modified desc',
    }

    query = get_action('package_search')(context, data_dict)
    count = query['count']
    results = query['results']

    for result in results:
        if 'record_publish_date' in result:
            timestamp = time.mktime(datetime.datetime.strptime(result['record_publish_date'], "%Y-%m-%d").timetuple())
            result['record_publish_date'] = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%a, %d %b %Y %H:%M:%S PST')


    base_url = config.get('ckan.site_url')

    vars = { 'results': results, 'count': count, 'base_url': base_url }

    response.content_type = 'xml'

    return render('recent.html', extra_vars=vars)

class EDCRSSPlugin(plugins.SingletonPlugin):

    plugins.implements(plugins.IConfigurer)
    # plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IBlueprint)

    def update_config(self, config):

        toolkit.add_template_directory(config, 'templates')

    # def before_map(self, map):

    #     rss_controller = 'ckanext.edc_rss.controllers.rss:RSSController'

    #     with SubMapper(map, controller=rss_controller) as m:
    #         m.connect('/feeds/recent.rss', action='recent')

    #     return map

    def get_blueprint(self):

        return rss_blueprint

