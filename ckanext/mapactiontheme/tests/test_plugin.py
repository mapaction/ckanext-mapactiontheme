import unittest

from ckan.common import _
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
