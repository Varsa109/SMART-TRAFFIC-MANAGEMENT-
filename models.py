from django.core.validators import RegexValidator
from django.db import models


class Student(models.Model):
    YEAR_CHOICES = [(1, "Year 1"), (2, "Year 2"), (3, "Year 3"), (4, "Year 4")]
    STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]

    roll_no = models.CharField(
        max_length=20,
        unique=True,
        validators=[RegexValidator(r"^[A-Za-z0-9\-]+$", "Roll number may only contain letters, numbers and hyphens.")],
    )
    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    course = models.CharField(max_length=120)
    year = models.PositiveSmallIntegerField(choices=YEAR_CHOICES, default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["roll_no"]

    def __str__(self):
        return f"{self.roll_no} — {self.name}"
