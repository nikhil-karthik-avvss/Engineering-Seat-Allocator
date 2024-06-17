from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
from django.db.models import Max
from django.db.models import F
from django.db.models.functions import Coalesce
import random
from django.db.models.signals import post_save
from django.dispatch import receiver

#from pages.tasks import process_flag

'''
@receiver(post_save, sender=Set)
def update_ranklist_on_flag(sender, instance, created, **kwargs):
    if created and instance.Allow_Create_CRL == 1:  # Check if a new Set instance is created with Allow_CRL set to 1
        # Fetch all students and sort them based on criteria
        sorted_students = Student.objects.filter(Allow_Login=1).order_by('-Cut_Off_Marks', '-Maths_Marks', '-Physics_Marks', '-Chemistry_Marks', 'DOB', 'Name', 'Fathers_Name')

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
'''
def generate_student_id():
    current_year = str(datetime.now().year)[-2:]  # Get the last two digits of the current year
    last_student = Student.objects.all().aggregate(Max('Student_ID'))['Student_ID__max']
    last_id = int(str(last_student)[4:]) if last_student else 0  # Extracting the last four digits
    new_id = (int(current_year) * 100000) + last_id + 1
    return new_id
    
def validate_marks(value):
    if value < 0 or value > 100:
        raise ValueError("Marks should be between 0 and 100.")

def validate_cutoff(value):
    if value < 0 or value > 200:
        raise ValueError("Cut-off marks should be between 0 and 200.")

class Institute(models.Model):
    College_ID = models.AutoField(primary_key=True)
    College_Image_URL = models.URLField()
    College_Name = models.CharField(max_length=100)
    Address = models.TextField()
    Password = models.CharField(max_length=50)  # Adjust max_length as needed
    Administrator_Name = models.CharField(max_length=70)  # Adjust max_length as needed
    Email_ID = models.EmailField()
    Contact_Number = models.CharField(max_length=10)# Adjust max_length as needed
    Tution_Fee = models.IntegerField()
    Hostel_Fee_min = models.IntegerField()
    Hostel_Fee_max = models.IntegerField()
    Bus_Fee = models.IntegerField()
    Mand_Bus = models.TextField()
    Mess_Inc = models.TextField()
    Web = models.URLField()
    Certificate = models.FileField(upload_to='media/certificates/college/',blank=True, null=True)
    Flag = models.IntegerField()
    Log_Stat = models.IntegerField()
    def __str__(self):
        return self.College_Name

