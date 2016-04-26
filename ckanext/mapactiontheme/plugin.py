import pylons.config as config
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

def hide_follows():
    '''Hides the follows section that would allow users to follow datasets

    To enable hiding the most popular groups, add this line to the
    [app:main] section of your CKAN config file::

      ckan.mapactiontheme.hide_follows = True

    Returns ``False`` by default, if the setting is not in the config file.

    :rtype: boolean
    '''
    value = config.get('ckan.mapactiontheme.hide_follows', False)
    value = toolkit.asbool(value)
    return value

def unauthorized(context, data_dict=None):
    return {'success': False, 'msg': 'Organizations are not available.'}

class MapactionthemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IAuthFunctions)

    
    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'mapactiontheme')

    def get_auth_functions(self):
        return {
            'group_create': unauthorized,
            'organization_show': unauthorized,
            'organization_list': unauthorized,
            'organization_create': unauthorized,
            'organization_member_create': unauthorized,
            'organization_update': unauthorized,
            'organization_delete': unauthorized        
        }

    def get_helpers(self):
        return {'hide_follows': hide_follows
                }