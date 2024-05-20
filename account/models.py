from django.db import models

# Create your models here.
from pages.models import Set, Student
from django.dispatch import receiver
from .signals import update_ranklist_on_flag
from django.db.models.signals import post_save
#from pages.tasks import process_flag


@receiver(post_save, sender=Set)
def update_ranklist_on_flag(sender, instance, created, **kwargs):
    if created and instance.Allow_Create_CRL == 1:  # Check if a new Set instance is created with Allow_CRL set to 1
        # Fetch all students and sort them based on criteria
        sorted_students = Student.objects.order_by('-Cut_Off_Marks', '-Maths_Marks', '-Physics_Marks', '-Chemistry_Marks', 'DOB', 'Name', 'Fathers_Name')
        #filter(Allow_Login=1).
        # Delete existing RankList records (optional, depending on your requirements)
        RankList.objects.all().delete()

        # Insert sorted students into RankList table
        for rank, student in enumerate(sorted_students, start=1):
            RankList.objects.create(
                Rank=rank,
                ID=student.Student_ID,
                Name=student.Name,
                DOB=student.DOB,
                Fathers_Name=student.Fathers_Name,
                Maths_Marks=student.Maths_Marks,
                Physics_Marks=student.Physics_Marks,
                Chemistry_Marks=student.Chemistry_Marks,
                Cut_Off_Marks=student.Cut_Off_Marks,
            )

