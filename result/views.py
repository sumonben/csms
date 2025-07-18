from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Marks,Exam,Result,HighestMarks,TestMarks
from student.models import Student,Group,Choice,Subject
from .forms import SeachResultForm,CreateResultForm,DeletResultForm,CreatePositionForm,HighestMarksForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Max,Window
# Create your views here.

def searchResult(request):
    context={}
    flag1=0
    flag2=0
    
    if request.method=='POST':
        totalgpa=0
        totalgpa1=0
        exam=Exam.objects.filter(id=request.POST.get('exam')).first()
        if exam.type == '2':
            marks=TestMarks.objects.filter(class_roll=request.POST.get('roll').strip(),exam=exam).order_by('subject')
        else:
            marks=Marks.objects.filter(class_roll=request.POST.get('roll').strip(),exam=exam).order_by('subject')
        highest_marks=HighestMarks.objects.filter(exam=exam)

        result=Result.objects.filter(class_roll=request.POST.get('roll').strip(),exam=exam).first()
        student=Student.objects.filter(class_roll=request.POST.get('roll').strip()).first()
        print(student)
        subject_choice=Choice.objects.filter(class_roll=request.POST.get('roll').strip()).first()

        if subject_choice and student and marks and exam:
            choice_list=[subject_choice.subject1,subject_choice.subject2,subject_choice.subject3,subject_choice.subject4,subject_choice.subject5,subject_choice.subject6,subject_choice.fourth_subject]
            print(choice_list)

        else:
            context['notfound']="Result not found!!re=Enter Right Information or Contact exam control room"
            form=SeachResultForm()
            context['form']=form
            return render(request, 'result/search_result.html', context=context)
        context['marks']=marks
        context['highest_marks']=highest_marks
        context['result']=result
        context['student']=student
        context['exam']=exam
        context['choice_list']=choice_list
        context['subject_choice']=subject_choice

        
        
        if exam.type == '2':
            return render(request, 'result/show_result_test.html', context=context)
        else:
            return render(request, 'result/show_result_copy.html', context=context)
    form=SeachResultForm(current_user=request.user)
    context['form']=form
    return render(request, 'result/search_result.html', context=context)

@login_required
def OptionCreateResult(request):
    context={}
    create_result_form=CreateResultForm()
    context['create_result_form']=create_result_form
    return render(request, 'result/search_result.html', context=context)
@login_required
def OptionHighestMarks(request):
    context={}
    highest_marks_form=HighestMarksForm()
    context['highest_marks_form']=highest_marks_form
    return render(request, 'result/search_result.html', context=context)

@login_required
def OptionDeleteResult(request):
    context={}
    delete_result_form=DeletResultForm()
    context['delete_result_form']=delete_result_form
    return render(request, 'result/search_result.html', context=context)


@login_required
def OptionCreatePosition(request):
    context={}
    create_position_form=CreateResultForm()
    #print(create_position_form)
    context['create_position_form']=create_position_form
    return render(request, 'result/search_result.html', context=context)


