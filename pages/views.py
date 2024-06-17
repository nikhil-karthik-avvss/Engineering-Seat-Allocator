from django.shortcuts import render, redirect
from django.http import HttpResponse
import random
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .models import Student, Institute, RankList, Set, Aadhar, MarkSheets, Serv_Files
from django.urls import reverse
import cv2
from pyzbar.pyzbar import decode
import os
import numpy as np
from PIL import Image


def decode_qr_code(image_data):
    # Convert image data to OpenCV format
    img = cv2.imdecode(np.frombuffer(image_data.read(), np.uint8), cv2.IMREAD_UNCHANGED)

    # Decode the QR code
    decoded_objects = decode(img)

    # Check if there are any QR codes in the image
    if not decoded_objects:
        return None

    # Extract data from decoded QR codes
    qr_data_list = []
    for obj in decoded_objects:
        qr_data = {
            "type": obj.type,
            "data": obj.data.decode('utf-8'),
            "position": obj.rect
        }
        data = obj.data.decode('utf-8')
        qr_data_list.append(qr_data)

    return int(data)
# Create your views here.
def index(request):
    return render(request,'index.html')

def emailenter(request):
    setv = Set.objects.first()
    if(setv.Allow_Register==0):
        return render(request,'blocked_register.html')
    return render(request,'emailenter.html')

def email_verify(request):
    otp = random.randint(100000,999999)
    sender_email = 'esa.py.project@gmail.com'  # Update with your Microsoft email address
    receiver_email = request.POST['email']
    subject = 'OTP for Engineering Seat Allocation (Student Project)'
    body = f"""
Greetings,

We are delighted to inform you that we have received your request to register on our website. As part of the registration process, we have generated a One-Time Password (OTP) exclusively for you. This OTP is a crucial step in verifying your email address and ensuring the security of your account.

Please find your unique OTP below:
{otp}

Kindly enter this OTP on our website to complete the verification process and finalize your registration. Should you have any questions or need further assistance, please don't hesitate to reach out to our support team.

Thank you for choosing us, and we look forward to welcoming you to our platform!

Best regards,
Engineering Seat Allocation Software (Student Project)"""

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    username = 'esa.py.project@gmail.com'  # Update with your Microsoft email address
    password = 'feyd fbbf mfaf ijgw' # Update with your email account password

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

# Add body to email
    message.attach(MIMEText(body, 'plain'))

    # Create a SMTP session
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Enable TLS encryption
    server.login(username, password)  # Login to email server

    # Send email
    server.sendmail(sender_email, receiver_email, message.as_string())
    print('Email sent successfully!')
    receiver_email = request.POST['email']
    ids = Student.objects.values_list('Email_ID',flat=True)
    for i in ids:
        if(i==receiver_email):
            return render(request,'email_exists.html',{'email_id':receiver_email,'contact_email':'esa.py.project@gmail.com'})
    return render(request,'email_verify.html',{'otpv':otp,'email':receiver_email})

def verify_otp(request):
    otpe = int(request.POST['otp'])
    otpv = int(request.POST.get('otpv'))
    email = request.POST.get('email')
    if (otpe == otpv):
        board_choices = ['CBSE', 'CISCE','NIOS','MSBSHSE','TNBHSE','UPMSP']
        context = {'board_choices': board_choices, 'email':email}
        return render(request,'register.html',context)
    else:
        return render(request,"email_verification_failure.html")

