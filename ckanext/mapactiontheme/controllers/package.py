import ckan.controllers.package as package
import ckan.lib.dictization.model_dictize as model_dictize
import ckan.model as model

from ckan.common import c


class MapactionPackageController(package.PackageController):

    def groups(self, id):

        q = model.Session.query(model.Group) \
            .filter(model.Group.is_organization == False) \
            .filter(model.Group.state == 'active')

        groups = q.all()

        '''
        package = c.get('package')
        if package:
            groups = set(groups) - set(package.get_groups())
        '''

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj, 'use_cache': False}

        group_list = model_dictize.group_list_dictize(groups, context)

        c.event_dropdown = [[group['id'], group['display_name']]
                            for group in group_list]

        return super(MapactionPackageController, self).groups(id)