@login_required
def createResult(request):
    if request.user.is_superuser:
        exam=Exam.objects.filter(id=request.POST.get('exam')).first()
        del_result=Result.objects.filter(exam=exam).delete()
        if exam.id == 3:
            rolls=list(TestMarks.objects.filter(exam=exam).values('class_roll').order_by('class_roll').distinct())
        else:
            rolls=list(Marks.objects.filter(exam=exam).values('class_roll').order_by('class_roll').distinct())

        print('Number of Student:',rolls.count)
        count=0
        choice_list=[]
        
        for roll in rolls[0:500]:
            if exam.id == 3:
                result=TestMarks.objects.filter(class_roll=roll['class_roll'])
            else:
                result=Marks.objects.filter(class_roll=roll['class_roll'])
            # if result.count()<7:
            #     print(result)
            #     continue
                # messages.success(request,exam.title_en+" Result Not Created Successfully! -->All subject marks not entered")
                # return redirect('option_create_result')            
            student=Student.objects.filter(class_roll=roll['class_roll']).first()
            subject_choice=Choice.objects.filter(class_roll=roll['class_roll'].strip()).first()
            
            if subject_choice:
                choice_list=[subject_choice.subject1,subject_choice.subject2,subject_choice.subject3,subject_choice.subject4,subject_choice.subject5,subject_choice.subject6,subject_choice.fourth_subject]
                
                #print(choice_list)
            totalgpa=0
            absent_or_fail_without_4th=0
            totalgpa1=0
            total=0
            flag1=0
            flag2=0
            absent_at=0
            fail_at=0
            fail_at_without_4th=0
            pass_at_without_4th=0
            present_at=0
            pass_at=0
            remarks=None
            
            for reslt in result:
                if reslt.subject  in choice_list:
                    if reslt.grade=="Absent":
                        absent_at=absent_at+1
                        absent_or_fail_without_4th=absent_or_fail_without_4th+1
                        grade="Absent"
                        cgpa=None
                        cgpa_without_4th=None
                        flag1=1

                    elif reslt.grade=="F" :
                        if subject_choice:
                            if reslt.subject != subject_choice.fourth_subject:
                                # print("Fourth_Subject: Eliif_top",subject_choice.fourth_subject,reslt.subject,reslt.class_roll)
                                present_at=present_at+1
                                fail_at=fail_at+1
                                fail_at_without_4th=fail_at_without_4th+1
                                absent_or_fail_without_4th=absent_or_fail_without_4th+1
                                grade="F"
                                cgpa=0
                                cgpa_without_4th=0
                                flag2=1
                                total=total+reslt.total
                            else:
                                total=total+reslt.total
                                fail_at=fail_at+1



                        
                    else:
                        #print(student.fourth_subject,reslt.subject)
                        if student and subject_choice:
                            print("Fourth_Subject: top",subject_choice.fourth_subject,reslt.subject,reslt.class_roll)
                            
                            if reslt.subject == subject_choice.fourth_subject:
                                print("Fourth_Subject: equal",subject_choice.fourth_subject)
                                present_at=present_at+1
                                pass_at = pass_at+1
                                cg=float(reslt.cgpa)
                                total=total+reslt.total
                                if cg>2:
                                    gpa=cg-2
                                    totalgpa=totalgpa+gpa

                            else:
                                present_at=present_at+1
                                pass_at_without_4th=pass_at_without_4th+1
                                pass_at=pass_at+1
                                total=total+reslt.total
                                totalgpa=totalgpa+float(reslt.cgpa)
                                totalgpa1=totalgpa1+float(reslt.cgpa)
            
            if absent_at==7:
                grade="AbsentAll"
                remarks="Not Promoted"
                result_individual=Result.objects.create(class_roll=roll['class_roll'],name=student.name,position=count,group=student.group,section=student.section,exam=exam,total=total,cgpa=cgpa,cgpa_without_4th=cgpa_without_4th,grade=grade,present_at=present_at,absent_at=absent_at,fail_at=fail_at,fail_at_without_4th=fail_at_without_4th,absent_or_fail_without_4th=absent_or_fail_without_4th, pass_at=pass_at,pass_at_without_4th=pass_at_without_4th,remarks=remarks)

            elif flag1==1 or flag2==1 :
                count_fail=absent_at+fail_at
                # Number of subject failed to be
                if pass_at_without_4th>exam.minimum_threshold:
                    remarks="Promoted"
                else:
                    remarks="Not Promoted"                   
                if student:
                    result_individual=Result.objects.create(class_roll=roll['class_roll'],name=student.name,position=count,group=student.group,section=student.section,exam=exam,total=total,cgpa=cgpa,cgpa_without_4th=cgpa_without_4th,grade=grade,present_at=present_at,absent_at=absent_at,fail_at=fail_at,fail_at_without_4th=fail_at_without_4th,absent_or_fail_without_4th=absent_or_fail_without_4th,pass_at=pass_at,pass_at_without_4th=pass_at_without_4th,remarks=remarks)
            else:
                #print(grade)
                cgpa=round(totalgpa/6,2)
                cgpa_without_4th=round(totalgpa1/6,2)

                if cgpa<1:
                    grade="F"
                elif cgpa>=1 and cgpa<2:
                    grade="D"
                elif cgpa>=2 and cgpa<3:
                    grade="C"
                elif cgpa>=3 and cgpa<3.5:
                    grade="B"
                elif cgpa>=3.5 and cgpa<4:
                    grade="A-"
                elif cgpa>=4 and cgpa<5:
                    grade="A"
                elif cgpa>=5:
                    grade="A+"
                else:
                    grade="Absent"
                    remarks="Not Promoted"                   
                if student:
                    #print(student.name)
                    remarks="Promoted"                   
                    result_individual=Result.objects.create(class_roll=roll['class_roll'],name=student.name,position=count,group=student.group,section=student.section,exam=exam,total=total,cgpa=cgpa,cgpa_without_4th=cgpa_without_4th,grade=grade,present_at=present_at,absent_at=absent_at,fail_at=fail_at,fail_at_without_4th=fail_at_without_4th,absent_or_fail_without_4th=absent_or_fail_without_4th,pass_at=pass_at,pass_at_without_4th=pass_at_without_4th,remarks=remarks)
            count=count+1

            
        
        #print(count,result)
        messages.success(request,exam.title_en+" Result Created Successfully")
        return redirect('option_create_result')
    messages.success(request,exam.title_en+" Result Created Successfully")
    return redirect('option_create_result')


