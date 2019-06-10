from django.db import models
import datetime
from django.utils import timezone
from django.urls import reverse
from tinymce.models import HTMLField

class College(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name

class Programme(models.Model):
    college = models.ForeignKey(College,on_delete=models.CASCADE)
    title = models.CharField(unique=True,max_length=100)
    def __str__(self):
        return self.title

class Course(models.Model):
    programme = models.ManyToManyField(Programme)
    title = models.CharField(unique=True,max_length=100)
    code = models.CharField(unique=True,max_length=10)
    #level 100 or 200 or 300 ....
    LEVEL_CHOICES = [("100","100"),("200","200"),("300","300"),("400","400")]
    level = models.CharField(max_length=4,choices =LEVEL_CHOICES, blank=True)

    def __str__(self):
        return "{0} {1}".format(self.title, self.code)

class Question(models.Model):

    def question_directory_path(instance, filename):
        #path eg---> QUESTIONS/EMG102/2015/quiz.pdf
        code = instance.course.code
        date = instance.date.year
        filename = "{0}_{1}".format(instance.quiz_number,filename)
        return "QUESTIONS/{0}/{1}/{2}".format(code,date,filename)

    def solution_directory_path(instance, filename):
        #path eg---> SOLUTIONS/EMG102/2015/quiz.pdf
        code = instance.course.code
        date = instance.date.year
        filename = "{0}_{1}".format(instance.quiz_number,filename)
        return "SOLUTIONS/{0}/{1}/{2}".format(code,date,filename)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    number_of_downloads = models.IntegerField(default=0)
    date = models.DateTimeField()
    pub_date = models.DateField(default=timezone.now)
    published = models.BooleanField(default=False)
    QUESTION_TYPE_CHOICES = [("Free","Free"),("premium","Premium"),("Others","others")]
    question_type = models.CharField(choices=QUESTION_TYPE_CHOICES,max_length=10)
    QUIZ_NUMBER = [("quiz 1"," quiz 1"),("quiz 2","quiz 2"),("exams","examination"),("supplementary","supplementary")]
    quiz_number = models.CharField(choices=QUIZ_NUMBER,max_length=10)
    question_file = models.FileField(upload_to=question_directory_path,blank=True)
    solution_file = models.FileField(upload_to=solution_directory_path,blank=True)
    page1 = HTMLField(blank=True)
    page2 = HTMLField(blank=True)
    page3 = HTMLField(blank=True)
    page4 = HTMLField(blank=True)


    def get_course_code(self):
        return self.course.code


    def __str__(self):
        name ="{}-question-{}-{}".format(self.course.code,self.quiz_number,self.date.year)
        return name