class SeatMatrix(models.Model):
    College_ID = models.IntegerField()
    College_Name = models.CharField(max_length=100)
    PROGRAM_CHOICES = [
        ('B.E. Computer Science and Engineering', 'Bachelor of Engineering in Computer Science and Engineering'),
    ('B.Tech. Computer Science and Engineering', 'Bachelor of Technology in Computer Science and Engineering'),
    ('B.E. Information Technology', 'Bachelor of Engineering in Information Technology'),
    ('B.Tech. Information Technology', 'Bachelor of Technology in Information Technology'),
    ('B.E. Artificial Intelligence and Machine Learning', 'Bachelor of Engineering in Artificial Intelligence and Machine Learning'),
    ('B.Tech. Artificial Intelligence and Machine Learning', 'Bachelor of Technology in Artificial Intelligence and Machine Learning'),
    ('B.E. Data Science and Analytics', 'Bachelor of Engineering in Data Science and Analytics'),
    ('B.Tech. Data Science and Analytics', 'Bachelor of Technology in Data Science and Analytics'),
    ('B.E. Cybersecurity', 'Bachelor of Engineering in Cybersecurity'),
    ('B.Tech. Cybersecurity', 'Bachelor of Technology in Cybersecurity'),
    ('B.E. Electronics and Communication Engineering', 'Bachelor of Engineering in Electronics and Communication Engineering'),
    ('B.Tech. Electronics and Communication Engineering', 'Bachelor of Technology in Electronics and Communication Engineering'),
    ('B.E. Robotics and Automation', 'Bachelor of Engineering in Robotics and Automation'),
    ('B.Tech. Robotics and Automation', 'Bachelor of Technology in Robotics and Automation'),
    ('B.E. Biotechnology', 'Bachelor of Engineering in Biotechnology'),
    ('B.Tech. Biotechnology', 'Bachelor of Technology in Biotechnology'),
    ('B.E. Nanotechnology', 'Bachelor of Engineering in Nanotechnology'),
    ('B.Tech. Nanotechnology', 'Bachelor of Technology in Nanotechnology'),
    ('B.E. Renewable Energy Engineering', 'Bachelor of Engineering in Renewable Energy Engineering'),
    ('B.Tech. Renewable Energy Engineering', 'Bachelor of Technology in Renewable Energy Engineering'),
    ('B.E. Aerospace Engineering', 'Bachelor of Engineering in Aerospace Engineering'),
    ('B.Tech. Aerospace Engineering', 'Bachelor of Technology in Aerospace Engineering'),
    ('B.E. Gaming Technology', 'Bachelor of Engineering in Gaming Technology'),
    ('B.Tech. Gaming Technology', 'Bachelor of Technology in Gaming Technology'),
    ('B.E. Mobile Application Development', 'Bachelor of Engineering in Mobile Application Development'),
    ('B.Tech. Mobile Application Development', 'Bachelor of Technology in Mobile Application Development'),
    ('B.E. Augmented Reality and Virtual Reality', 'Bachelor of Engineering in Augmented Reality and Virtual Reality'),
    ('B.Tech. Augmented Reality and Virtual Reality', 'Bachelor of Technology in Augmented Reality and Virtual Reality'),
    ('B.E. Internet of Things (IoT)', 'Bachelor of Engineering in Internet of Things (IoT)'),
    ('B.Tech. Internet of Things (IoT)', 'Bachelor of Technology in Internet of Things (IoT)'),
    ('B.E. Biomedical Engineering', 'Bachelor of Engineering in Biomedical Engineering'),
    ('B.Tech. Biomedical Engineering', 'Bachelor of Technology in Biomedical Engineering'),
    ('B.E. Environmental Engineering', 'Bachelor of Engineering in Environmental Engineering'),
    ('B.Tech. Environmental Engineering', 'Bachelor of Technology in Environmental Engineering'),
    ('B.E. Petroleum Engineering', 'Bachelor of Engineering in Petroleum Engineering'),
    ('B.Tech. Petroleum Engineering', 'Bachelor of Technology in Petroleum Engineering'),
    ('B.E. Mining Engineering', 'Bachelor of Engineering in Mining Engineering'),
    ('B.Tech. Mining Engineering', 'Bachelor of Technology in Mining Engineering'),
    ('B.E. Nuclear Engineering', 'Bachelor of Engineering in Nuclear Engineering'),
    ('B.Tech. Nuclear Engineering', 'Bachelor of Technology in Nuclear Engineering'),
    ('B.E. Software Engineering', 'Bachelor of Engineering in Software Engineering'),
    ('B.Tech. Software Engineering', 'Bachelor of Technology in Software Engineering'),
    ('B.E. Systems Engineering', 'Bachelor of Engineering in Systems Engineering'),
    ('B.Tech. Systems Engineering', 'Bachelor of Technology in Systems Engineering'),
    ('B.E. Telecommunication Engineering', 'Bachelor of Engineering in Telecommunication Engineering'),
    ('B.Tech. Telecommunication Engineering', 'Bachelor of Technology in Telecommunication Engineering'),
    ('B.E. Instrumentation Engineering', 'Bachelor of Engineering in Instrumentation Engineering'),
    ('B.Tech. Instrumentation Engineering', 'Bachelor of Technology in Instrumentation Engineering'),
    ('B.E. Power Engineering', 'Bachelor of Engineering in Power Engineering'),
    ('B.Tech. Power Engineering', 'Bachelor of Technology in Power Engineering'),
    ('B.E. Civil Engineering', 'Bachelor of Engineering in Civil Engineering'),
    ('B.Tech. Civil Engineering', 'Bachelor of Technology in Civil Engineering'),
    ('B.E. Electrical and Electronics Engineering', 'Bachelor of Engineering in Electrical and Electronics Engineering'),
    ('B.Tech. Electrical and Electronics Engineering', 'Bachelor of Technology in Electrical and Electronics Engineering'),
    ('B.E. Mechanical Engineering', 'Bachelor of Engineering in Mechanical Engineering'),
    ('B.Tech. Mechanical Engineering', 'Bachelor of Technology in Mechanical Engineering'),
    ('B.E. Industrial Engineering', 'Bachelor of Engineering in Industrial Engineering'),
    ('B.Tech. Industrial Engineering', 'Bachelor of Technology in Industrial Engineering'),
    ('B.E. Electronics and Instrumentation Engineering', 'Bachelor of Engineering in Electronics and Instrumentation Engineering'),
    ('B.Tech. Electronics and Instrumentation Engineering', 'Bachelor of Technology in Electronics and Instrumentation Engineering'),
    ('B.E. Chemical Engineering', 'Bachelor of Engineering in Chemical Engineering'),
    ('B.Tech. Chemical Engineering', 'Bachelor of Technology in Chemical Engineering'),
    ('B.E. Textile Engineering', 'Bachelor of Engineering in Textile Engineering'),
    ('B.Tech. Textile Engineering', 'Bachelor of Technology in Textile Engineering'),
    ('B.E. Agricultural Engineering', 'Bachelor of Engineering in Agricultural Engineering'),
    ('B.Tech. Agricultural Engineering', 'Bachelor of Technology in Agricultural Engineering'),
    ('B.E. Food Technology', 'Bachelor of Engineering in Food Technology'),
    ('B.Tech. Food Technology', 'Bachelor of Technology in Food Technology'),
    ('B.E. Marine Engineering', 'Bachelor of Engineering in Marine Engineering'),
    ('B.Tech. Marine Engineering', 'Bachelor of Technology in Marine Engineering'),
    ('B.E. Nuclear Engineering', 'Bachelor of Engineering in Nuclear Engineering'),
    ('B.Tech. Nuclear Engineering', 'Bachelor of Technology in Nuclear Engineering'),
    ('B.E. Telecommunication Engineering', 'Bachelor of Engineering in Telecommunication Engineering'),
    ('B.Tech. Telecommunication Engineering', 'Bachelor of Technology in Telecommunication Engineering'),
    ('B.E. Instrumentation Engineering', 'Bachelor of Engineering in Instrumentation Engineering'),
    ('B.Tech. Instrumentation Engineering', 'Bachelor of Technology in Instrumentation Engineering'),
    ('B.E. Power Engineering', 'Bachelor of Engineering in Power Engineering'),
    ('B.Tech. Power Engineering', 'Bachelor of Technology in Power Engineering')
    ]
    Program = models.CharField(max_length=100, choices=PROGRAM_CHOICES)
    Seats_Available = models.IntegerField(default=0)
    def save(self, *args, **kwargs):
        # Check if a duplicate record exists
        duplicate_records = SeatMatrix.objects.filter(
            College_Name=self.College_Name,
            Program=self.Program
        )
        if duplicate_records.exists():
            # Delete the duplicate records
            duplicate_records.delete()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.College_Name} - {self.Program}"
    '''
    class Meta:
        # Ensures that no duplicate combinations of College_ID and Program are allowed
        unique_together = ('College_ID', 'Program')
    '''

