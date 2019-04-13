import dateutil.parser
from datetime import datetime

import pycountry

import pylons.config as config

from ckan.lib.helpers import get_pkg_dict_extra

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.logic.schema import default_create_package_schema

from functools import partial


def group_name():
    '''Allows renaming of "Group"

    To change this setting add to the
    [app:main] section of your CKAN config file::

      ckan.mapactiontheme.group_name = MyGroupName

    Returns ``Group`` by default, if the setting is not in the config file.

    :rtype: boolean
    '''
    value = config.get('ckan.mapactiontheme.group_name', 'Group')
    return value


def plural_group_name():
    '''Allows renaming of "Groups", the plural form.

    To change this setting add to the
    [app:main] section of your CKAN config file::

      ckan.mapactiontheme.plural_group_name = MyGroupNames

    Returns ``Group`` by default, if the setting is not in the config file.

    :rtype: boolean
    '''
    value = config.get('ckan.mapactiontheme.plural_group_name', group_name() + 's')
    return value


def show_follows():
    '''Shows the follows section that would allow users to follow datasets

    To enable hiding this section add this line to the
    [app:main] section of your CKAN config file::

      ckan.mapactiontheme.show_follows = False

    Returns ``True`` by default, if the setting is not in the config file.

    :rtype: boolean
    '''
    value = config.get('ckan.mapactiontheme.show_follows', True)
    value = toolkit.asbool(value)
    return value


def show_license():
    '''Shows the license section

    To enable hiding this section add this line to the
    [app:main] section of your CKAN config file::

      ckan.mapactiontheme.show_license = False

    Returns ``True`` by default, if the setting is not in the config file.

    :rtype: boolean
    '''
    value = config.get('ckan.mapactiontheme.show_license', True)
    value = toolkit.asbool(value)
    return value


def show_organization():
    '''Show or hide the entire concept of organizations (this affects several templates)

    To hide organizations add this line to the
    [app:main] section of your CKAN config file::

      ckan.mapactiontheme.show_organization = False

    Returns ``True`` by default, if the setting is not in the config file.

    Templates this setting affects:
    * package/read_base.html
    * package/base.html


    :rtype: boolean
    '''
    value = config.get('ckan.mapactiontheme.show_organization', True)
    value = toolkit.asbool(value)
    return value


def show_social():
    '''Shows the social links section

    To hide this section add this line to the
    [app:main] section of your CKAN config file::

      ckan.mapactiontheme.show_social = False

    Returns ``True`` by default, if the setting is not in the config file.

    :rtype: boolean
    '''
    value = config.get('ckan.mapactiontheme.show_social', True)
    value = toolkit.asbool(value)
    return value


def show_groups_tab():
    '''Shows the groups tab in places like the package_read template.

    To hide this section add this line to the
    [app:main] section of your CKAN config file::

      ckan.mapactiontheme.show_groups_tab = False

    Returns ``True`` by default, if the setting is not in the config file.

    :rtype: boolean
    '''
    value = config.get('ckan.mapactiontheme.show_groups_tab', True)
    value = toolkit.asbool(value)
    return value


def show_activity_tab():
    '''Shows the Activity Stream tab in places like the package_read template.

    To hide this section add this line to the
    [app:main] section of your CKAN config file::

      ckan.mapactiontheme.show_activity_tab = False

    Returns ``True`` by default, if the setting is not in the config file.

    :rtype: boolean
    '''
    value = config.get('ckan.mapactiontheme.show_activity_tab', True)
    value = toolkit.asbool(value)
    return value


def ckan_home_page_name():
    '''Get the name of the CKAN home page

    To set add this under the
    [app:main] section of your CKAN config file::

      ckan.mapactiontheme.ckan_home_page_name = Maps and Data

    :rtype: string
    '''
    value = config.get('ckan.mapactiontheme.ckan_home_page_name', 'Home')
    return value


def home_page_link():
    '''Get the link for the home page if ckan is deployed as part of a site.

    To set add this under the
    [app:main] section of your CKAN config file::

      ckan.mapactiontheme.home_page_link = http://mapaction.org

    :rtype: string
    '''
    value = config.get('ckan.mapactiontheme.home_page_link')
    return value


def nav_menu_this_id():
    '''The navigation menu item ID of the CKAN site

    To set add this under the
    [app:main] section of your CKAN config file::

      ckan.mapactiontheme.nav_menu_this_id = 12

    :rtype: string
    '''
    value = config.get('ckan.mapactiontheme.nav_menu_this_id')
    return int(value)


