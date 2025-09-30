from django.db import models
from django.conf import settings
from django.utils import timezone


# Create your models here.
class EnquiryType(models.Model):
    enquiry_type = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.enquiry_type

class TeleCaller(models.Model):
    tele_caller_name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.tele_caller_name

class ReferenceType(models.Model):
    reference_type = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reference_type


class Enquiry(models.Model):
    enquiry_id = models.CharField(max_length=20, unique=True, editable=False)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    whatsapp_number = models.CharField(max_length=10)
    address = models.TextField()
    enquiry_type = models.ForeignKey(EnquiryType, on_delete=models.RESTRICT, null=True)
    service_description = models.TextField()
    reference_type = models.ForeignKey(ReferenceType, on_delete=models.RESTRICT, null=True)
    customer_reference_name = models.CharField(max_length=255, blank=True, null=True)
    tele_caller_name = models.ForeignKey(TeleCaller, on_delete=models.RESTRICT, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='enquiries_created'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='enquiries_updated'
    )

    def save(self, *args, **kwargs):
        if not self.enquiry_id:
            last_enquiry = Enquiry.objects.order_by('-id').first()
            if last_enquiry and last_enquiry.enquiry_id:
                last_id = int(last_enquiry.enquiry_id.replace('ENQ', ''))
            else:
                last_id = 0
            self.enquiry_id = f'ENQ{last_id + 1:06d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.enquiry_id    

    class Meta:
        verbose_name_plural = 'Enquiries'
