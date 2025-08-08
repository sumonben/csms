from django.contrib import admin
from django.db.models import Q
from .models import Exam,Marks,Result,HighestMarks,TestMarks,SubjectWiseMarksSummery
from student.models import Student,Choice
from django.http import HttpResponse
from import_export.admin import ExportActionMixin,ImportExportMixin
from rangefilter.filters import (
    DateRangeFilterBuilder,
    DateTimeRangeFilterBuilder,
    NumericRangeFilterBuilder,
    DateRangeQuickSelectListFilterBuilder,
)
import csv

# Register your models here.
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display=[  'id','serial','title_en',]
    list_filter=[  'title_en',]
    list_display_links = ['id','serial','title_en',]
@admin.register(HighestMarks)
class HighestMarksAdmin(admin.ModelAdmin):
    list_display=[  'id','class_roll','subject','highest_mark','exam']
    list_filter=[  'class_roll','exam','subject']
    list_display_links = ['id','class_roll',]

@admin.register(SubjectWiseMarksSummery)
class SubjectWiseMarksSummeryAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=[  'id','subject','exam' ,'percentage_pass','percentage_fail','percentage_absent']
    list_filter=[  'exam','subject']
    list_display_links = ['id',]
    actions = ('export_subject_wise_marks',)
    def export_subject_wise_marks(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        header = field_names
        writer.writerow(header)
        for obj in queryset:
            row = [getattr(obj, field) for field in field_names]
            if row:
                writer.writerow(row)
        return response

    export_subject_wise_marks.short_description = "Subject Wise marks export"

@admin.register(TestMarks)
class TestMarksAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=[  'id','class_roll','name','subject_name','MCQ1','CQ1','MCQ2','CQ2','total','grade','cgpa','exam','cgpa_1st','cgpa_2nd','group','grade_1st','grade_2nd']
    search_fields=['class_roll']
    list_display_links = ['id','class_roll']
    list_filter=[  'grade','cgpa','exam','subject','group']
    def get_import_data_kwargs(self, **kwargs):
        return super().get_import_data_kwargs(**kwargs)
@admin.register(Marks)
class MarksAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=[  'id','class_roll','name','subject_name','MCQ','CQ','practical','total','grade','cgpa','exam','group']
    search_fields=['class_roll']
    list_display_links = ['id','class_roll']
    list_filter=[  'grade','cgpa','exam','subject','group']
    def get_import_data_kwargs(self, **kwargs):
        return super().get_import_data_kwargs(**kwargs)
@admin.register(Result)
class ResultAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=[  'class_roll','position','name','group','section','exam','total','cgpa','cgpa_without_4th','grade','absent_at','fail_at','fail_at_without_4th','pass_at','pass_at_without_4th','present_at','absent_or_fail_at','absent_or_fail_without_4th','remarks']
    search_fields=['class_roll']
    list_display_links = ['class_roll','name']
    list_filter=( 'group','cgpa','exam','grade','section',('cgpa', NumericRangeFilterBuilder()),('pass_at', NumericRangeFilterBuilder()),('fail_at', NumericRangeFilterBuilder()),('fail_at_without_4th', NumericRangeFilterBuilder()),('absent_at', NumericRangeFilterBuilder()),('absent_or_fail_at', NumericRangeFilterBuilder()),('absent_or_fail_without_4th', NumericRangeFilterBuilder()),'remarks')
    actions = ('export_as_csv','export_absent_all_subject')
    def export_as_csv(self, request, queryset):
    
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        header = field_names + ['Subject1','Subject2','Subject3','Subject4','Subject5','Subject6','Optional Subject',]
        writer.writerow(header)
        for obj in queryset:
            row = [getattr(obj, field) for field in field_names]
            subject_failed=Marks.objects.filter(class_roll=obj.class_roll,exam=obj.exam).filter(Q(grade ='F') | Q(grade= "Absent") )
            subject_choice=Choice.objects.filter(class_roll=obj.class_roll).first()
            
            if subject_choice:
                choice_list=[subject_choice.subject1,subject_choice.subject2,subject_choice.subject3,subject_choice.subject4,subject_choice.subject5,subject_choice.subject6,subject_choice.fourth_subject]
          
            for subject in subject_failed:
                if subject.subject in choice_list:
                    row.append(subject.subject.name_en)
            if row:
                writer.writerow(row)
        return response

    export_as_csv.short_description = "Not promoted with subjects list"
    
    def export_absent_all_subject(self, request, queryset):
    
        meta =Student._meta
        field_names = ['Class Roll','Name','Group']
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        header = field_names 
        writer.writerow(header)
        rolls=list(queryset.order_by())
        student=Student.objects.filter(class_roll=queryset[0].class_roll,group=queryset[0].group).first()
        students=Student.objects.filter(session=student.session,department=None).order_by('class_roll')
        rolls2=[]
        for roll in rolls:
            rolls2.append(roll.class_roll)
        for student in students:
            if student.class_roll not in rolls2:
                row = [student.class_roll,student.name,student.group]
                writer.writerow(row)
            
        return response