def register_db(request):
    #if(request.method == 'POST'):
    name = request.POST['name']
    email = request.POST.get('email')
    password = request.POST['password']
    #maths = request.POST['maths']
    #physics = request.POST['physics']
    #chemistry = request.POST['chemistry']
    #cutoff = request.POST['cutoff']
    school12th = request.POST['twelfth_school']
    board12th = request.POST['twelfth_board']
    certificate12th = request.FILES.get('twelfth_certificate')
    year12th = request.POST['twelfth_year']
    school10th = request.POST['tenth_school']
    board10th = request.POST['tenth_board']
    certificate10th = request.FILES.get('tenth_certificate')
    year10th = request.POST['tenth_year']
    photo = request.FILES.get('photo')
    aadhar = request.FILES.get('aadhar')
    dob = request.POST['dob']
    address = request.POST['address']
    father_name = request.POST['father_name']
    mother_name = request.POST['mother_name']
    tc = request.FILES.get('tc')
    QR12th = decode_qr_code(certificate12th)
    QR_Aadhar = decode_qr_code(aadhar)
    adr_obj = Aadhar.objects.filter(QR_Number=QR_Aadhar).first()
    mrk_obj = MarkSheets.objects.filter(QR_Number=QR12th).first()
    if(adr_obj and mrk_obj):
        pass
    else:
        return render(request,'invalid_docs.html')
    print(QR12th,QR_Aadhar)
    #adr_obj.DOB==dob and
    print(adr_obj.DOB==dob and adr_obj.Aadhar_Number==mrk_obj.Aadhar_Number and name.lower()==adr_obj.Name.lower() and  name.lower()==mrk_obj.Name.lower() and year12th==mrk_obj.Year and adr_obj.Fathers_Name.lower()==father_name.lower() and adr_obj.Mothers_Name.lower()==mother_name.lower())
    
    print("adr_obj.DOB:", type(adr_obj.DOB))
    print("dob:", type(dob))
    dob = datetime.strptime(dob, '%Y-%m-%d').date()
    print(adr_obj.DOB==dob)
    print(adr_obj.Aadhar_Number==mrk_obj.Aadhar_Number)
    print(name.lower()==adr_obj.Name.lower())
    print(name.lower()==mrk_obj.Name.lower())
    print(int(year12th)==mrk_obj.Year)
    print(adr_obj.Fathers_Name.lower()==father_name.lower())
    print(adr_obj.Mothers_Name.lower()==mother_name.lower())
    
    if(adr_obj and mrk_obj):
        pass
    else:
        return render(request,'invalid_docs.html')
    if(adr_obj.DOB==dob and adr_obj.Aadhar_Number==mrk_obj.Aadhar_Number and name.lower()==adr_obj.Name.lower() and  name.lower()==mrk_obj.Name.lower() and int(year12th)==mrk_obj.Year and adr_obj.Fathers_Name.lower()==father_name.lower() and adr_obj.Mothers_Name.lower()==mother_name.lower()):
        
        flag=1
        print("hello",flag)
        maths = mrk_obj.Maths
        physics = mrk_obj.Physics
        chemistry = mrk_obj.Chemistry
        cutoff = mrk_obj.Cutoff
    else:
        maths=physics=chemistry=cutoff=0
        flag=0  
    print(adr_obj.DOB,dob)
    print(adr_obj.Aadhar_Number,mrk_obj.Aadhar_Number,name.lower(),adr_obj.Name.lower(),name.lower(),mrk_obj.Name.lower(),year12th,mrk_obj.Year, adr_obj.Fathers_Name.lower(),father_name.lower(), adr_obj.Mothers_Name.lower(),mother_name.lower())
    stud_user = Student(Allow_Login=flag,Email_ID = email, Password = password, Name = name, DOB = dob, Address = address, Fathers_Name = father_name, Mothers_Name = mother_name, Aadhar_Card = aadhar, School_Name12th = school12th, Board_12th = board12th, Certificate_12th = certificate12th, Maths_Marks = maths, Physics_Marks = physics, Chemistry_Marks = chemistry, Cut_Off_Marks = cutoff, School_Name10th = school10th, Board_10th = board10th, Certificate_10th = certificate10th, TC = tc, Passport_Photo = photo, tenth_year = year10th, twelfth_year = year12th,Log_Stat=0)
    stud_user.save()
    stud = Student.objects.filter(Email_ID=email).first()
    #rn = RankList(ID=stud.Student_ID,Name=name,DOB=dob,Fathers_Name=father_name,Maths_Marks=maths,Physics_Marks=physics,Chemistry_Marks=chemistry,Cut_Off_Marks=cutoff,Rank=0)
    #rn.save()
    return render(request,'success_create.html',{'user_id':stud.Student_ID})
    
