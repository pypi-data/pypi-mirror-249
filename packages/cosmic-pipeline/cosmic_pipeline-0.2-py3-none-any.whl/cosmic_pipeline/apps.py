import logging

from django.apps import AppConfig
from django.conf import settings
from django.db import connection
from django.db.models.signals import pre_save
from django.db.utils import ProgrammingError

logger = logging.getLogger(__name__)


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class CosmicPipelineConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cosmic_pipeline"

    def ready(self):
        self.connect_signals("cosmic_pipeline_workflow")


    def process_signals(self):
        from cosmic_pipeline.models.workflow import Workflow
        from django.apps import apps
        from cosmic_pipeline.handler import handle_state_change

        try:
            for workflow in Workflow.objects.all().values(
                "workflow_model__app_label", "workflow_model__model"
            ):
                Model = apps.get_model(
                    workflow.get("workflow_model__app_label"),
                    workflow.get("workflow_model__model"),
                )
                pre_save.connect(
                    handle_state_change,
                    sender=Model,
                    dispatch_uid="handle_state_change_" + Model.__name__.lower(),
                )

        except ProgrammingError:
            logger.warning(
                f"{bcolors.WARNING}WARNING:{bcolors.ENDC}\n"
                f"Cosmic Pipeline migrations missing.\n"
                f"Run 'python manage.py migrate cosmic_pipeline' to fix this.\n"
            )
        except Exception:
            logger.warning(
                f"{bcolors.WARNING}WARNING:{bcolors.ENDC}\n"
                "Issue connecting cosmic signals.\n"
            )

    def get_all_schemas(self, public_schema_name):
        all_schemas = []
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT schema_name FROM information_schema.schemata WHERE "
                f"schema_name NOT LIKE 'pg_%' "
                f"AND schema_name NOT LIKE 'information_schema' "
                f"AND schema_name NOT  like '{public_schema_name}';"
            )
            schema_rows = cursor.fetchall()
            for row in schema_rows:
                schema_name = row[0]
                all_schemas.append(schema_name)
        return all_schemas

    def check_using_django_tenants(self):
        has_django_tenants = False
        if getattr(settings, "INSTALLED_APPS", []):
            if "django_tenants" in settings.INSTALLED_APPS:
                has_django_tenants = True
        return has_django_tenants

    def connect_signals(self, table_name):
        COSMIC_PIPELINE_USING_DJANGO_TENANTS = getattr(
            settings, "COSMIC_PIPELINE_USING_DJANGO_TENANTS", False
        )
        if (
            self.check_using_django_tenants()
            and not COSMIC_PIPELINE_USING_DJANGO_TENANTS
        ):
            logger.warning(
                f"{bcolors.WARNING}WARNING:\n{bcolors.ENDC}"
                f"Detected django-tenants"
                f"and COSMIC_PIPELINE_USING_DJANGO_TENANTS is False.\n"
                f"Recommend setting COSMIC_PIPELINE_USING_DJANGO_TENANTS=True\n"
            )

        if COSMIC_PIPELINE_USING_DJANGO_TENANTS:
            try:
                from django_tenants.utils import schema_context
                from django_tenants.utils import get_public_schema_name
            except ImportError:
                raise ImportError(
                    "Using COSMIC_PIPELINE_USING_DJANGO_TENANTS=True requires django-tenants to be installed. And you need to add 'django_tenants' to INSTALLED_APPS."
                    "See https://django-tenants.readthedocs.io/en/latest/install.html"
                    "Limitations: Postgres only."
                )

            if self.name not in getattr(settings, "SHARED_APPS", []):
                schema_list = self.get_all_schemas(get_public_schema_name())
                if schema_list:
                    schema = schema_list[0]
                    with schema_context(schema):
                        self.process_signals()
                else:
                    logger.warning(
                        "\nNo schemas found. Signals not connected. Create a schema to connect signals.\n"
                    )
                return
        self.process_signals()
        return
