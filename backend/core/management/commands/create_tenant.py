from django.core.management.base import BaseCommand
from tenants.models import Tenant, Domain


class Command(BaseCommand):
    help = "Create the initial tenant and domain for HCW@Home deployment"

    def handle(self, *args, **options):
        schema_name = "zuhair"
        tenant_name = "Dr. Zuhair Clinic"
        domain = "hcw.zuhairabusalma.com"

        tenant, created = Tenant.objects.get_or_create(
            schema_name=schema_name,
            defaults={"name": tenant_name},
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created tenant '{tenant_name}' (schema: {schema_name})"))
        else:
            self.stdout.write(f"Tenant '{schema_name}' already exists")

        dom, dom_created = Domain.objects.get_or_create(
            domain=domain,
            defaults={"tenant": tenant, "is_primary": True},
        )
        if dom_created:
            self.stdout.write(self.style.SUCCESS(f"Created domain '{domain}'"))
        else:
            self.stdout.write(f"Domain '{domain}' already exists")

        # Also allow the Railway default domain
        railway_domain = "hcw-web-production.up.railway.app"
        rd, rd_created = Domain.objects.get_or_create(
            domain=railway_domain,
            defaults={"tenant": tenant, "is_primary": False},
        )
        if rd_created:
            self.stdout.write(self.style.SUCCESS(f"Created domain '{railway_domain}'"))
