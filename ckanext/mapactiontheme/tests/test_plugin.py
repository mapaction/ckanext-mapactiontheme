import unittest

from ckan.common import _
import ckan.tests.helpers as helpers
import ckan.plugins as plugins

from ckanext.mapactiontheme.plugin import MapactionthemePlugin


class DatasetFacetsTest(unittest.TestCase):
    def setUp(self):
        super(DatasetFacetsTest, self).setUp()
        self.default_facet_titles = {
            'organization': _('Organizations'),
            'groups': _('Groups'),
            'tags': _('Tags'),
            'res_format': _('Formats'),
            'license_id': _('Licenses'),
        }

    def test_removes_organization(self):
        plugin = MapactionthemePlugin()
        facets_dict = plugin.dataset_facets(self.default_facet_titles,
                                            'dataset')

        self.assertTrue('organization' not in facets_dict)

    def test_removes_tags(self):
        plugin = MapactionthemePlugin()
        facets_dict = plugin.dataset_facets(self.default_facet_titles,
                                            'dataset')

        self.assertTrue('tags' not in facets_dict)

    def test_facet_dict_is_left_empty(self):
        plugin = MapactionthemePlugin()
        facets_dict = plugin.dataset_facets({},
                                            'dataset')

        self.assertEquals(facets_dict, {})


class OrganizationFacetsTest(unittest.TestCase):
    def setUp(self):
        super(OrganizationFacetsTest, self).setUp()
        self.default_facet_titles = {'organization': _('Organizations'),
                                     'groups': _('Groups'),
                                     'tags': _('Tags'),
                                     'res_format': _('Formats'),
                                     'license_id': _('Licenses')}

    def test_removes_organization(self):
        plugin = MapactionthemePlugin()
        facets_dict = plugin.organization_facets(self.default_facet_titles,
                                                 'organization',
                                                 'dataset')

        self.assertTrue('organization' not in facets_dict)

    def test_removes_tags(self):
        plugin = MapactionthemePlugin()
        facets_dict = plugin.organization_facets(self.default_facet_titles,
                                                 'organization',
                                                 'dataset')

        self.assertTrue('tags' not in facets_dict)

    def test_facet_dict_is_left_empty(self):
        plugin = MapactionthemePlugin()
        facets_dict = plugin.organization_facets({},
                                                 'organization',
                                                 'dataset')

        self.assertEquals(facets_dict, {})


class UpdateForSyndicationTest(unittest.TestCase):
    def setUp(self):
        super(UpdateForSyndicationTest, self).setUp()
        plugins.load('mapactiontheme')

    def tearDown(self):
        plugins.unload('mapactiontheme')
        super(UpdateForSyndicationTest, self).tearDown()

    def test_dataset_date_is_created_date(self):
        dataset_dict = {
            'extras': [{
                'key': 'createdate',
                'value': '2016-06-15 03:49:19'},
            ]
        }

        updated_dict = helpers.call_action('update_dataset_for_syndication',
                                           dataset_dict=dataset_dict)

        self.assertEquals(updated_dict['dataset_date'],
                          '06/15/16')

    def test_dataset_source_is_datasource(self):

        datasource = 'Situational data: N/ABoundaries: GADMSettlements: GeofabrikPhysical features: GeofabrikWaterways: Geofabrik<ITA>add data sources here (concise list)</ITA>'

        dataset_dict = {
            'extras': [{
                'key': 'datasource',
                'value': datasource},
            ]
        }

        updated_dict = helpers.call_action('update_dataset_for_syndication',
                                           dataset_dict=dataset_dict)

        self.assertEquals(updated_dict['dataset_source'],
                          datasource)
