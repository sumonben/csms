from django.contrib import admin
from .models import Exam,Marks,Result,HighestMarks,TestMarks
from import_export.admin import ExportActionMixin,ImportExportMixin

# Register your models here.
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display=[  'id','serial','title_en',]
    list_filter=[  'title_en',]
    list_display_links = ['id','serial','title_en',]
@admin.register(HighestMarks)
class HighestMarksAdmin(admin.ModelAdmin):
    list_display=[  'id','class_roll','subject','highest_mark','exam']
    list_filter=[  'class_roll',]
    list_display_links = ['id','class_roll',]

@admin.register(TestMarks)
class TestMarksAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=[  'id','class_roll','name','subject_name','MCQ1','CQ1','MCQ2','CQ2','total','grade','cgpa','exam','group']
    search_fields=['class_roll']
    list_display_links = ['id','class_roll']
    list_filter=[  'grade','cgpa','exam','subject','group']
    def get_import_data_kwargs(self, **kwargs):
        return super().get_import_data_kwargs(**kwargs)
@admin.register(Marks)
class MarksAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=[  'id','class_roll','name','subject_name','MCQ','CQ','total','grade','cgpa','exam','group']
    search_fields=['class_roll']
    list_display_links = ['id','class_roll']
    list_filter=[  'grade','cgpa','exam','subject','group']
    def get_import_data_kwargs(self, **kwargs):
        return super().get_import_data_kwargs(**kwargs)
@admin.register(Result)
class ResultAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=[  'class_roll','position','name','group','section','exam','total','cgpa','grade','absent_at','fail_at','fail_at_without_4th','pass_at','present_at','absent_or_fail_at','absent_or_fail_without_4th','remarks']
    search_fields=['class_roll']
    list_display_links = ['class_roll','name']
    list_filter=[  'group','cgpa','exam','grade','section','fail_at','fail_at_without_4th','absent_at','absent_or_fail_at','absent_or_fail_without_4th','remarks']
