from django.db import models
from evercycle_models.models.organization import Organization
from .address import Address
from .processor import Processor
from .service_provider_service import ServiceProviderService
from .certification import Certification


class ServiceProvider(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    name = models.CharField(max_length=50)
    logo = models.BinaryField(blank=True, null=True)
    description = models.CharField(max_length=50)
    device_specialization = models.CharField(max_length=255)
    industry_specialization = models.CharField(max_length=255)
    report_services = models.TextField()
    warehouse_security = models.TextField()
    audit_report_sla = models.TextField()
    sample_audit_report = models.BinaryField(blank=True, null=True)
    device_audit_pictures = models.TextField()
    data_erasure_id = models.TextField()
    payment_terms = models.TextField()
    payment_methods = models.TextField()
    service_provider_workflow_email = models.EmailField(max_length=50)
    headquarters_address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        related_name='headquarter_service_providers'  # Unique related name
    )
    warehouse_address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        related_name='warehouse_service_providers'  # Unique related name
    )
    organization = models.ForeignKey(Organization, models.DO_NOTHING)
    processor = models.ForeignKey(Processor, models.DO_NOTHING)
    service_provider_services = models.ManyToManyField(ServiceProviderService)
    certifications = models.ManyToManyField(Certification)

    class Meta:
        db_table = 'service_provider'