def student_login(request):
    #setv = Set.objects.first()
    #if(setv.Allow_)
    if request.method == 'GET':
        return render(request, 'student_login.html')
    elif request.method == 'POST':
        uname = request.POST.get('username')
        pasw = request.POST.get('password')
        # Check if username and password match a student record
        student = Student.objects.filter(Student_ID=uname, Password=pasw).first()
        if(student==None):
            return render(request,'blocked_login.html')
        #if(student.Log_Stat==1):
        #    return render(request,'acc_logdin.html')
        student.Log_Stat=1
        student.save()
        if(student.Allow_Login==0):
            return render(request,'blocked_login.html')
        if (student):
            # Authentication successful, redirect to homepage or any other page
            request.session['uname'] = uname
            request.session['pasw'] = pasw
            return redirect(reverse('home'))  # Replace 'homepage' with your actual URL name
        else:
            # Authentication failed, you can render the login page with an error message
            return render(request, 'auth_fail.html', {'error': 'Istudent_login.htmlials'})
'''
def student_login(request):
    if(request.method == 'GET'):
        return render(request,'student_login.html')
    else:
        uname = request.POST['username']
        pasw = request.POST['password']
        all_records = Student.objects.all().values('Student_ID', 'Password')
        for acc in all_records:
            if(acc['Student_ID']==uname and acc['Password']==pasw):
                return redirect(request,"homepage")
        pass
'''
def institute_login(request):
    if(request.method == 'POST'):
        uname = int(request.POST['username'])
        pasw = request.POST['password']
        institute = Institute.objects.filter(College_ID=uname, Password=pasw).first()
        if(institute):
            request.session['uname'] = uname
            request.session['pasw'] = pasw
            if(institute.Log_Stat==1):
                return render(request,'acc_logdin.html')
            institute.Log_Stat=1
            institute.save()
            return redirect(reverse('institute_home'))
        else:
            return render(request,'auth_fail_inst.html')
    else:
        return render(request,'institute_login.html')
    
def pass_enter(request):
    if(request.method == "GET"):
        return render(request, 'pass_enter.html')
    otp = random.randint(100000,999999)
    sender_email = 'esa.py.project@gmail.com'  # Update with your Microsoft email address
    receiver_email = request.POST['email']
    request.session['emaile'] = receiver_email
    email_ids = Student.objects.values('Email_ID')
    print(email_ids)
    for em in email_ids:
        if(em['Email_ID']==receiver_email):
            break
    else:
        return render(request,'email_not_found.html')
    subject = 'OTP for Engineering Seat Allocation (Student Project)'
    body = f'''
Dear user,

We have received a request to reset the password associated with your account. To proceed with the password reset process, please use the following One-Time Password (OTP):

OTP: {otp}

Please enter this OTP on the password reset page to create a new password for your account. If you did not request this password reset, please disregard this message and ensure your account security.

Thank you,
Engineering Seat Allocation Student Project Team'''

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    username = 'esa.py.project@gmail.com'  # Update with your Microsoft email address
    password = 'feyd fbbf mfaf ijgw' # Update with your email account password

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

# Add body to email
    message.attach(MIMEText(body, 'plain'))

    # Create a SMTP session
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Enable TLS encryption
    server.login(username, password)  # Login to email server

    # Send email
    server.sendmail(sender_email, receiver_email, message.as_string())
    print('Email sent successfully!')
    request.session['otpg'] = otp
    return render(request,'otp_enter.html')

def reset_password(request):
    otpe = request.POST['otp']
    pasw = request.POST['password']
    otpg = request.session.get('otpg')
    emaile = request.session.get('emaile')
    print(otpe,otpg)
    if(int(otpe) == int(otpg)):
        obj = Student.objects.get(Email_ID = emaile)
        obj.Password = pasw
        obj.save()
        return render(request,'password_successful.html')
    else:
        return render(request,'otp_fail.html')

def download_manual(request):
    return render(request,'view_manual.html')


    
