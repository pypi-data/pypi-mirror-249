from django.conf import settings
from rest_framework import exceptions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from cosmic_pipeline.models.rules import RestrictRuleCondition
from cosmic_pipeline.models.transition import Transition
from cosmic_pipeline.models.transitionstate import TransitionState
from cosmic_pipeline.models.workflow import Workflow
from cosmic_pipeline_drf.serializers import (
    WorkflowSerializer,
    WorkflowUpdateSerializer,
    WorkflowCreateSerializer,
    TransitionStateSerializer,
    TransitionStateCreateSerializer,
    TransitionStateUpdateSerializer,
    TransitionSerializer,
    TransitionCreateSerializer,
    TransitionUpdateSerializer,
    RuleConditionSerializer,
    RuleConditionCreateSerializer,
    RuleConditionUpdateSerializer,
)

TAGS = getattr(settings, "COSMIC_PIPELINE_DRF_TAGS", "Workflow")
DELETE_STATUS_CODE = getattr(
    settings, "COSMIC_PIPELINE_DRF_DELETE_STATUS_CODE", status.HTTP_204_NO_CONTENT
)


class CustomModelViewSet(ModelViewSet):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=DELETE_STATUS_CODE)


class WorkflowViewSet(CustomModelViewSet):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer
    tags = [TAGS]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == "create":
            serializer_class = WorkflowCreateSerializer
        elif self.action in {"update", "partial_update"}:
            serializer_class = WorkflowUpdateSerializer
        return serializer_class

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.states.all() or instance.transitions.all():
            raise exceptions.ValidationError(
                "Cannot delete a workflow that has states or transitions"
            )
        self.perform_destroy(instance)
        return Response(status=DELETE_STATUS_CODE)


class TransitionStateViewSet(CustomModelViewSet):
    queryset = TransitionState.objects.all()
    serializer_class = TransitionStateSerializer
    tags = [TAGS]

    def get_queryset(self):
        workflow_pk = self.kwargs.get("workflow_pk")
        return self.queryset.filter(workflow__id=workflow_pk)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action in ["create", "update", "partial_update"]:
            context.update(
                {
                    "workflow_pk": self.kwargs.get("workflow_pk"),
                }
            )
        return context

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == "create":
            serializer_class = TransitionStateCreateSerializer
        elif self.action in {"update", "partial_update"}:
            serializer_class = TransitionStateUpdateSerializer
        return serializer_class

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.transitions_source.all() or instance.transitions_destination.all():
            raise exceptions.ValidationError(
                "Cannot delete a state that has transitions"
            )
        self.perform_destroy(instance)
        return Response(status=DELETE_STATUS_CODE)

    @action(detail=True, methods=["get"], url_path="next-states")
    def get_next_possible_states(self, request, pk=None,**kwargs):
        """
        Returns the next possible states for a given transition
        """
        state = self.get_object()
        _next_possible_states = state.next_possible_states()
        # next_possible_states = self.queryset.filter(
        #     id__in=_next_possible_states.values_list("id", flat=True)
        # )
        serializer = self.get_serializer(_next_possible_states, many=True)
        return Response(serializer.data)


class TransitionViewSet(CustomModelViewSet):
    queryset = Transition.objects.all()
    serializer_class = TransitionSerializer
    tags = [TAGS]

    def get_queryset(self):
        workflow_pk = self.kwargs.get("workflow_pk")
        return self.queryset.filter(workflow__id=workflow_pk)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action in ["create", "update", "partial_update"]:
            context.update(
                {
                    "workflow_pk": self.kwargs.get("workflow_pk"),
                }
            )
        return context

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == "create":
            serializer_class = TransitionCreateSerializer
        elif self.action in {"update", "partial_update"}:
            serializer_class = TransitionUpdateSerializer
        return serializer_class


class RulesViewSet(CustomModelViewSet):
    queryset = RestrictRuleCondition.objects.all()
    serializer_class = RuleConditionSerializer
    tags = [TAGS]

    def get_queryset(self):
        transition_pk = self.kwargs.get("transition_pk")
        workflow_pk = self.kwargs.get("workflow_pk")
        return self.queryset.filter(
            transition__id=transition_pk, transition__workflow__id=workflow_pk
        )

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == "create":
            serializer_class = RuleConditionCreateSerializer
        elif self.action in {"update", "partial_update"}:
            serializer_class = RuleConditionUpdateSerializer
        return serializer_class

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                "transition_pk": self.kwargs.get("transition_pk"),
                "workflow_pk": self.kwargs.get("workflow_pk"),
            }
        )
        return context
