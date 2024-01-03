from rest_framework import serializers
from kfsd.apps.core.utils.dict import DictUtils


class BaseModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    identifier = serializers.CharField(required=False)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    slug = serializers.SlugField(read_only=True)

    def get_model_class(self):
        return self.Meta.model

    def exists(self):
        raw_data = self.initial_data
        identifier = DictUtils.get(raw_data, "identifier")
        if identifier:
            return self.get_model_class().objects.filter(identifier=identifier).exists()
        else:
            return False

    def get_instance(self):
        raw_data = self.initial_data
        identifier = DictUtils.get(raw_data, "identifier")
        return self.get_model_class().objects.get(identifier=identifier)
