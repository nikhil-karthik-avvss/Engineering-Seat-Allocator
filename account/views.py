from django.shortcuts import render, get_object_or_404, redirect
from pages.models import Student, SeatMatrix, Set, RankList, Institute, ChoiceListTable, image, Previous
from datetime import date
import json
from decimal import Decimal
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_POST

def home(request):
    '''uname = request.POST['uname']
    pasw = request.POST['pasw']'''
    my_date = date.today()
    uname = request.session.get('uname')
    def decimal_to_str(decimal_obj):
        return str(decimal_obj) if isinstance(decimal_obj, Decimal) else decimal_obj
    student = get_object_or_404(Student, Student_ID=uname)
    request.session['uname'] = student.Student_ID
    request.session['email'] = student.Email_ID
    request.session['pasw'] = student.Password
    request.session['name'] = student.Name
    request.session['dob'] = student.DOB.isoformat()
    request.session['address'] = student.Address
    request.session['fname'] = student.Fathers_Name
    request.session['mname'] = student.Mothers_Name
    request.session['aadhar'] = student.Aadhar_Card.url
    request.session['sch12'] = student.School_Name12th
    request.session['brd12'] = student.Board_12th
    request.session['cer12'] = student.Certificate_12th.url
    request.session['maths'] = decimal_to_str(student.Maths_Marks)
    request.session['physics'] = decimal_to_str(student.Physics_Marks)
    request.session['chemistry'] = decimal_to_str(student.Chemistry_Marks)
    request.session['cutoff'] = decimal_to_str(student.Cut_Off_Marks)
    request.session['sch10'] = student.School_Name10th
    request.session['brd10'] = student.Board_10th
    request.session['cer10'] = student.Certificate_10th.url
    request.session['tc'] = student.TC.url
    request.session['photo'] = student.Passport_Photo.url
    request.session['year10'] = decimal_to_str(student.tenth_year)
    request.session['year12'] = decimal_to_str(student.twelfth_year)
    request.session['rank'] = student.Rank
    request.session['college'] = student.Allotted_College
    request.session['seat'] = student.Allotted_Course
    setv = Set.objects.first()
    '''
    data = {
        'registration': 'completed',
        'commonRankList': 'in-progress',
        'seatMatrix': 'not-started',
        'choiceFilling': 'not-started',
        'seatAllotment': 'not-started',
        'admission': 'not-started'
    }
    '''
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
    return render(request,'home.html',{'step_status': data})

def user_profile(request):
    return render(request,'student_profile.html')

def view_sm(request):
    setv = Set.objects.first()
    print(setv.Allow_SM)
    if(setv.Allow_SM == 0):
        return render(request,'deny_sm_stud.html')
    all_records = SeatMatrix.objects.all()
    return render(request,'view_seat_matric_stud.html',{'colleges':all_records})

def view_crl(request):
    setv = Set.objects.first()
    if(setv.Allow_CRL==0):
        return render(request,'ranklist_deny.html')
    else:
        all_records = RankList.objects.all()
        return render(request,'ranklist_view.html',{'students':all_records})

def choice(request):
    rank = request.session.get('rank')
    sid = request.session.get('uname')
    print(request.session.items())
    if(request.method == 'POST'):
        selected_choices = {}
        num = 0  # Initialize the choice number counter

# Retrieve the session user ID
        sid = request.session.get('uname')
        print(f"Session User ID: {sid}")

# Iterate over the POST items
        for key, value in request.POST.items():
            if key.startswith('college_id_'):
                num += 1  # Increment choice number for each valid choice
                choice_number = key.split('_')[-1]
                college_name_key = f'college_name_{choice_number}'
                program_key = f'program_{choice_number}'

        # Check if the related fields exist
                if college_name_key in request.POST and program_key in request.POST:
                    selected_choices[num] = {
                        'college_id': value,
                        'college_name': request.POST.get(college_name_key),
                        'program': request.POST.get(program_key)
                    }
                    print(f"Processed choice {num}: {selected_choices[num]}")
                else:
                    print(f"Missing fields for choice number {choice_number}")

# Debug output for selected choices
        print(f"Selected Choices: {selected_choices}")

