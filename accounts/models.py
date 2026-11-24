from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('staff', 'Staff'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def save(self, *args, **kwargs):
        # Staff-role users should be able to reach /admin/
        if self.role == 'staff':
            self.is_staff = True
        super().save(*args, **kwargs)

    def is_student(self):
        return self.role == 'student'

    def is_staff_member(self):
        return self.role == 'staff'