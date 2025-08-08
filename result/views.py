from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render,redirect
from .models import Marks,Exam,Result,HighestMarks,TestMarks,SubjectWiseMarksSummery
from payment.models import Transaction, PaymentPurpose
from student.models import Session
from student.models import Student,Group,Choice,Subject
from .forms import SeachResultForm,CreateResultForm,DeletResultForm,CreatePositionForm,HighestMarksForm,SummeryResultForm,SubjectWiseMarksForm
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
        transaction=Transaction.objects.filter(class_roll=request.POST.get('roll'),tran_purpose=exam.tran_purpose).first()
        if  exam.type == '2' or  exam.type == '4' and transaction is None:
            form=SeachResultForm(current_user=request.user)
            context['notfound']="We can't find your payment history"
            context['form']=form
            return render(request, 'result/search_result.html', context=context)
        if exam.type == '2':
            marks=TestMarks.objects.filter(class_roll=request.POST.get('roll').strip(),exam=exam).order_by('subject')
        else:
            marks=Marks.objects.filter(class_roll=request.POST.get('roll'),exam=exam).order_by('subject')
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
            # messages.add_message('Result not found!!re=Enter Right Information or Contact exam control room')
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
        elif exam.type == '3':
            return render(request, 'result/show_result_class_test.html', context=context)
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
def OptionSubjectWiseMarks(request):
    context={}
    subject_wise_marks_form=SubjectWiseMarksForm()
    context['subject_wise_marks_form']=subject_wise_marks_form
    return render(request, 'result/search_result.html', context=context)