# Create and save ChoiceListTable objects
        for cn, choice in selected_choices.items():
            choice_obj = ChoiceListTable(
            Student_Rank=rank,
            Student_ID=int(sid),
            College=choice['college_name'],
            Program=choice['program'],
            Choice_Number=cn,  # Use the incremented choice number
            College_ID=int(choice['college_id'])
        )
            choice_obj.save()
            print(f"Saved choice {cn} to the database")
            #print(selected_choices.keys())
            
        choice_obj = ChoiceListTable.objects.filter(Student_ID=sid)
        return render(request,'choice_show.html',{'choices':choice_obj})
    all_records = SeatMatrix.objects.all()
    clg_names = SeatMatrix.objects.values('College_ID').distinct()
    print(clg_names)
    for rec in all_records:
        print(rec.College_ID)
    choice_obj = ChoiceListTable.objects.filter(Student_ID=sid)
    if(choice_obj):
        return render(request,'choice_show.html',{'choices':choice_obj})
    else:
        setv = Set.objects.first()
        if(setv.Allow_CF==1):
            return render(request,'choice_fill.html',{'colleges':all_records,'clg_names':clg_names})
        else:
            return render(request,'deny_cf.html')

def get_college_name(request):
    college_id = request.GET.get('college_id')
    college = Institute.objects.get(College_ID=college_id)
    return JsonResponse({'college_name': college.College_Name})

def get_programs(request):
    college_id = request.GET.get('college_id')
    programs = SeatMatrix.objects.filter(College_ID=college_id)
    program_list = list(programs.values('College_ID', 'Program'))
    print(program_list)
    return JsonResponse({'programs': program_list})

def logout_stud(request):
    uname = request.session.get('uname')
    print(uname)
    student = Student.objects.filter(Student_ID=uname).first()
    student.Log_Stat=0
    student.save()
    request.session.flush()
    auth_logout(request)
    return render(request,'logout.html')

def view_allotment_stud(request):
    setv = Set.objects.first()
    if setv.Show_Allotted == 1:
        uname = request.session.get('uname')
        stud = Student.objects.filter(Student_ID=uname).first()
        setv = Set.objects.first()
        print(setv.ReAllot)
        return render(request, 'show_allotment.html', {'stud': stud,'setv':setv})
    else:
        return render(request, 'deny_allotment.html')

@require_POST
def update_allotment(request):
    uname = request.session.get('uname')
    stud = Student.objects.filter(Student_ID=uname).first()
    print('Hello')
    '''
    if not stud or stud.Allot_Stat != 0:  # Assuming 0 means the allotment is accepted
        return redirect('view_allotment_stud')
    '''
    action = request.POST.get('action', '')
    if action:
        allot_stat = {
            'accept': 2,
            'accept_upward': 3,
            'decline': -1,
            'decline_upward': -2,
        }.get(action, 1)  # Default to 1 if action is unrecognized

        stud.Allot_Stat = allot_stat
        print(stud.Allot_Stat,allot_stat)
        stud.save()

    return redirect('home')
    
def view_manual(request):
    imgs = image.objects.filter(flag=0)
    print(imgs)
    return render(request,'stud_manual.html',{'images':imgs})

def college_list(request):
    colleges = Institute.objects.all().order_by('College_ID')
    #stud = Student.objects.all().order_by('Rank')
    return render(request, 'college_list.html', {'colleges': colleges})

def college_detail(request, college_id):
    college = get_object_or_404(Institute, pk=college_id)
    seat_matrix = SeatMatrix.objects.filter(College_ID=college_id)
    return render(request, 'college_detail.html', {'college': college, 'seat_matrix': seat_matrix})

def prev_allotment(request):
    previous=Previous.objects.all().exclude(Rank=0).order_by('Rank')
    return render(request,'prev_allotment_stud.html',{'students':previous})
    pass

def curr_allotment(request):
    setv = Set.objects.first()
    if(setv.Show_Allotted==1):
        stud = Student.objects.exclude(Rank=0).order_by('Rank')
        return render(request, 'curr_allotment_stud.html',{'students':stud})
    else:
        return render(request, 'deny_allotment.html')



