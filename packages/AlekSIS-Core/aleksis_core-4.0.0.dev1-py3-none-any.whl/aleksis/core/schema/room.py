from graphene_django import DjangoObjectType
from graphene_django_cud.mutations import (
    DjangoBatchDeleteMutation,
    DjangoBatchPatchMutation,
    DjangoCreateMutation,
)

from ..models import Room
from .base import (
    DeleteMutation,
    DjangoFilterMixin,
    PermissionBatchDeleteMixin,
    PermissionBatchPatchMixin,
    PermissionsTypeMixin,
)


class RoomType(PermissionsTypeMixin, DjangoFilterMixin, DjangoObjectType):
    class Meta:
        model = Room
        fields = ("id", "name", "short_name")
        filter_fields = {
            "id": ["exact", "lte", "gte"],
            "name": ["icontains"],
            "short_name": ["icontains"],
        }

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset  # FIXME filter this queryset based on permissions


class RoomCreateMutation(DjangoCreateMutation):
    class Meta:
        model = Room
        permissions = ("core.create_room",)
        only_fields = ("id", "name", "short_name")


class RoomDeleteMutation(DeleteMutation):
    klass = Room
    permission_required = "core.delete_room"


class RoomBatchDeleteMutation(PermissionBatchDeleteMixin, DjangoBatchDeleteMutation):
    class Meta:
        model = Room
        permissions = ("core.delete_room",)


class RoomBatchPatchMutation(PermissionBatchPatchMixin, DjangoBatchPatchMutation):
    class Meta:
        model = Room
        permissions = ("core.change_room",)
        only_fields = ("id", "name", "short_name")
