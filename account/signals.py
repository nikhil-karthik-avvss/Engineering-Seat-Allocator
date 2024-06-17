# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from pages.models import Set, Student, RankList, ChoiceListTable, SeatMatrix, Previous
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
    if not created and instance.Allot_Program == 1 and instance.ReAllot==0:
        ranklist = RankList.objects.all()
        for rank in ranklist:
            choice_obj = ChoiceListTable.objects.filter(Student_ID=rank.ID)
            flag=0
            stud = Student.objects.filter(Student_ID=rank.ID).first()
            for choice in choice_obj:
                sm = SeatMatrix.objects.filter(College_ID=choice.College_ID,Program=choice.Program).first()
                print(sm.College_ID,sm.Program,sm.Seats_Available)
                if(sm.Seats_Available>0):
                    flag=1
                    sm.Seats_Available-=1
                    stud.Choice_Number = choice.Choice_Number
                    stud.Allotted_College = choice.College
                    stud.Allotted_Course = choice.Program
                    stud.Course_ID = sm.pk
                    stud.save()
                    sm.save()
                    #choice_obj.delete()
                    break
                sm.save()
            if(flag==0):
                stud.Allotted_College = "Not Allotted"
                stud.Allotted_Course = "Not Allotted"
                stud.Choice_Number = len(SeatMatrix.objects.all())+1
                stud.save()

@receiver(post_save, sender=Set)
def handle_reallot(sender, instance, created, **kwargs):
    if not created and instance.ReAllot == 1:
        ranklist = RankList.objects.all()
        students = Student.objects.all()
        for stud in students:
            #print(stud.Student_ID)
            if(stud.Allot_Stat<0):
                college = stud.Allotted_College
                course = stud.Allotted_Course
                course_id = stud.Course_ID
                sm = SeatMatrix.objects.filter(pk=course_id).first()
                #print(course_id,course)
                if(sm):
                    sm.Seats_Available+=1
                    sm.save()
                print(sm.pk,sm.Seats_Available)
        '''
        allot_stat = {
            'accept': 2,
            'accept_upward': 3,
            'decline': -1,
            'decline_upward': -2,
        }.get(action, 1)
        '''
        for rank in ranklist:
            stud = Student.objects.filter(Student_ID=rank.ID).first()
            print(stud.Student_ID)
            print(stud.Allot_Stat==2 or stud.Allot_Stat==-1)
            if(stud.Allot_Stat==2 or stud.Allot_Stat==-1):
                print('B1')
                if(stud.Allot_Stat==-1):
                    print('B2')
                    stud.Allotted_College = "Declined Allotment"
                    stud.Allotted_Course = "Declined Allotment"
                    stud.save()
                continue
            if (True):#instance.Allot_Program == 1:
                # Accept and Upward scenario
                choice_obj = ChoiceListTable.objects.filter(Student_ID=rank.ID)
                flag = False
                for choice in choice_obj:
                    sm = SeatMatrix.objects.filter(College_ID=choice.College_ID, Program=choice.Program).first()
                    if (sm and sm.Seats_Available > 0 and (choice.Choice_Number < stud.Choice_Number)):
                        flag = True
                        sm.Seats_Available -= 1
                        if(stud.Allot_Stat==3):
                            osm = SeatMatrix.objects.filter(pk=stud.Course_ID).first()
                            osm.Seats_Available += 1
                            osm.save()
                        stud.Choice_Number = choice.Choice_Number
                        stud.Allotted_College = choice.College
                        stud.Allotted_Course = choice.Program
                        stud.Course_ID = sm.pk
                        stud.save()
                        sm.save()
                        #choice_obj.delete()
                        break
                
                if not flag:
                    if(stud.Allot_Stat==-2):
                        stud.Allotted_College = "Lost Allotment"
                        stud.Allotted_Course = "Lost Allotment"
                    stud.save()
        
        students = Student.objects.all()
        for stud in students:
            psa = Previous(Rank=stud.Rank,CutOff=stud.Cut_Off_Marks,College=stud.Allotted_College,Course=stud.Allotted_Course)
            psa.save()
    '''
            Rank = models.IntegerField()
    CutOff = models.IntegerField()
    College = models.TextField()
    Course = models.TextField()
    '''
'''
            elif instance.Allot_Program == -1:
                # Decline and Upward scenario
                stud.Allotted_College = "Not Allotted"
                stud.Allotted_Course = "Not Allotted"
                stud.save()
'''


