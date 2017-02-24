import pytz
from django.dispatch import Signal
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from config import settings
from foodsaving.groups.models import Group as GroupModel
from foodsaving.history.utils import get_changed_data

post_group_create = Signal()
post_group_modify = Signal()


class TimezoneField(serializers.Field):
    def to_representation(self, obj):
        return str(obj)

    def to_internal_value(self, data):
        try:
            return pytz.timezone(str(data))
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValidationError('Unknown timezone')


class GroupDetailSerializer(serializers.ModelSerializer):
    "use this also for creating and updating a group"
    class Meta:
        model = GroupModel
        fields = [
            'id',
            'name',
            'description',
            'public_description',
            'members',
            'address',
            'latitude',
            'longitude',
            'password',
            'timezone'
        ]
        extra_kwargs = {
            'members': {
                'read_only': True
            },
            'description': {
                'trim_whitespace': False,
                'max_length': settings.DESCRIPTION_MAX_LENGTH
            },
            'password': {
                'trim_whitespace': False,
                'max_length': 255
            }
        }
    timezone = TimezoneField()

    def update(self, group, validated_data):
        changed_data = get_changed_data(group, validated_data)
        group = super().update(group, validated_data)

        if changed_data:
            post_group_modify.send(
                sender=self.__class__,
                group=group,
                user=self.context['request'].user,
                payload=changed_data)
        return group

    def create(self, validated_data):
        user = self.context['request'].user
        group = GroupModel.objects.create(**validated_data)
        group.members.add(user)
        group.save()
        post_group_create.send(sender=self.__class__, group=group, user=user, payload=self.initial_data)
        return group


class GroupPreviewSerializer(serializers.ModelSerializer):
    """
    Public information for all visitors
    should be readonly
    """
    class Meta:
        model = GroupModel
        fields = [
            'id',
            'name',
            'public_description',
            'address',
            'latitude',
            'longitude',
            'members',
            'protected'
        ]

    protected = serializers.SerializerMethodField()

    def get_protected(self, group):
        return group.password != ''