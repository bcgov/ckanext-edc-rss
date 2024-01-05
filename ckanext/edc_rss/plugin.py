import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from routes.mapper import SubMapper
from rss import rss_blueprint

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