def wp_json_api(endpoint_setting):
    import requests
    menu = None

    endpoint_url = config.get(endpoint_setting)

    if endpoint_url is None:
        raise Exception("Missing setting: %s" % endpoint_setting)

    # http://docs.python-requests.org/en/master/user/advanced/#advanced
    # It's a good practice to set connect timeouts to slightly larger
    # than a multiple of 3, which is the default TCP packet retransmission
    # window.
    connect_timeout = float(config.get(
        'ckan.mapactiontheme.api_connect_timeout', 3.05))
    read_timeout = float(config.get('ckan.mapactiontheme.api_read_timeout', 3))

    try:
        resp = requests.get(endpoint_url, timeout=(connect_timeout,
                                                   read_timeout))
    except Exception:
        return None

    try:
        menu = resp.json()
    except Exception:
        pass

    return menu


def unauthorized(context, data_dict=None):
    return {'success': False, 'msg': 'Organizations are not available.'}


def authorized(context, data_dict=None):
    return {'success': True}


def update_dataset_for_hdx_syndication(context, data_dict):
    default_schema = default_create_package_schema()
    dataset_dict = data_dict['dataset_dict']

    # Copy only the default schema fields and values
    syndicated_dataset = dict(
        (k, dataset_dict[k]) for k in default_schema.keys()
        if k in dataset_dict
    )

    # Set creation date in HDX format
    try:
        date = dateutil.parser.parse(dataset_dict['createdate'])
    except:
        dataset_date = '01/01/2003'  # Consistent with previous implementation
    else:
        dataset_date = date.strftime('%d/%m/%Y')

    syndicated_dataset['dataset_date'] = dataset_date

    # Set Methodology
    methodology = dataset_dict.get('methodology')
    if methodology is None:
        syndicated_dataset['methodology_other'] = 'Not specified'
    else:
        syndicated_dataset['methodology_other'] = methodology
    syndicated_dataset['methodology'] = 'Other'

    syndicated_dataset['dataset_source'] = dataset_dict.get('datasource')

    syndicated_dataset['groups'] = _get_group_ids(dataset_dict)

    syndicated_dataset['data_update_frequency'] = '0'  # Never

    syndicated_dataset.pop('type', None)
    syndicated_dataset.pop('tags', None)
    syndicated_dataset.pop('extras', None)

    return syndicated_dataset


def _get_group_ids(dataset_dict):
    group_ids = []

    countries = dataset_dict.get('countries')

    if countries is not None:
        for country_name in countries.split(','):
            cleaned_name = country_name.strip().title()
            country = None

            try:
                country = pycountry.countries.get(
                    name=cleaned_name)
            except KeyError:
                try:
                    country = pycountry.countries.get(
                        common_name=cleaned_name)
                except KeyError:
                    pass

            if country is not None:
                group_ids.append(
                    {'id': country.alpha3.lower()})

    if group_ids == []:
        group_ids.append({'id': 'world'})

    return group_ids


class MapactionthemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IFacets, inherit=True)

    # IActions
    def get_actions(self):
        return {
            'update_dataset_for_syndication':
            update_dataset_for_hdx_syndication,
        }

    # IFacets
    def dataset_facets(self, facets_dict, package_type):
        facets_dict.pop('organization', False)
        facets_dict.pop('tags', False)

        return facets_dict

    # IFacets
    def organization_facets(self, facets_dict, group_type, package_type):
        facets_dict.pop('organization', False)
        facets_dict.pop('tags', False)

        return facets_dict

    # IRoutes
    def before_map(self, map):
        map.connect(
            '/dataset/groups/{id}',
            controller='ckanext.mapactiontheme.controllers.package:MapactionPackageController',
            action='groups')

        return map

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'mapactiontheme')

    #IAuthFunctions
    def get_auth_functions(self):

        permissions = {}
        if not show_organization():
            permissions = {
                'group_create': unauthorized,
                'member_create': authorized,
                'authorized': unauthorized,
                'organization_list': unauthorized,
                'organization_create': unauthorized,
                'organization_member_create': unauthorized,
                'organization_update': unauthorized,
                'organization_delete': unauthorized
            }

        return permissions

    #ITemplateHelpers
    def get_helpers(self):
        return {
            'group_name': group_name,
            'plural_group_name': plural_group_name,
            'show_follows': show_follows,
            'show_social': show_social,
            'show_organization': show_organization,
            'show_license': show_license,
            'show_groups_tab': show_groups_tab,
            'show_activity_tab': show_activity_tab,
            'ckan_home_page_name': ckan_home_page_name,
            'home_page_link': home_page_link,
            'current_emergencies': partial(
                wp_json_api,
                endpoint_setting='ckan.mapactiontheme.current_emergencies_api'
            ),
            'nav_menu': partial(
                wp_json_api,
                endpoint_setting='ckan.mapactiontheme.nav_menu_api'
            ),
            'nav_menu_this_id': nav_menu_this_id,
            'footer_widget': partial(
                wp_json_api,
                endpoint_setting='ckan.mapactiontheme.footer_widget_api'
            ),
        }
