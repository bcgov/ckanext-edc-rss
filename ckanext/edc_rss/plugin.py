import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.edc_rss.controllers.rss import rss_blueprint


class EDCRSSPlugin(plugins.SingletonPlugin):

    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)

    def update_config(self, config):

        toolkit.add_template_directory(config, 'templates')


    def get_blueprint(self):

        return rss_blueprint

