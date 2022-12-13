import os
from rest_framework import serializers

from .models import File


class FileUploadSerializer(serializers.ModelSerializer):
    file = serializers.ListField(
        child=serializers.FileField(max_length=100000,
                                    allow_empty_file=False,
                                    use_url=False))

    class Meta:
        model = File
        fields = ['file']

    def create(self, validated_data):
        file = validated_data.pop('file')
        audio_list = []
        for record in file:
            file_name = str(record)
            audio = File.objects.create(file=record, file_name=file_name)
            audio_url = f'{audio.file.url}'
            audio_list.append(audio_url)
        return audio_list


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = '__all__'
