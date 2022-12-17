from rest_framework import serializers

from .models import File, ParsingStatus


class FileUploadSerializer(serializers.ModelSerializer):
    file = serializers.ListField(
        child=serializers.FileField(max_length=100000,
                                    allow_empty_file=False,
                                    use_url=False))

    class Meta:
        model = File
        fields = ['file']

    def create(self, validated_data):
        uploaded_by = self.context['request'].user
        file = validated_data.pop('file')
        audio_list = []
        for record in file:
            file_name = str(record)
            audio = File.objects.create(file=record, file_name=file_name, user=uploaded_by)
            audio_url = f'{audio.file.url}'
            audio_list.append(audio_url)
        return audio_list


class FileSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    user = serializers.StringRelatedField()

    class Meta:
        model = File
        fields = ['file_name', 'file', 'status', 'insert_date', 'user']

    def get_status(self, obj: File):

        try:
            return obj.statuses.status
        except File.statuses.RelatedObjectDoesNotExist:
            return None