@login_required
def OptionSummeryResult(request):
    context={}
    summery_result_form=SummeryResultForm()
    context['summery_result_form']=summery_result_form
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
        
        rolls=list(Transaction.objects.filter(tran_purpose=exam.tran_purpose).values('class_roll').order_by('class_roll'))
        
        # return HttpResponse(len(rolls))
        # if exam.id == 3:
        #     rolls=list(TestMarks.objects.filter(exam=exam).values('class_roll').order_by('class_roll').distinct())
        # else:
        #     rolls=list(Marks.objects.filter(exam=exam).values('class_roll').order_by('class_roll').distinct())

        # print('Number of Student:',rolls.count)
        count=0
        choice_list=[]
        
        for roll in rolls:
            if exam.id == 3:
                result=TestMarks.objects.filter(class_roll=roll['class_roll'],exam=exam)
            else:
                result=Marks.objects.filter(class_roll=roll['class_roll'],exam=exam)
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
            totalcq=0
            flag1=0
            flag2=0
            flag3=0
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
                        if exam.is_practical_applicable and reslt.practical is None and reslt.subject.is_practical :
                            flag3=1
                        cgpa=None
                        cgpa_without_4th=None
                        flag1=1

                    elif reslt.grade=="F" :
                        if exam.type == '3':
                            if reslt.CQ:
                                totalcq=totalcq + reslt.CQ
                                print(reslt.subject,reslt.CQ)
                        if subject_choice:
                            if reslt.subject != subject_choice.fourth_subject:
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
                            #print("Fourth_Subject: top",subject_choice.fourth_subject,reslt.subject,reslt.class_roll)
                            
                            if reslt.subject == subject_choice.fourth_subject:
                                #print("Fourth_Subject: equal",subject_choice.fourth_subject)
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
                if exam.type == '3':
                    if student:
                        result_individual=Result.objects.create(class_roll=roll['class_roll'],name=student.name,position=count,group=student.group,section=student.section,exam=exam,total=totalcq,cgpa=cgpa,cgpa_without_4th=cgpa_without_4th,grade=grade,present_at=present_at,absent_at=absent_at,fail_at=fail_at,fail_at_without_4th=fail_at_without_4th,absent_or_fail_without_4th=absent_or_fail_without_4th, pass_at=pass_at,pass_at_without_4th=pass_at_without_4th,remarks=remarks)
                else:
                    result_individual=Result.objects.create(class_roll=roll['class_roll'],name=student.name,position=count,group=student.group,section=student.section,exam=exam,total=total,cgpa=cgpa,cgpa_without_4th=cgpa_without_4th,grade=grade,present_at=present_at,absent_at=absent_at,fail_at=fail_at,fail_at_without_4th=fail_at_without_4th,absent_or_fail_without_4th=absent_or_fail_without_4th, pass_at=pass_at,pass_at_without_4th=pass_at_without_4th,remarks=remarks)

            elif flag1==1 or flag2==1 :
                count_fail=absent_at+fail_at
                # Number of subject failed to be
                if pass_at_without_4th >= exam.minimum_threshold:
                    if flag3 == 1:
                        remarks="Postponed"
                    else:
                        remarks="Promoted"
                else:
                    if flag3 == 1:
                        remarks="Postponed"
                    else:
                        remarks="Not Promoted"                   
                if student:
                    if exam.type == '3':
                        if student:
                            result_individual=Result.objects.create(class_roll=roll['class_roll'],name=student.name,position=count,group=student.group,section=student.section,exam=exam,total=totalcq,cgpa=cgpa,cgpa_without_4th=cgpa_without_4th,grade=grade,present_at=present_at,absent_at=absent_at,fail_at=fail_at,fail_at_without_4th=fail_at_without_4th,absent_or_fail_without_4th=absent_or_fail_without_4th, pass_at=pass_at,pass_at_without_4th=pass_at_without_4th,remarks=remarks)
                    else:
                        result_individual=Result.objects.create(class_roll=roll['class_roll'],name=student.name,position=count,group=student.group,section=student.section,exam=exam,total=total,cgpa=cgpa,cgpa_without_4th=cgpa_without_4th,grade=grade,present_at=present_at,absent_at=absent_at,fail_at=fail_at,fail_at_without_4th=fail_at_without_4th,absent_or_fail_without_4th=absent_or_fail_without_4th, pass_at=pass_at,pass_at_without_4th=pass_at_without_4th,remarks=remarks)

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
                    remarks="Promoted"                   
                    if exam.type == '3':
                        if student:
                            result_individual=Result.objects.create(class_roll=roll['class_roll'],name=student.name,position=count,group=student.group,section=student.section,exam=exam,total=totalcq,cgpa=cgpa,cgpa_without_4th=cgpa_without_4th,grade=grade,present_at=present_at,absent_at=absent_at,fail_at=fail_at,fail_at_without_4th=fail_at_without_4th,absent_or_fail_without_4th=absent_or_fail_without_4th, pass_at=pass_at,pass_at_without_4th=pass_at_without_4th,remarks=remarks)
                    else:
                        result_individual=Result.objects.create(class_roll=roll['class_roll'],name=student.name,position=count,group=student.group,section=student.section,exam=exam,total=total,cgpa=cgpa,cgpa_without_4th=cgpa_without_4th,grade=grade,present_at=present_at,absent_at=absent_at,fail_at=fail_at,fail_at_without_4th=fail_at_without_4th,absent_or_fail_without_4th=absent_or_fail_without_4th, pass_at=pass_at,pass_at_without_4th=pass_at_without_4th,remarks=remarks)
            count=count+1

            
        
        #print(count,result)
        messages.success(request,exam.title_en+" Result Created Successfully")
        return redirect('option_create_result')
    messages.success(request,exam.title_en+" Result Created Successfully")
    return redirect('option_create_result')



