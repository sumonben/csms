from django.http import HttpResponse
from django.shortcuts import render
from .models import Marks,Exam,Result
from student.models import Student,Group,Choice
from .forms import SeachResultForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def searchResult(request):
    context={}
    flag1=0
    flag2=0
    
    if request.method=='POST':
        totalgpa=0
        totalgpa1=0

        result=Marks.objects.filter(class_roll=request.POST.get('roll').strip()).order_by('subject')
        print(result)
        position=Result.objects.filter(class_roll=request.POST.get('roll').strip()).first()
        student=Student.objects.filter(class_roll=request.POST.get('roll').strip()).first()
        print(student)
        subject_choice=Choice.objects.filter(class_roll=request.POST.get('roll').strip()).first()
        exam=Exam.objects.filter(id=request.POST.get('exam')).first()
        if subject_choice and student and result and exam:
            choice_list=[subject_choice.subject1,subject_choice.subject2,subject_choice.subject3,subject_choice.subject4,subject_choice.subject5,subject_choice.subject6,subject_choice.fourth_subject]
        else:
            context['notfound']="Result not found!!re=Enter Right Information or Contact exam control room"
            form=SeachResultForm()
            context['form']=form
            return render(request, 'result/search_result.html', context=context)
        context['result']=result
        context['position']=position
        context['student']=student
        context['exam']=exam
        context['choice_list']=choice_list

        
        for reslt in result:
            print(reslt.subject,reslt.cgpa,reslt.grade,reslt.total)
            if reslt.subject  in choice_list:
                if reslt.grade=="Absent":
                    grade="Absent"
                    cgpa=None
                    context['grade']=grade
                    context['cgpa']=cgpa
                    flag1=1
                    return render(request, 'result/show_result.html', context=context)

                elif reslt.grade=="F" and reslt.subject !=subject_choice.fourth_subject:
                    grade="F"
                    cgpa=0
                    context['grade']=grade
                    context['cgpa']=cgpa
                    flag2=1
                    
                else:
                    #print(student.fourth_subject,reslt.subject)
                    if student:
                        if reslt.subject == student.fourth_subject:
                            cg=float(reslt.cgpa)
                            if cg>2:
                                gpa=cg-2
                                totalgpa=totalgpa+gpa

                        else:
                            totalgpa=totalgpa+float(reslt.cgpa)
                            totalgpa1=totalgpa1+float(reslt.cgpa)
                            print(totalgpa1)

        if flag2==1 or flag1==1:
            return render(request, 'result/show_result.html', context=context)
        
        else:
            #print(grade)
            cgpa=totalgpa/6
            context['cgpa']=round(cgpa,2)
            cgpa_witout_4th=totalgpa1/6
            context['cgpa_witout_4th']=round(cgpa_witout_4th,2)

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
            context['grade']=grade

        
        
   
        return render(request, 'result/show_result.html', context=context)
    form=SeachResultForm()
    context['form']=form
    return render(request, 'result/search_result.html', context=context)

@login_required
def createResult(request):
        rolls=list(Marks.objects.filter(exam=1).values('class_roll').order_by('class_roll').distinct())
        exam=Exam.objects.filter(id=1).first()
        count=0
        choice_list=[]
        for roll in rolls:
            result=Marks.objects.filter(class_roll=roll['class_roll'])
            student=Student.objects.filter(class_roll=roll['class_roll']).first()
            subject_choice=Choice.objects.filter(class_roll=roll['class_roll'].strip()).first()
            if subject_choice:
                choice_list=[subject_choice.subject1,subject_choice.subject2,subject_choice.subject3,subject_choice.subject4,subject_choice.subject5,subject_choice.subject6,subject_choice.fourth_subject]
                print(choice_list)
            totalgpa=0
            totalgpa1=0
            total=0
            flag1=0
            flag2=0
            absent_at=0
            fail_at=0
            fail_at_without_4th=0
            present_at=0
            pass_at=0
            remarks=None

            for reslt in result:
                if reslt.subject  in choice_list:
                    if reslt.grade=="Absent":
                        absent_at=absent_at+1
                        grade="Absent"
                        cgpa=None
                        flag1=1

                    elif reslt.grade=="F" and reslt.subject !=subject_choice.fourth_subject :
                        present_at=present_at+1
                        fail_at=fail_at+1
                        fail_at_without_4th=fail_at_without_4th+1
                        grade="F"
                        cgpa=0
                        flag2=1
                        total=total+reslt.total

                        
                    else:
                        #print(student.fourth_subject,reslt.subject)
                        if student:
                            if reslt.subject == student.fourth_subject:
                                present_at=present_at+1

                                if reslt.grade=="F":
                                    fail_at=fail_at+1
                                else:
                                    pass_at=pass_at+1
                                cg=float(reslt.cgpa)
                                total=total+reslt.total

                                if cg>2:
                                    gpa=cg-2
                                    totalgpa=totalgpa+gpa

                            else:
                                present_at=present_at+1
                                pass_at=pass_at+1
                                total=total+reslt.total
                                totalgpa=totalgpa+float(reslt.cgpa)
            if absent_at==7:
                grade="AbsentAll"
                remarks="Not Promoted"
                result_individual=Result.objects.create(class_roll=roll['class_roll'],name=student.name,position=count,group=student.group,section=student.section,exam=exam,total=total,cgpa=cgpa,grade=grade,present_at=present_at,absent_at=absent_at,fail_at=fail_at,fail_at_without_4th=fail_at_without_4th,pass_at=pass_at,remarks=remarks)

            elif flag1==1 or flag2==1 :
                count_fail=absent_at+fail_at
                # Number of subject failed to be
                if count_fail>3:
                    remarks="Not Promoted"
                else:
                    remarks="Promoted"                   
                if student:
                    result_individual=Result.objects.create(class_roll=roll['class_roll'],name=student.name,position=count,group=student.group,section=student.section,exam=exam,total=total,cgpa=cgpa,grade=grade,present_at=present_at,absent_at=absent_at,fail_at=fail_at,fail_at_without_4th=fail_at_without_4th,pass_at=pass_at,remarks=remarks)
            else:
                #print(grade)
                cgpa=round(totalgpa/6,2)

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
                if student:
                    print(student.name)
                    remarks="Promoted"                   
                    result_individual=Result.objects.create(class_roll=roll['class_roll'],name=student.name,position=count,group=student.group,section=student.section,exam=exam,total=total,cgpa=cgpa,grade=grade,present_at=present_at,absent_at=absent_at,fail_at=fail_at,fail_at_without_4th=fail_at_without_4th,pass_at=pass_at,remarks=remarks)
            count=count+1

            
        
        print(count,result)

        return HttpResponse('Result Created Successfully!')

@login_required
def deleteResult(request):
    for row in Result.objects.all().reverse():
        if Result.objects.filter(class_roll=row.class_roll).count() > 1:
            row.delete()
    return HttpResponse("Data Deleted successfully!!")

@login_required
def CreatePosition(request):
    group1=Group.objects.filter(id=3).first()
    group2=Group.objects.filter(id=4).first()
    group3=Group.objects.filter(id=5).first()
    result1=Result.objects.filter(group=group1).order_by('-cgpa','-total')
    result2=Result.objects.filter(group=group2).order_by('-cgpa','-total')
    result3=Result.objects.filter(group=group3).order_by('-cgpa','-total')
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
    for rslt in result3:
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
         

    return HttpResponse("Position Created successfully!!")