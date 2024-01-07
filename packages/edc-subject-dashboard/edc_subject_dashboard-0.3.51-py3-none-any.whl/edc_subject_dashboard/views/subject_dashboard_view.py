from __future__ import annotations

from typing import Any

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _
from edc_action_item.view_mixins import ActionItemViewMixin
from edc_appointment.view_mixins import AppointmentViewMixin
from edc_consent.view_mixins import ConsentViewMixin
from edc_dashboard.view_mixins import EdcViewMixin
from edc_dashboard.views import DashboardView
from edc_data_manager.view_mixins import DataManagerViewMixin
from edc_locator.utils import get_locator_model
from edc_locator.view_mixins import SubjectLocatorViewMixin
from edc_metadata.view_mixins import MetadataViewMixin
from edc_navbar.view_mixin import NavbarViewMixin
from edc_sites.site import sites
from edc_subject_model_wrappers import (
    AppointmentModelWrapper,
    RelatedVisitModelWrapper,
    SubjectConsentModelWrapper,
    SubjectLocatorModelWrapper,
)
from edc_visit_schedule.view_mixins import VisitScheduleViewMixin

from ..view_mixins import RegisteredSubjectViewMixin, SubjectVisitViewMixin


class VerifyRequisitionMixin:
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        scanning = self.kwargs.get("scanning")
        kwargs.update(scanning=scanning)
        return super().get_context_data(**kwargs)


class SubjectDashboardView(
    EdcViewMixin,
    NavbarViewMixin,
    MetadataViewMixin,
    ConsentViewMixin,
    SubjectLocatorViewMixin,
    ActionItemViewMixin,
    DataManagerViewMixin,
    SubjectVisitViewMixin,
    AppointmentViewMixin,
    VisitScheduleViewMixin,
    RegisteredSubjectViewMixin,
    VerifyRequisitionMixin,
    DashboardView,
):
    navbar_selected_item = "consented_subject"

    dashboard_url_name = "subject_dashboard_url"
    dashboard_template = "subject_dashboard_template"

    appointment_model = "edc_appointment.appointment"
    appointment_model_wrapper_cls = AppointmentModelWrapper

    consent_model = None
    consent_model_wrapper_cls = SubjectConsentModelWrapper

    subject_locator_model = get_locator_model()
    subject_locator_model_wrapper_cls = SubjectLocatorModelWrapper

    visit_model = None
    visit_model_wrapper_cls = RelatedVisitModelWrapper

    history_button_label = _("Audit")

    default_manager = "on_site"

    def __init__(self, **kwargs):
        if not self.navbar_name:
            raise ImproperlyConfigured(f"'navbar_name' cannot be None. See {repr(self)}.")
        self.appointment_model_wrapper_cls.visit_model_wrapper_cls = (
            self.visit_model_wrapper_cls
        )
        if self.visit_model:
            self.visit_model_wrapper_cls.model = self.visit_model
        else:
            self.visit_model = self.visit_model_wrapper_cls.model
        if self.consent_model:
            self.consent_model_wrapper_cls.model = self.consent_model
        else:
            self.consent_model = self.consent_model_wrapper_cls.model
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        kwargs.update(history_button_label=self.history_button_label)
        return super().get_context_data(**kwargs)

    @property
    def manager(self) -> str:
        """Returns the name of the model manager"""
        if sites.user_may_view_other_sites(self.request):
            return "objects"
        return self.default_manager
