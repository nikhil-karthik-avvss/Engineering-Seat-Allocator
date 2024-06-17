from django.shortcuts import render, redirect
from pages.models import Institute, SeatMatrix, Student, Set, RankList, image
from django.db.models import Count
from django.db.models import F
from django.db.models.functions import Coalesce
import random
from django.contrib.auth import logout as auth_logout

# Create your views here.
def institute_home(request):
    uname = request.session.get('uname')
    pasw = request.session.get('pasw')
    institute = Institute.objects.filter(College_ID=uname, Password=pasw).first()
    if institute is not None:
        request.session['c_id'] = institute.College_ID
        request.session['clg_name'] = institute.College_Name
        request.session['adr'] = institute.Address
        request.session['admin'] = institute.Administrator_Name
        request.session['email'] = institute.Email_ID
        request.session['contact'] = institute.Contact_Number
        #request.session['certificate'] = institute.Certificate.url
        request.session['flag'] = institute.Flag
        setv = Set.objects.first()
        data = {
        'registration': 'not-started',
        'commonRankList': 'not-started',
        'seatMatrix': 'not-started',
        'choiceFilling': 'not-started',
        'seatAllotment': 'not-started',
        'admission': 'not-started'
        }
        if(setv.Allow_Register==1):
            data['registration']='in-progress'
        else:
            data['registration']='not-started'
        if(setv.Allow_CRL==1):
            data['registration']='completed'
            data['commonRankList']='completed'
        if(setv.Allow_SM==1):
            data['registration']='completed'
            data['seatMatrix']='completed'
        if(setv.Allow_CF==1):
            data['registration']='completed'
            data['seatMatrix']='completed'
            data['choiceFilling']='in-progress'
        if(setv.Show_Allotted==1):
            data['registration']='completed'
            data['choiceFilling']='completed'
            data['seatAllotment']='completed'
            data['admission']='completed'
            request.session['step_status'] = data
        return render(request, 'institute_home.html',{'step_status': data})
    else:
        # Handle case where no institute is found
        # For example, redirect to a login page with an error message
        return redirect("index")
def profile(request):
    uname = request.session.get('uname')
    pasw = request.session.get('pasw')
    institute = Institute.objects.filter(College_ID=uname, Password=pasw).first()
    
    if institute:
        request.session['College_ID'] = institute.College_ID
        request.session['College_Image_URL'] = institute.College_Image_URL
        request.session['College_Name'] = institute.College_Name
        request.session['Address'] = institute.Address
        request.session['Administrator_Name'] = institute.Administrator_Name
        request.session['Contact_Number'] = institute.Contact_Number
        request.session['Tution_Fee'] = institute.Tution_Fee
        request.session['Hostel_Fee_Min'] = institute.Hostel_Fee_min
        request.session['Hostel_Fee_Max'] = institute.Hostel_Fee_max
        request.session['Bus_Fee'] = institute.Bus_Fee
        request.session['Mand_Bus'] = institute.Mand_Bus
        request.session['Mess_Inc'] = institute.Mess_Inc
        request.session['Web'] = institute.Web

    # Render the profile template
    return render(request, 'institute_profile.html')


def seatmatrix_success(request):
    c_id = request.session.get('c_id')
    sm = SeatMatrix.objects.filter(College_ID=c_id)
    return render(request,"seatmatrix_success.html",{'all_courses':sm})

