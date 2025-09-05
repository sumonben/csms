import csv
from django.contrib import admin
from django.contrib import admin
from django.http import HttpResponse
from import_export.admin import ExportActionMixin,ImportExportMixin
from .models import Student,Subject,StudentCategory,Class,Session,Group,Department,Division,District,Upazilla,Union,GuardianInfo,Adress,SubjectChoice,SscEquvalent,Choice,TestSubject
from import_export.admin import ExportActionMixin,ImportExportMixin
from import_export.widgets import ManyToManyWidget,ForeignKeyWidget
from import_export import resources,fields
from django.forms import Field
# Register your models here.
class SubjectResource(resources.ModelResource):
    class Meta:
        model = Subject
        fields = ('name_en', 'name')

class SubjectChoiceResource(resources.ModelResource):
    
    compulsory_subject = fields.Field(
        column_name="Compulsory Subject",
        attribute='compulsory_subject',
        widget=ManyToManyWidget(Subject, field='name_en',separator='|')
    )
    class Meta:
        model = SubjectChoice
        fields = ('serial', 'compulsory_subject')


class StudentResource(resources.ModelResource):
    
    group = fields.Field(
        column_name="Group",
        attribute='group',
        widget=ForeignKeyWidget(Group, field='title_en')
    )
    class Meta:
        model = Student
        


@admin.register(Student)
class StudentAdmin(ImportExportMixin,admin.ModelAdmin):
    search_fields=['email','phone','class_roll']
    list_display=[ 'class_roll','name','email','phone','student_category','department','session','user_link','guardian_info_link','permanent_adress_link','present_adress_link']
    list_display_links = ['name','email']
    list_filter=['department','student_category','session','group','class_year','is_active']
    actions = ("export_as_csv",)
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        header = field_names + ['Subject1','Subject2','Subject3','Subject4','Subject5','Subject6','Fourth Subject',]
        writer.writerow(header)
        for obj in queryset:
            row = [getattr(obj, field) for field in field_names]
            subject_choice=SubjectChoice.objects.filter(student=obj).first()
            for subject in subject_choice.compulsory_subject.all():
                if row:
                    print("Subject_choice:",subject)

                    row.append(subject)
            for subject in subject_choice.optional_subject.all():
                if row:
                    row.append(subject)
            if row:
                row.append(subject_choice.fourth_subject)
            writer.writerow(row)
        return response

    export_as_csv.short_description = "Export Selected student as csv file"

@admin.register(Session)
class StudentSessionAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display=[ 'id','serial','title','title_en']
    list_display_links = ['serial','title']

@admin.register(GuardianInfo)
class GuardianInfoAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display= ['father_name', 'mother_name','guardian_phone']
    list_display_links = ['father_name', 'mother_name','guardian_phone']
    list_filter=['guardian_phone',]
@admin.register(SscEquvalent)
class SscEquvalentAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display= ['id','ssc_exam_roll', 'ssc_or_equvalent','ssc_board']
    list_display_links = ['id', 'ssc_or_equvalent','ssc_board']
    list_filter=['id','ssc_exam_roll', 'ssc_or_equvalent','ssc_board']
@admin.register(SubjectChoice)
class SubjectChoiceAdmin(ImportExportMixin,admin.ModelAdmin):
        list_display=['id','serial','class_roll','student']
        filter_horizontal = ['compulsory_subject','optional_subject']
        search_fields=['class_roll']


@admin.register(Adress)
class AdressAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display=['id','village_or_house','house_or_street_no','division','district','upazilla']
    search_fields=['village_or_house']
    list_filter=['division','district']


@admin.register(StudentCategory)
class StudentCategoryAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display=[ 'id','serial','title','title_en']
    list_display_links = ['serial','title']
    save_as = True


@admin.register(Division)
class DivisionAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display=[ 'id','name','name_en','link']
    list_display_links = ['name','name_en']
@admin.register(District)
class DistrictAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display=[ 'id','name','name_en','division','link']
    list_display_links = ['id','name','name_en']
    list_filter=['division']

@admin.register(Upazilla)
class UpazillaAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display=[ 'id','name','name_en','district','link']
    list_display_links = ['id','name','name_en']
    list_filter=['district']

@admin.register(Union)
class UnionAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display=[ 'id','name','name_en','upazilla','link']
    list_display_links = ['id','name','name_en']
    

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display=[  'id','serial','title_en',]
    list_filter=[  'title_en',]
    list_display_links = ['serial','title_en',]
    
@admin.register(Department)
class UserAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display=[  'serial','name','code','professor', 'associate_professor', 'assistant_professor','lecturer','about']
    list_filter=[  'name','code',]
    list_display_links = ['serial','name','code']

    fieldsets = ((None,{'fields': ('serial','name','name_en','code','about','about_en')}),
        ("পদসংখ্যাঃ", {
           'fields': ('professor', 'associate_professor', 'assistant_professor','lecturer')
        }),
        
    )
@admin.register(TestSubject)
class TestSubjectAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display=[  'id','serial','name','code',]
    list_filter=[  'name','code',]
    list_display_links = ['id','serial','name','code']

@admin.register(Subject)
class SubjectAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display=[  'id','serial','name','code',]
    list_filter=[  'name','code',]
    filter_horizontal = ['group',]
    list_display_links = ['id','serial','name','code']


@admin.register(Choice)
class ChoiceAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display=[  'id','class_roll','subject1','subject2','subject3','subject4','subject5','subject6','fourth_subject','group','session']
    search_fields=['class_roll']
    list_display_links = ['id','class_roll']
    list_filter=[ 'subject1','subject2','subject3','subject4','subject5','subject6','fourth_subject','group','session']

   

