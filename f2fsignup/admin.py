import csv
from copy import copy

from django.conf import settings
from django.contrib import admin
from django.forms.models import model_to_dict
from django.http import HttpResponse

from models import Group, Member, F2FSettings, ImportFile, Ministry


def export_members_action(modeladmin, request, queryset):
    """

    Exports the selected members into a csv file. The browser will prompt for download.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = "attachment; filename=f2fmembers.csv"
    writer = csv.DictWriter(response, settings.EXPORT_FIELDS, dialect=csv.excel)
    writer.writeheader()
    for member in queryset:
        row = copy(model_to_dict(member))
        for field in [x for x in row if x not in settings.EXPORT_FIELDS]:
            del row[field]
        row['group'] = member.group
        writer.writerow(row)
    return response


export_members_action.short_description = 'Export selected members to csv file'


class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'registrant_count']
    ordering = ('name',)


class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'ministry', 'group', 'added']
    list_filter = ('group', 'ministry')
    search_fields = ['^first_name', '^last_name']
    readonly_fields = ('added',)
    actions = [export_members_action]


class F2FSettingsAdmin(admin.ModelAdmin):
    list_display = ['attribute', 'value']


class MinistryAdmin(admin.ModelAdmin):
    list_display = ['name', 'limit']


admin.site.site_header = 'Central Baptist Church'
admin.site.site_title = 'Central Baptist Church'

admin.site.register(Group, GroupAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(F2FSettings, F2FSettingsAdmin)
admin.site.register(Ministry, MinistryAdmin)
admin.site.register(ImportFile)
