from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path

from arches_rdm.views import ConceptTreeView

urlpatterns = [
    path('', include('arches.urls')),
    path("concept_trees/", ConceptTreeView.as_view(), name="concept_trees"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.SHOW_LANGUAGE_SWITCH is True:
#     urlpatterns = i18n_patterns(*urlpatterns)
