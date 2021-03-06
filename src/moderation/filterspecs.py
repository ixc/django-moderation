from django.db import models
from django.contrib.admin.filterspecs import FilterSpec, RelatedFilterSpec
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _

import moderation


class ContentTypeFilterSpec(RelatedFilterSpec):
    def __init__(self, f, request, params, model, model_admin):
        super(ContentTypeFilterSpec, self).__init__(f, request, params,
                                                    model, model_admin)
        self.content_types = self._get_content_types()
        self.lookup_choices = [(ct.id, ct.name.capitalize()) \
                               for ct in self.content_types]

    def _get_content_types(self):
        content_types = []
        for model in moderation.moderation._registered_models.keys():
            content_types.append(ContentType.objects.get_for_model(model))

        return content_types

FilterSpec.filter_specs.insert(0, (lambda f: getattr(f, 'content_type_filter',
                                                     False),
                                    ContentTypeFilterSpec))
