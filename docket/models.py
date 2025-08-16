from django.db import models
from django.conf import settings
from django.utils import timezone

from enquiry.models import Enquiry
from accounts.models import User

STATUS_CHOICES = [
        ('Created', 'Created'),
        ('Assigned/Initiated', 'Assigned/Initiated'),
        ('Parts Required (Pending)', 'Parts Required (Pending)'),
        ('Taken for Servicing (Pending)', 'Taken for Servicing (Pending)'),
        ('Solved', 'Solved'),
    ]

class Docket(models.Model):
    docket_id = models.CharField(max_length=20, unique=True, editable=False)
    enquiry = models.ForeignKey(Enquiry, null=True, blank=True, on_delete=models.RESTRICT, related_name='dockets')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15)
    dob = models.DateField(null=True, blank=True)
    problem_facing = models.TextField()
    expected_solution = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        null=True,
        limit_choices_to={'role': 'ADVISER', 'is_active': True},
        related_name='assigned_dockets'
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=STATUS_CHOICES[0])
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        null=True,
        related_name='created_dockets'
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.RESTRICT, 
        null=True, 
        related_name='updated_docket'
    )
    closed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.docket_id:
            last_docket = Docket.objects.order_by('-id').first()
            if last_docket and last_docket.docket_id:
                last_id = int(last_docket.docket_id.replace('DKT', ''))
            else:
                last_id = 0
            self.docket_id = f'DKT{last_id + 1:06d}'

        if self.status == 'Solved' and not self.closed_at:
            self.closed_at = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.docket_id
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class DocketUpdateLog(models.Model):
    docket_id = models.ForeignKey(Docket, on_delete=models.CASCADE, related_name='docket_update_log')
    assigned_engineer = models.ForeignKey(
        User, 
        on_delete=models.RESTRICT, 
        null=True, 
        blank=True,
        limit_choices_to={
            'role': 'ENGINEER',
            'is_active': True
        },
        related_name='assigned_engineer'
    )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.RESTRICT, 
        null=True, 
        blank=True,
        limit_choices_to={
            'is_active': True,
            'role__in': ['ADMIN', 'ADVISER']
        },
        related_name='updated_by_adviser'
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=STATUS_CHOICES[0])
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.docket_id.docket_id
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the DocketUpdateLog instance first

        # Update the related Docket's status
        docket = self.docket_id
        docket.status = self.status

        # Logic for closed_at handling
        if self.status == 'Solved':
            docket.closed_at = timezone.now()
        else:
            docket.closed_at = None

        docket.save()