from rest_framework import mixins, viewsets

from apps.preference.models import UserPreference
from apps.preference.serializers import UserPreferenceSerializer


class UserPreferenceViewSet(mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    serializer_class = UserPreferenceSerializer
    queryset = UserPreference.objects.all()

    def get_queryset(self):
        qs = self.queryset

        if 'telegram_pk' in self.kwargs:
            qs = qs.filter(telegram_user=self.kwargs['telegram_pk'])

        return qs
