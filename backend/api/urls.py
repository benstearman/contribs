from django.urls import include, path
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r"contributions", views.ContributionViewSet)
router.register(r"contributors", views.ContributorViewSet)
router.register(r"candidates", views.CandidateViewSet)
router.register(r"committees", views.CommitteeViewSet)
router.register(r"parties", views.PartyViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]