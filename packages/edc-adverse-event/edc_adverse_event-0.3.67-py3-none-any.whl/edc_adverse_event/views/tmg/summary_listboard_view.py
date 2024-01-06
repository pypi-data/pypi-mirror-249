from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.core.exceptions import ObjectDoesNotExist
from edc_dashboard.view_mixins import EdcViewMixin
from edc_listboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_listboard.views import ListboardView as BaseListboardView
from edc_navbar import NavbarViewMixin
from edc_utils import get_utcnow

from ...auth_objects import TMG
from ...constants import (
    AE_FOLLOWUP_ACTION,
    AE_TMG_ACTION,
    DEATH_REPORT_ACTION,
    DEATH_REPORT_TMG_ACTION,
)
from ...model_wrappers import TmgActionItemModelWrapper as BaseTmgActionItemModelWrapper
from ...utils import get_adverse_event_app_label

if TYPE_CHECKING:
    from django.db.models import Q


class TmgActionItemModelWrapper(BaseTmgActionItemModelWrapper):
    next_url_name = "tmg_summary_listboard_url"


class SummaryListboardView(
    NavbarViewMixin,
    EdcViewMixin,
    ListboardFilterViewMixin,
    SearchFormViewMixin,
    BaseListboardView,
):
    listboard_back_url = "tmg_home_url"

    ae_tmg_model = f"{get_adverse_event_app_label()}.aetmg"
    listboard_template = "tmg_summary_listboard_template"
    listboard_url = "tmg_summary_listboard_url"
    listboard_panel_style = "warning"
    listboard_model = "edc_action_item.actionitem"
    listboard_panel_title = "TMG: Events Summary"
    listboard_view_permission_codename = "edc_adverse_event.view_tmg_listboard"

    model_wrapper_cls = TmgActionItemModelWrapper
    navbar_selected_item = "tmg_home"
    ordering = "-report_datetime"
    paginate_by = 25
    search_form_url = "tmg_summary_listboard_url"
    action_type_names = [
        AE_TMG_ACTION,
        DEATH_REPORT_TMG_ACTION,
        DEATH_REPORT_ACTION,
        AE_FOLLOWUP_ACTION,
    ]
    search_fields = [
        "subject_identifier",
        "action_identifier",
        "parent_action_item__action_identifier",
        "related_action_item__action_identifier",
        "user_created",
        "user_modified",
    ]

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        kwargs.update(AE_TMG_ACTION=AE_TMG_ACTION, utc_date=get_utcnow().date())
        return super().get_context_data(**kwargs)

    def get_queryset_filter_options(self, request, *args, **kwargs) -> tuple[Q, dict]:
        q_object, options = super().get_queryset_filter_options(request, *args, **kwargs)
        options.update({"action_type__name__in": self.action_type_names})
        return q_object, options

    def update_wrapped_instance(self, model_wrapper) -> TmgActionItemModelWrapper:
        model_wrapper.has_reference_obj_permissions = True
        model_wrapper.has_parent_reference_obj_permissions = True
        model_wrapper.has_related_reference_obj_permissions = True
        try:
            self.request.user.groups.get(name=TMG)
        except ObjectDoesNotExist:
            pass
        else:
            if (
                model_wrapper.reference_obj
                and model_wrapper.reference_obj._meta.label_lower == self.ae_tmg_model
            ):
                model_wrapper.has_reference_obj_permissions = (
                    model_wrapper.reference_obj.user_created == self.request.user.username
                )
            if (
                model_wrapper.parent_reference_obj
                and model_wrapper.parent_reference_obj._meta.label_lower == self.ae_tmg_model
            ):  # noqa
                model_wrapper.has_parent_reference_obj_permissions = (
                    model_wrapper.parent_reference_obj.user_created
                    == self.request.user.username
                )  # noqa
            if (
                model_wrapper.related_reference_obj
                and model_wrapper.related_reference_obj._meta.label_lower == self.ae_tmg_model
            ):  # noqa
                model_wrapper.has_related_reference_obj_permissions = (
                    model_wrapper.related_reference_obj.user_created
                    == self.request.user.username
                )  # noqa
        return model_wrapper
