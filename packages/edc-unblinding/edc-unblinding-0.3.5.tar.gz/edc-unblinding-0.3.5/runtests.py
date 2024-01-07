#!/usr/bin/env python
import logging
from pathlib import Path

from edc_constants.constants import IGNORE
from edc_test_utils import DefaultTestSettings, func_main

app_name = "edc_unblinding"
base_dir = Path(__file__).absolute().parent

project_settings = DefaultTestSettings(
    calling_file=__file__,
    template_dirs=[str(base_dir / app_name / "tests" / "templates")],
    BASE_DIR=base_dir,
    APP_NAME=app_name,
    ETC_DIR=str(base_dir / app_name / "tests" / "etc"),
    EDC_AUTH_CODENAMES_WARN_ONLY=True,
    EDC_NAVBAR_VERIFY_ON_LOAD=IGNORE,
    SUBJECT_SCREENING_MODEL="visit_schedule_app.subjectscreening",
    SUBJECT_CONSENT_MODEL="visit_schedule_app.subjectconsent",
    SUBJECT_VISIT_MODEL="edc_visit_tracking.subjectvisit",
    SUBJECT_VISIT_MISSED_MODEL="visit_schedule_app.subjectvisitmissed",
    SUBJECT_REQUISITION_MODEL="visit_schedule_app.subjectrequisition",
    EXTRA_INSTALLED_APPS=["visit_schedule_app.apps.AppConfig"],
    DASHBOARD_BASE_TEMPLATES={
        "dashboard_template": str(
            base_dir / "edc_unblinding" / "tests" / "templates" / "dashboard.html"
        ),
        "dashboard2_template": str(
            base_dir / "edc_unblinding" / "tests" / "templates" / "dashboard2.html"
        ),
    },
    use_test_urls=True,
    add_dashboard_middleware=True,
    add_lab_dashboard_middleware=True,
).settings


def main():
    func_main(project_settings, *[f"{app_name}.tests"])


if __name__ == "__main__":
    logging.basicConfig()
    main()