def seatmatrix_input(request):
    if(request.method == "POST"):
        c_id = request.session.get('c_id')
        clg_name = request.session.get('clg_name')
        selected_courses = request.POST.getlist('course')  # Get selected course names (if multiple selections are allowed)
        seat_intakes = request.POST.getlist('seat_intake')
        for course, intake in zip(selected_courses, seat_intakes):
            sm = SeatMatrix(College_ID=c_id, College_Name=clg_name, Program=course,Seats_Available=intake)
            sm.save()
        
        duplicate_ids = (SeatMatrix.objects.values('College_Name', 'Program').annotate(min_id=Count('College_ID')).filter(min_id__gt=1).values_list('College_ID', flat=True))
        SeatMatrix.objects.filter(id__in=duplicate_ids).delete()
        sm = SeatMatrix.objects.filter(College_ID=c_id)
        return render(request,"seatmatrix_success.html",{'all_courses':sm})
        
    c_id = request.session.get('c_id')
    sm = SeatMatrix.objects.filter(College_ID=c_id)
    if(sm):
        return render(request,"seatmatrix_success.html",{'all_courses':sm})
    courses = [
    'B.E. Computer Science and Engineering',
    'B.Tech. Computer Science and Engineering',
    'B.E. Information Technology',
    'B.Tech. Information Technology',
    'B.E. Artificial Intelligence and Machine Learning',
    'B.Tech. Artificial Intelligence and Machine Learning',
    'B.E. Data Science and Analytics',
    'B.Tech. Data Science and Analytics',
    'B.E. Cybersecurity',
    'B.Tech. Cybersecurity',
    'B.E. Electronics and Communication Engineering',
    'B.Tech. Electronics and Communication Engineering',
    'B.E. Robotics and Automation',
    'B.Tech. Robotics and Automation',
    'B.E. Biotechnology',
    'B.Tech. Biotechnology',
    'B.E. Nanotechnology',
    'B.Tech. Nanotechnology',
    'B.E. Renewable Energy Engineering',
    'B.Tech. Renewable Energy Engineering',
    'B.E. Aerospace Engineering',
    'B.Tech. Aerospace Engineering',
    'B.E. Gaming Technology',
    'B.Tech. Gaming Technology',
    'B.E. Mobile Application Development',
    'B.Tech. Mobile Application Development',
    'B.E. Augmented Reality and Virtual Reality',
    'B.Tech. Augmented Reality and Virtual Reality',
    'B.E. Internet of Things (IoT)',
    'B.Tech. Internet of Things (IoT)',
    'B.E. Biomedical Engineering',
    'B.Tech. Biomedical Engineering',
    'B.E. Environmental Engineering',
    'B.Tech. Environmental Engineering',
    'B.E. Petroleum Engineering',
    'B.Tech. Petroleum Engineering',
    'B.E. Mining Engineering',
    'B.Tech. Mining Engineering',
    'B.E. Nuclear Engineering',
    'B.Tech. Nuclear Engineering',
    'B.E. Software Engineering',
    'B.Tech. Software Engineering',
    'B.E. Systems Engineering',
    'B.Tech. Systems Engineering',
    'B.E. Telecommunication Engineering',
    'B.Tech. Telecommunication Engineering',
    'B.E. Instrumentation Engineering',
    'B.Tech. Instrumentation Engineering',
    'B.E. Power Engineering',
    'B.Tech. Power Engineering',
    'B.E. Civil Engineering',
    'B.Tech. Civil Engineering',
    'B.E. Electrical and Electronics Engineering',
    'B.Tech. Electrical and Electronics Engineering',
    'B.E. Mechanical Engineering',
    'B.Tech. Mechanical Engineering',
    'B.E. Industrial Engineering',
    'B.Tech. Industrial Engineering',
    'B.E. Electronics and Instrumentation Engineering',
    'B.Tech. Electronics and Instrumentation Engineering',
    'B.E. Chemical Engineering',
    'B.Tech. Chemical Engineering',
    'B.E. Textile Engineering',
    'B.Tech. Textile Engineering',
    'B.E. Agricultural Engineering',
    'B.Tech. Agricultural Engineering',
    'B.E. Food Technology',
    'B.Tech. Food Technology',
    'B.E. Marine Engineering',
    'B.Tech. Marine Engineering',
    'B.E. Nuclear Engineering',
    'B.Tech. Nuclear Engineering',
    'B.E. Telecommunication Engineering',
    'B.Tech. Telecommunication Engineering',
    'B.E. Instrumentation Engineering',
    'B.Tech. Instrumentation Engineering',
    'B.E. Power Engineering',
    'B.Tech. Power Engineering'
]

    return render(request,"seat_matrix_get.html",{'courses':courses})

def view_crl_inst(request):
    setv = Set.objects.first()
    if(setv.Allow_CRL==0):
        return render(request,'ranklist_deny_inst.html')
    else:
        all_records = RankList.objects.all()
        return render(request,'ranklist_view_inst.html',{'students':all_records})

def logout(request):
    uname = request.session.get('uname')
    institute = Institute.objects.filter(College_ID=uname).first()
    institute.Log_Stat=0
    institute.save()
    request.session.flush()
    auth_logout(request)
    return render(request,'logout.html')

def view_allotment_inst(request):
    
    setv = Set.objects.first()
    if(setv.Show_Allotted==1):
        clg_name = request.session.get('clg_name')
        students = Student.objects.filter(Allotted_College=clg_name)
        return render(request,'show_allotment_inst.html',{'students':students})
    else:
        return render(request,'deny_allotment_inst.html')

def download_manual(request):
    imgs = image.objects.filter(flag=1)
    return render(request,'inst_manual.html',{'images':imgs})