class Student(models.Model):
    def get_student_id():
        return generate_student_id()
    Allow_Login = models.IntegerField()
    Email_ID = models.EmailField()
    Password = models.CharField(max_length=50)
    Student_ID = models.IntegerField(primary_key=True, default=get_student_id)
    Name = models.CharField(max_length=100)
    DOB = models.DateField()
    Address = models.TextField()
    Fathers_Name = models.CharField(max_length=100)
    Mothers_Name = models.CharField(max_length=100)
    Aadhar_Card = models.FileField(upload_to='media/aadhar/', blank=True, null=True)
    School_Name12th = models.CharField(max_length=100)

    BOARD_CHOICES_12TH = [
        ('CBSE', 'Central Board of Secondary Education (CBSE)'),
        ('CISCE', 'Council for the Indian School Certificate Examinations (CISCE)'),
        ('NIOS', 'National Institute of Open Schooling (NIOS)'),
        ('MSBSHSE', 'Maharashtra State Board of Secondary and Higher Secondary Education (MSBSHSE)'),
        ('TNBHSE', 'Tamil Nadu State Board of Higher Secondary Education (TNBHSE)'),
        ('UPMSP', 'Uttar Pradesh Madhyamik Shiksha Parishad (UPMSP)'),
        # Add other state boards as needed
    ]
    Board_12th = models.CharField(max_length=60, choices=BOARD_CHOICES_12TH)

    Certificate_12th = models.FileField(upload_to='media/certificates/12th/', blank=True, null=True)
    Maths_Marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MaxValueValidator(100), validate_marks])
    Physics_Marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MaxValueValidator(100), validate_marks])
    Chemistry_Marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MaxValueValidator(100), validate_marks])
    Cut_Off_Marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MaxValueValidator(200), validate_cutoff])

    BOARD_CHOICES_10TH = [
        ('CBSE', 'Central Board of Secondary Education (CBSE)'),
        ('CISCE', 'Council for the Indian School Certificate Examinations (CISCE)'),
        ('NIOS', 'National Institute of Open Schooling (NIOS)'),
        ('MSBSHSE', 'Maharashtra State Board of Secondary and Higher Secondary Education (MSBSHSE)'),
        ('TNBSE', 'Tamil Nadu State Board of Secondary Education (TNBSE)'),
        ('UPMSP', 'Uttar Pradesh Madhyamik Shiksha Parishad (UPMSP)'),
        # Add other state boards as needed
    ]
    School_Name10th = models.CharField(max_length=100)
    Board_10th = models.CharField(max_length=50, choices=BOARD_CHOICES_10TH)

    Certificate_10th = models.FileField(upload_to='media/certificates/10th/', blank=True, null=True)
    TC = models.FileField(upload_to='tc/', blank=True, null=True)
    Passport_Photo = models.ImageField(upload_to='media/photos/', blank=True, null=True)
    tenth_year = models.PositiveIntegerField()  # Year of passing for 10th
    twelfth_year = models.PositiveIntegerField()
    Rank = models.IntegerField(default=0, blank=True, null=True)
    Allotted_College = models.CharField(max_length=100, default='TBD', blank=True)
    Allotted_Course = models.CharField(max_length=100, default='TBD', blank=True)
    Course_ID = models.IntegerField()
    Log_Stat = models.IntegerField()
    Allot_Stat = models.IntegerField(default=1)
    Choice_Number = models.IntegerField(default=0)
    def __str__(self):
        return self.Name
        
