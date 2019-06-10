from django.contrib import admin
from . import models

class QuestionAdmin(admin.ModelAdmin):
    singular_message_bit = "1 questions was"
    plural_message_bit = "{} questions were"
    def mark_selected_as_published(self, request, queryset):
        rows_updated = queryset.update(published=True)
        if rows_updated == 1:
            message_bit = self.singular_message_bit
        else:
            message_bit = self.plural_message_bit.format(rows_updated)
        self.message_user(request, "%s successfully marked as published." % message_bit)

    def mark_selected_as_unpublished(self, request, queryset):
        rows_updated = queryset.update(published=False)
        if rows_updated == 1:
            message_bit = self.singular_message_bit
        else:
            message_bit = self.plural_message_bit.format(rows_updated)
        self.message_user(request, "{} successfully marked as unpublished.".format(message_bit))

    list_display = ("get_course_code", "quiz_number", "question_type", "pub_date", "published")
    list_filter = ["published", "pub_date", "question_type", "course"]
    actions = [
                "mark_selected_as_published",
                "mark_selected_as_unpublished"
            ]
    fieldsets = [
                    ("detail", {"fields": [
                                    "course",
                                    "date",
                                    "question_type",
                                    "quiz_number",
                                    "pub_date",
                                    "published"]}),
                    ("question files", {"fields": [
                                        "question_file",
                                        "solution_file"
                                            ]}),
                    ("question", {"fields": [
                                    "page1",
                                    "page2",
                                    "page3",
                                    "page4"]})
                ]


class CollegeAdmin(admin.ModelAdmin):
    list_display = ["id","name"]
class CourseAdmin(admin.ModelAdmin):
    list_display = ["code","title","id"]

admin.site.register(models.College,CollegeAdmin)
admin.site.register(models.Programme)
admin.site.register(models.Course,CourseAdmin)
admin.site.register(models.Question,QuestionAdmin)