@login_required
def SummeryResult(request):
    if request.user.is_superuser:
        context={}
        exam=Exam.objects.filter(id=request.POST.get('exam')).first()
        session=Session.objects.filter(id=request.POST.get('session')).first()
        all_examinee_all=Student.objects.filter(session=session,department=None)
        all_examinee=Result.objects.filter(exam=exam).exclude(grade="AbsentAll")
        all_examinee_absent_all=all_examinee_all.count()- all_examinee.count()
        all_subject_pass=Result.objects.filter(exam=exam,pass_at=7)
        pass_at_4_without_4th=Result.objects.filter(exam=exam,pass_at_without_4th__gte=4)
        pass_at_3_without_4th=Result.objects.filter(exam=exam,pass_at_without_4th__gte=3)
        rate_of_pass=round((all_subject_pass.count()/all_examinee.count())*100,2)
        context['all_examinee_all']=all_examinee_all
        context['all_examinee']=all_examinee
        context['all_examinee_absent_all']=all_examinee_absent_all
        context['all_subject_pass']=all_subject_pass
        context['pass_at_4_without_4th']=pass_at_4_without_4th
        context['pass_at_3_without_4th']=pass_at_3_without_4th
        context['rate_of_pass']=rate_of_pass
        context['exam']=exam
       
        science_examinee=Result.objects.filter(exam=exam,group=3).exclude(grade="AbsentAll")
        science_examinee_all=Student.objects.filter(session=session,department=None,group=3)
        science_examinee_absent_all=science_examinee_all.count() - science_examinee.count()
        science_all_subject_pass=Result.objects.filter(exam=exam,group=3,pass_at=7)
        science_pass_at_4_without_4th=Result.objects.filter(exam=exam,group=3,pass_at_without_4th__gte=4)
        science_pass_at_3_without_4th=Result.objects.filter(exam=exam,group=3,pass_at_without_4th__gte=3)
        science_rate_of_pass=round((science_all_subject_pass.count()/science_examinee.count())*100,2)
        context['science_examinee']=science_examinee
        context['science_examinee_all']=science_examinee_all
        context['science_examinee_absent_all']=science_examinee_absent_all
        context['science_all_subject_pass']=science_all_subject_pass
        context['science_pass_at_4_without_4th']=science_pass_at_4_without_4th
        context['science_pass_at_3_without_4th']=science_pass_at_3_without_4th
        context['science_rate_of_pass']=science_rate_of_pass
        
        
        humanities_examinee=Result.objects.filter(exam=exam,group=4).exclude(grade="AbsentAll")
        humanities_examinee_all=Student.objects.filter(session=session,department=None,group=4)
        humanities_examinee_absent_all=humanities_examinee_all.count() - humanities_examinee.count()
        humanities_all_subject_pass=Result.objects.filter(exam=exam,group=4,pass_at=7)
        humanities_pass_at_4_without_4th=Result.objects.filter(exam=exam,group=4,pass_at_without_4th__gte=4)
        humanities_pass_at_3_without_4th=Result.objects.filter(exam=exam,group=4,pass_at_without_4th__gte=3)
        humanities_rate_of_pass=round((humanities_all_subject_pass.count()/humanities_examinee.count())*100,2)
        
        context['humanities_examinee']=humanities_examinee
        context['humanities_examinee_all']=humanities_examinee_all
        context['humanities_examinee_absent_all']=humanities_examinee_absent_all
        context['humanities_all_subject_pass']=humanities_all_subject_pass
        context['humanities_pass_at_4_without_4th']=humanities_pass_at_4_without_4th
        context['humanities_pass_at_3_without_4th']=humanities_pass_at_3_without_4th
        context['humanities_rate_of_pass']=humanities_rate_of_pass
        
        
        business_examinee=Result.objects.filter(exam=exam,group=5).exclude(grade="AbsentAll")
        business_examinee_all=Student.objects.filter(session=session,department=None,group=5)
        business_examinee_absent_all=business_examinee_all.count() - business_examinee.count()
        business_all_subject_pass=Result.objects.filter(exam=exam,group=5,pass_at=7)
        business_pass_at_4_without_4th=Result.objects.filter(exam=exam,group=5,pass_at_without_4th__gte=4)
        business_pass_at_3_without_4th=Result.objects.filter(exam=exam,group=5,pass_at_without_4th__gte=3)
        business_rate_of_pass=round((business_all_subject_pass.count()/business_examinee.count())*100,2)
        context['business_examinee']=business_examinee
        context['business_examinee_all']=business_examinee_all
        context['business_examinee_absent_all']=business_examinee_absent_all
        context['business_all_subject_pass']=business_all_subject_pass
        context['business_pass_at_4_without_4th']=business_pass_at_4_without_4th
        context['business_pass_at_3_without_4th']=business_pass_at_3_without_4th
        context['business_rate_of_pass']=business_rate_of_pass

      
        return render(request,'result/report_summery.html',context)
