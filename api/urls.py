from rest_framework import routers

from api.views import SecretKeyViewSet

router = routers.DefaultRouter()

router.register('secrets', SecretKeyViewSet, 'secrets')

urlpatterns = router.urls
