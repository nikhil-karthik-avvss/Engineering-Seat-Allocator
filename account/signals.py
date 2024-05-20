# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from pages.models import Set, Student, RankList, ChoiceListTable, SeatMatrix
from django.db.models.signals import post_save

@receiver(post_save, sender=Set)
def update_ranklist_on_flag(sender, instance, created, **kwargs):
    if not created and instance.Allow_Create_CRL == 1:
        # Fetch all students and sort them based on criteria
        sorted_students = Student.objects.filter(Allow_Login=1).order_by('-Cut_Off_Marks', '-Maths_Marks', '-Physics_Marks', '-Chemistry_Marks', 'DOB', 'Name', 'Fathers_Name')

        # Delete existing RankList records
        RankList.objects.all().delete()

        # Insert sorted students into RankList table
        for rank, student in enumerate(sorted_students, start=1):
            stud_obj=Student.objects.get(Student_ID=student.Student_ID)
            stud_obj.Rank = rank
            stud_obj.save()
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

@receiver(post_save, sender=Set)
def allow_seat(sender,instance,created,**kwargs):
    if not created and instance.Allot_Program == 1:
        ranklist = RankList.objects.all()
        for rank in ranklist:
            choice_obj = ChoiceListTable.objects.filter(Student_ID=rank.ID)
            flag=0
            stud = Student.objects.filter(Student_ID=rank.ID).first()
            for choice in choice_obj:
                sm = SeatMatrix.objects.filter(College_ID=choice.College_ID,Program=choice.Program).first()
                print(sm)
                if(sm.Seats_Available!=-1):
                    flag=1
                    sm.Seats_Available-=1
                    
                    stud.Allotted_College = choice.College
                    stud.Allotted_Course = choice.Program
                    stud.save()
                    choice_obj.delete()
                    break
            if(flag==0):
                stud.Allotted_College = "Not Allotted"
                stud.Allotted_Course = "Not Allotted"
                stud.save()

