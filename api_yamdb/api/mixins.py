from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.permission import IsAdminOrReadOnly


class CreateListDestroyViewSet(
mixins.CreateModelMixin, mixins.ListModelMixin,
mixins.DestroyModelMixin, viewsets.GenericViewSet,
):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]