@login_required
def SubjectWiseMarks(request):
    if request.user.is_superuser:
        context={}
        exam=Exam.objects.filter(id=request.POST.get('exam')).first()
        session=Session.objects.filter(id=request.POST.get('session')).first()
        SubjectWiseMarksSummery.objects.filter(exam=exam).delete()
        subjects=Subject.objects.all()
        for subject in subjects:
            all_examinee_all=Student.objects.filter(session=session,department=None).count()
            all_participant=Marks.objects.filter(~Q(grade= "Absent"), subject=subject,exam=exam ).count()
            all_examinee_fail=Marks.objects.filter(subject=subject,exam=exam,grade="F").count()
            all_examinee_absent=Marks.objects.filter(subject=subject,exam=exam,grade="Absent").count()
            all_pass=all_examinee_all -all_examinee_fail- all_examinee_absent
            A_plus=Marks.objects.filter(subject=subject,exam=exam,grade="A+").count()
            A=Marks.objects.filter(subject=subject,exam=exam,grade="A").count()
            A_minus=Marks.objects.filter(subject=subject,exam=exam,grade="A-").count()
            B=Marks.objects.filter(subject=subject,exam=exam,grade="B").count()
            C=Marks.objects.filter(subject=subject,exam=exam,grade="C").count()
            D=Marks.objects.filter(subject=subject,exam=exam,grade="D").count()
            if all_examinee_all:
                rate_of_pass=round((all_pass/all_examinee_all)*100,2)
                rate_of_fail=round((all_examinee_fail/all_examinee_all)*100,2)
                rate_of_absent=100- rate_of_pass- rate_of_fail
                context['subject']=subject
                context['exam']=exam
                SubjectWiseMarksSummery.objects.create(subject=subject,exam=exam,session=session,
                            all_participant=all_participant,all_pass=all_pass,all_fail=all_examinee_fail,
                            all_absent=all_examinee_absent,percentage_pass=rate_of_pass,percentage_fail=rate_of_fail,
                            percentage_absent=rate_of_absent,A_plus=A_plus,A=A,A_minus=A_minus,B=B,C=C,D=D)
                           

        return HttpResponse("subject wise marks summery created")

@login_required
def GetSubjectWiseMarks(request):
    if request.user.is_superuser:
        context={}
        exam=Exam.objects.filter(id=request.POST.get('exam')).first()
        session=Session.objects.filter(id=request.POST.get('session')).first()
        subject_wise_summery=SubjectWiseMarksSummery.objects.filter(exam=exam)
        context['subject_wise_summery']=subject_wise_summery
        return render(request,'result/report_subject_wise_marks.html',context)

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

        subject=Subject.objects.all()
        for subjt in subject:
            if exam.type == '3':
                marks=Marks.objects.filter(subject=subjt,exam=exam).order_by('-CQ')
            else:
                marks=Marks.objects.filter(subject=subjt,exam=exam).order_by('-total')

            highest_mark=marks.first()
            if exam.type == '3':
                highest_mark=HighestMarks.objects.create(class_roll=highest_mark.class_roll,exam=exam,subject=subjt,highest_mark=highest_mark.CQ)
            else:
                highest_mark=HighestMarks.objects.create(class_roll=highest_mark.class_roll,exam=exam,subject=subjt,highest_mark=highest_mark.total)
            for mark in marks:
                mark.highest_mark=highest_mark
                mark.save(update_fields=['highest_mark'])

        messages.success(request,exam.title_en+" Highest Marks Created Successfully")
        return redirect('option_delete_result')
    messages.success(request,exam.title_en+" -You have no permission to Create Highest Marks")
    return redirect('option_highest_marks')