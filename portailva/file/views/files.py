import magic
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.views.generic import DetailView

from django.utils.translation import ugettext as _
from portailva.file.models import File, FileVersion


class FileView(DetailView):
    template_name = None
    model = File
    object = None

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.can_access(request.user):
            raise PermissionDenied
        return super(FileView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        file_uuid = self.kwargs.get('uuid')
        if file_uuid is not None:
            queryset = queryset.filter(uuid=file_uuid)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def get(self, request, *args, **kwargs):
        # We get file last version
        try:
            version = FileVersion.objects\
                .filter(file_id=self.object.id)\
                .latest('created_at')

            mime = magic.Magic(mime=True, magic_file=settings.MAGIC_BIN)
            mime_type = mime.from_file(version.data.path)

            response = HttpResponse(version.data.read(), content_type=mime_type)
            return response
        except FileVersion.DoesNotExist:
            raise Http404