class RankList(models.Model):
    Rank = models.IntegerField(unique=True, validators=[MinValueValidator(1)])
    ID = models.IntegerField(unique=True)
    Name = models.CharField(max_length=100)
    DOB = models.DateField()
    Fathers_Name = models.CharField(max_length=100)
    Maths_Marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MaxValueValidator(100), validate_marks])
    Physics_Marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MaxValueValidator(100), validate_marks])
    Chemistry_Marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MaxValueValidator(100), validate_marks])
    Cut_Off_Marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MaxValueValidator(200), validate_cutoff])
    def __str__(self):
        return f"{self.Rank} - {self.Name}"
'''
class RankList(models.Model):
    Student_Rank = models.IntegerField(unique=True, validators=[MinValueValidator(1)])
    Student_ID = models.IntegerField(unique=True)
    Student_Name = models.CharField(max_length=100)
    Student_DOB = models.DateField()
    Student_Mark = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f"{self.Student_Rank} - {self.Student_Name}"

    def save(self, *args, **kwargs):
        # Generate a random number for tie-breaking
        random_number = random.randint(0, 1000)
        
        # Get the current highest rank
        highest_rank = RankList.objects.aggregate(max_rank=models.Max('Student_Rank'))['max_rank']
        
        # Assign rank based on sorting criteria
        rank_queryset = (
            RankList.objects.annotate(
                random_number=Coalesce(F('id') % 1000, 0)  # Adjust the modulo value as needed
            )
            .order_by(
                '-Student_Mark',  # Descending order of marks
                '-Student_DOB',  # Elder students first based on DOB
                'Student_Name',  # Alphabetical order of names
                '-random_number',  # Random number, higher first
            )
        )
        
        # Calculate new rank for the current record
        new_rank = 1
        for record in rank_queryset:
            if record.Student_Mark > self.Student_Mark:
                new_rank += 1
            elif record.Student_Mark == self.Student_Mark:
                # Compare other criteria if marks are equal
                if record.Student_DOB < self.Student_DOB:
                    new_rank += 1
                elif record.Student_DOB == self.Student_DOB:
                    # Compare names
                    if record.Student_Name > self.Student_Name:
                        new_rank += 1
                    # Add more comparison criteria if needed
                else:
                    break
            else:
                break
        
        # Adjust rank for new record
        if highest_rank is not None and new_rank > highest_rank:
            new_rank = highest_rank + 1
        
        self.Student_Rank = new_rank
        super(RankList, self).save(*args, **kwargs)
 '''       
