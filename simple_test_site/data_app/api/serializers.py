from rest_framework import serializers

from data_app.models import DataModels


class DataPostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_author')

    class Meta:
        model = DataModels
        fields = ['title', 'body', 'date_updated', 'username']

    def get_username_from_author(self, data_post):
        username = data_post.author.username
        return username
