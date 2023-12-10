from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from api.models import Users


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"