class ChoiceListTable(models.Model):
    Student_Rank = models.IntegerField()
    Student_ID = models.IntegerField()
    College = models.CharField(max_length=100)  # Change to CharField
    Program = models.CharField(max_length=100, choices=SeatMatrix.PROGRAM_CHOICES)
    Choice_Number = models.IntegerField()
    College_ID = models.IntegerField()  # Default value
    
    def __str__(self):
        return f"Rank: {self.Student_Rank}, Student: {self.Student_ID}, Choice: {self.Choice_Number}, College: {self.College}, Program: {self.Program}"
    '''
    def save(self, *args, **kwargs):
        if not self.pk:
            # Get the maximum choice_number for the current user's choices
            max_choice_number = ChoiceListTable.objects.filter(Student_ID=self.Student_ID, College=self.College, Program=self.Program).aggregate(max_choice=models.Max('Choice_Number'))['max_choice']
            # Increment choice_number for the new choice
            self.Choice_Number = max_choice_number + 1 if max_choice_number is not None else 1
        super(ChoiceListTable, self).save(*args, **kwargs)
    '''

class Set(models.Model):
    Allow_Register = models.IntegerField()
    Allow_CF = models.IntegerField()
    Allow_SM = models.IntegerField()
    Allow_Create_CRL = models.IntegerField()
    Allow_CRL = models.IntegerField()
    Allot_Program = models.IntegerField()
    ReAllot = models.IntegerField()
    Finish = models.IntegerField()
    DelRecords = models.IntegerField()
    Show_Allotted = models.IntegerField()

class Aadhar(models.Model):
    QR_Number = models.IntegerField()
    Aadhar_Number = models.IntegerField()
    Name = models.CharField(max_length=100)
    DOB = models.DateField(default="2024-01-01")
    Fathers_Name = models.CharField(max_length=100)
    Mothers_Name = models.CharField(max_length=100)
    Address = models.TextField()
    
    
class MarkSheets(models.Model):
    QR_Number = models.IntegerField()
    Aadhar_Number = models.IntegerField()
    Maths = models.IntegerField()
    Physics = models.IntegerField()
    Chemistry = models.IntegerField()
    Cutoff = models.IntegerField()
    Name = models.CharField(max_length=100)
    School = models.TextField()
    Board = models.CharField(max_length=50)
    Year = models.IntegerField()

class Serv_Files(models.Model):
    manual = models.FileField(upload_to='media/serverfiles/', blank=True, null=True)

class image(models.Model):
    flag = models.IntegerField()
    img=models.ImageField(upload_to='media/photos/')
    desc = models.TextField()
    
class Previous(models.Model):
    Rank = models.IntegerField()
    CutOff = models.IntegerField()
    College = models.TextField()
    Course = models.TextField()
