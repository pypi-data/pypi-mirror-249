from dateutil.relativedelta import relativedelta
from edc_visit_schedule.schedule import Schedule
from edc_visit_schedule.tests.dummy_panel import DummyPanel
from edc_visit_schedule.visit import Crf, FormsCollection, Requisition, Visit
from edc_visit_schedule.visit_schedule import VisitSchedule


class Panel(DummyPanel):
    """`requisition_model` is normally set when the lab profile
    is set up.
    """

    def __init__(self, name):
        super().__init__(
            requisition_model="edc_subject_dashboard.subjectrequisition", name=name
        )


crfs = FormsCollection(
    Crf(show_order=1, model="edc_subject_dashboard.crfone", required=True),
    Crf(show_order=2, model="edc_subject_dashboard.crftwo", required=True),
    Crf(show_order=3, model="edc_subject_dashboard.crfthree", required=True),
    Crf(show_order=4, model="edc_subject_dashboard.crffour", required=True),
    Crf(show_order=5, model="edc_subject_dashboard.crffive", required=True),
)

requisitions = FormsCollection(
    Requisition(show_order=10, panel=Panel("one"), required=True, additional=False),
    Requisition(show_order=20, panel=Panel("two"), required=True, additional=False),
    Requisition(show_order=30, panel=Panel("three"), required=True, additional=False),
    Requisition(show_order=40, panel=Panel("four"), required=True, additional=False),
    Requisition(show_order=50, panel=Panel("five"), required=True, additional=False),
    Requisition(show_order=60, panel=Panel("six"), required=True, additional=False),
)

visit_schedule1 = VisitSchedule(
    name="visit_schedule1",
    offstudy_model="edc_offstudy.subjectoffstudy",
    death_report_model="edc_visit_tracking.deathreport",
    locator_model="edc_locator.subjectlocator",
)

visit_schedule2 = VisitSchedule(
    name="visit_schedule2",
    offstudy_model="edc_offstudy.subjectoffstudy",
    death_report_model="edc_visit_tracking.deathreport",
    locator_model="edc_locator.subjectlocator",
)

schedule1 = Schedule(
    name="schedule1",
    onschedule_model="edc_subject_dashboard.onscheduleone",
    offschedule_model="edc_subject_dashboard.offscheduleone",
    consent_model="edc_visit_tracking.subjectconsent",
    appointment_model="edc_appointment.appointment",
)


visits = []
for index in range(0, 4):
    visits.append(
        Visit(
            code=f"{index + 1}000",
            title=f"Day {index + 1}",
            timepoint=index,
            rbase=relativedelta(days=index),
            rlower=relativedelta(days=0),
            rupper=relativedelta(days=6),
            requisitions=requisitions,
            crfs=crfs,
            facility_name="7-day-clinic",
            allow_unscheduled=True,
        )
    )
for visit in visits:
    schedule1.add_visit(visit)

schedule2 = Schedule(
    name="schedule2",
    onschedule_model="edc_subject_dashboard.onscheduletwo",
    offschedule_model="edc_subject_dashboard.offscheduletwo",
    consent_model="edc_visit_tracking.subjectconsent",
    appointment_model="edc_appointment.appointment",
    base_timepoint=4,
)


visits = []
for index in range(4, 8):
    visits.append(
        Visit(
            code=f"{index + 1}000",
            title=f"Day {index + 1}",
            timepoint=index,
            rbase=relativedelta(days=index),
            rlower=relativedelta(days=0),
            rupper=relativedelta(days=6),
            requisitions=requisitions,
            crfs=crfs,
            facility_name="7-day-clinic",
        )
    )
for visit in visits:
    schedule2.add_visit(visit)

visit_schedule1.add_schedule(schedule1)
visit_schedule2.add_schedule(schedule2)
