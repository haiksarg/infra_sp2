from rest_framework import filters, mixins, viewsets

from api.permissions import IsAdminUserOrReadOnly
from .validators import validate_username


class UsernameMixin:
    def validate_username(self, username):
        return validate_username(username)


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CategoryGenreMixin(ListCreateDestroyViewSet):
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter, )
    lookup_field = 'slug'
    search_fields = ('name', )
