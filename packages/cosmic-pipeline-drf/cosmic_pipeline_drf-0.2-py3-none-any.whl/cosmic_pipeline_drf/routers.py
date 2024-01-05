from rest_framework import routers

from cosmic_pipeline_drf.views import (
    WorkflowViewSet,
    TransitionStateViewSet,
    TransitionViewSet,
    RulesViewSet
)

router = routers.DefaultRouter()
router.register(r"workflow", WorkflowViewSet)
router.register(r"workflow/(?P<workflow_pk>.+?)/state", TransitionStateViewSet)
router.register(r"workflow/(?P<workflow_pk>.+?)/transition", TransitionViewSet)
router.register(r"workflow/(?P<workflow_pk>.+?)/transition/(?P<transition_pk>.+?)/rules", RulesViewSet)