@login_required
def deleteResult(request):
    if request.user.is_superuser:
        exam=Exam.objects.filter(id=request.POST.get('exam')).first()
        for row in Result.objects.filter(exam=exam).reverse():
            if Result.objects.filter(class_roll=row.class_roll).count() > 1:
                row.delete()
        messages.success(request,exam.title_en+" Result deleted Successfully")
        return redirect('option_delete_result')
    messages.success(request,exam.title_en+" -You have no permission to delete result")
    return redirect('option_delete_result')

@login_required
def CreatePosition(request):
    if request.user.is_superuser:
        exam=Exam.objects.filter(id=request.POST.get('exam')).first()    
        group1=Group.objects.filter(id=3).first()
        group2=Group.objects.filter(id=4).first()
        group3=Group.objects.filter(id=5).first()
        result1=Result.objects.filter(group=group1,exam=exam).order_by('-cgpa','-total')
        result2=Result.objects.filter(group=group2,exam=exam).order_by('-cgpa','-total')
        result3=Result.objects.filter(group=group3,exam=exam).order_by('-cgpa','-total')
        if result1==None or result2==None or result3==None:
            messages.success(request,exam.title_en+" Result Not found")
            return redirect('option_create_position')
        count=0
        cgpa_prev=0
        total=0
        for rslt in result1:
            print('Cgpa: ',rslt.cgpa)
            if cgpa_prev==rslt.cgpa and total==rslt.total:
                rslt.position=count
                cgpa_prev=rslt.cgpa
                total=rslt.total
                rslt.save(update_fields=['position'])
                print('if clause',rslt.position)
            else:
                rslt.position=count+1
                count=count+1
                cgpa_prev=rslt.cgpa
                total=rslt.total
                rslt.save(update_fields=['position'])
                print('else clause',rslt.position)

        count=0
        cgpa_prev=0
        total=0
        for rslt in result2:
            #print('Cgpa: ',rslt.cgpa)
            if cgpa_prev==rslt.cgpa and total==rslt.total:
                rslt.position=count
                cgpa_prev=rslt.cgpa
                total=rslt.total
                rslt.save(update_fields=['position'])
                #print('if clause',rslt.position)
            else:
                rslt.position=count+1
                count=count+1
                cgpa_prev=rslt.cgpa
                total=rslt.total
                rslt.save(update_fields=['position'])
                #print('else clause',rslt.position)
        count=0
        cgpa_prev=0
        total=0
        for rslt in result3:
            #print('Cgpa: ',rslt.cgpa)
            if cgpa_prev==rslt.cgpa and total==rslt.total:
                rslt.position=count
                cgpa_prev=rslt.cgpa
                total=rslt.total
                rslt.save(update_fields=['position'])
                #print('if clause',rslt.position)
            else:
                rslt.position=count+1
                count=count+1
                cgpa_prev=rslt.cgpa
                total=rslt.total
                rslt.save(update_fields=['position'])
                #print('else clause',rslt.position)
        messages.success(request,exam.title_en+" Position Created Successfully")
        return redirect('option_create_position')
    messages.success(request,exam.title_en+" -You have no permission to Create Position")
    return redirect('option_create_position')

def CreateHighestMarks(request):
    if request.user.is_superuser:
        exam=Exam.objects.filter(id=request.POST.get('exam')).first() 
        print(exam)

        subject=Subject.objects.all()
        for subjt in subject:
            marks=Marks.objects.filter(subject=subjt,exam=exam).order_by('-total')
            highest_mark=marks.first()
            highest_mark=HighestMarks.objects.create(class_roll=highest_mark.class_roll,exam=exam,subject=subjt,highest_mark=highest_mark.total)
            for mark in marks:
                mark.highest_mark=highest_mark
                mark.save(update_fields=['highest_mark'])

        messages.success(request,exam.title_en+" Highest Marks Created Successfully")
        return redirect('option_delete_result')
    messages.success(request,exam.title_en+" -You have no permission to Create Highest Marks")
    return redirect('option_highest_marks')