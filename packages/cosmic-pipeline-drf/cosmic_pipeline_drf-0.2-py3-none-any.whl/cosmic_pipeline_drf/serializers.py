from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers, exceptions

from cosmic_pipeline.check import check_operations
from cosmic_pipeline.choices import model_fields_choices
from cosmic_pipeline.exceptions import CosmicPipelineValidationError
from cosmic_pipeline.models.rules import RestrictRuleCondition
from cosmic_pipeline.models.transition import Transition
from cosmic_pipeline.models.transitionstate import TransitionState
from cosmic_pipeline.models.workflow import (
    Workflow,
    get_workflow_choices,
    check_workflow_from_choices,
)


class RuleSerializerMixin:
    def validate(self, attrs):
        attrs = super().validate(attrs)
        transition = attrs.get("transition")
        field = attrs.get("field")
        operator = attrs.get("operator")
        annotate = attrs.get("annotate")

        if transition and field and operator:
            is_valid = check_operations(transition, field, operator, annotate)
            if not is_valid:
                raise CosmicPipelineValidationError(
                    f"Invalid operator for {field}", code="invalid_operator"
                )
        return attrs


class WorkflowSerializer(serializers.ModelSerializer):
    workflow_model = serializers.CharField(read_only=True, source="workflow_model.name")

    class Meta:
        model = Workflow
        fields = "__all__"

    def create(self, validated_data):
        # This is to prevent the workflow_model from being updated
        raise exceptions.NotAcceptable("Workflow model cannot be created")

    def update(self, instance, validated_data):
        # This is to prevent the workflow_model from being updated
        raise exceptions.NotAcceptable("Workflow model cannot be updated")


class WorkflowCreateSerializer(serializers.ModelSerializer):
    workflow_model = serializers.ChoiceField(choices=get_workflow_choices())

    class Meta:
        model = Workflow
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["workflow_model"] = instance.workflow_model.name
        return ret

    def validate_workflow_model(self, value):
        workflow_model = ContentType.objects.filter(pk=value)
        if not workflow_model:
            raise exceptions.ValidationError("Workflow model not found")
        workflow_model = workflow_model.first()
        if not check_workflow_from_choices(workflow_model=workflow_model):
            raise exceptions.ValidationError("Workflow model can not be used")
        return workflow_model

    def update(self, instance, validated_data):
        # This is to prevent the workflow_model from being updated
        raise exceptions.NotAcceptable("Workflow model cannot be updated")


class WorkflowUpdateSerializer(serializers.ModelSerializer):
    workflow_model = serializers.CharField(read_only=True, source="workflow_model.name")

    class Meta:
        model = Workflow
        fields = "__all__"

    def validate_workflow_model(self, value):
        workflow_model = ContentType.objects.filter(pk=value)
        if not workflow_model:
            raise exceptions.ValidationError("Workflow model not found")
        workflow_model = workflow_model.first()
        if not check_workflow_from_choices(workflow_model=workflow_model):
            raise exceptions.ValidationError("Workflow model can not be used")
        return workflow_model

    def create(self, validated_data):
        # This is to prevent the workflow_model from being updated
        raise exceptions.NotAcceptable("Workflow model cannot be created")


class TransitionStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransitionState
        fields = "__all__"

    def create(self, validated_data):
        # This is to prevent the workflow_model from being updated
        raise exceptions.NotAcceptable("TransitionState model cannot be created")

    def update(self, instance, validated_data):
        # This is to prevent the workflow_model from being updated
        raise exceptions.NotAcceptable("TransitionState model cannot be updated")


class TransitionStateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransitionState
        fields = "__all__"
        extra_kwargs = {"workflow": {"read_only": True}, "slug": {"read_only": True}}

    def create(self, validated_data):
        validated_data["workflow_id"] = self.context.get("workflow_pk")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # This is to prevent the workflow_model from being updated
        raise exceptions.NotAcceptable("TransitionState model cannot be updated")


class TransitionStateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransitionState
        fields = "__all__"
        extra_kwargs = {"workflow": {"read_only": True}, "slug": {"read_only": True}}

    def validate_workflow(self, value):
        if value.workflow_model.id != self.instance.workflow.workflow_model.id:
            if (
                self.instance.transitions_source.all()
                or self.instance.transitions_destination.all()
            ):
                raise exceptions.ValidationError("Workflow model cannot be changed")
        return value

    def create(self, validated_data):
        # This is to prevent the workflow_model from being updated
        raise exceptions.NotAcceptable("TransitionState model cannot be created")

    def update(self, instance, validated_data):
        validated_data["workflow_id"] = self.context.get("workflow_pk")
        return super().update(instance, validated_data)


class RuleConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestrictRuleCondition
        fields = "__all__"


class RuleConditionCreateSerializer(RuleSerializerMixin, serializers.ModelSerializer):
    field = serializers.ChoiceField(choices=[])

    class Meta:
        model = RestrictRuleCondition
        fields = "__all__"
        extra_kwargs = {"transition": {"read_only": True}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        transition_pk = self.context.get("transition_pk")
        transition = Transition.objects.filter(pk=transition_pk)
        if transition:
            transition = transition.first()
            choices = model_fields_choices(
                transition.workflow.workflow_model.model_class()
            )
            self.fields["field"] = serializers.ChoiceField(choices=choices)

    def create(self, validated_data):
        validated_data["transition_id"] = self.context.get("transition_pk")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # This is to prevent the workflow_model from being updated
        raise exceptions.NotAcceptable("RestrictRuleCondition model cannot be updated")


class RuleConditionUpdateSerializer(RuleSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = RestrictRuleCondition
        fields = "__all__"
        extra_kwargs = {"transition": {"read_only": True}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        transition_pk = self.context.get("transition_pk")
        transition = Transition.objects.filter(pk=transition_pk)
        if transition:
            transition = transition.first()
            choices = model_fields_choices(
                transition.workflow.workflow_model.model_class()
            )
            self.fields["field"] = serializers.ChoiceField(choices=choices)


    def create(self, validated_data):
        # This is to prevent the workflow_model from being updated
        raise exceptions.NotAcceptable("RestrictRuleCondition model cannot be created")


class TransitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transition
        fields = "__all__"


class TransitionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transition
        fields = "__all__"

    def validate_source_state(self, value):
        if str(value.workflow.id) != self.initial_data.get("workflow"):
            raise exceptions.ValidationError("Invalid State")
        return value

    def validate_destination_state(self, value):
        if str(value.workflow.id) != self.initial_data.get("workflow"):
            raise exceptions.ValidationError("Invalid State")
        return value


class TransitionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transition
        fields = "__all__"

    def validate_source_state(self, value):
        if str(value.workflow.id) != self.initial_data.get("workflow"):
            raise exceptions.ValidationError("Invalid State")
        return value

    def validate_destination_state(self, value):
        if str(value.workflow.id) != self.initial_data.get("workflow"):
            raise exceptions.ValidationError("Invalid State")
        return value
