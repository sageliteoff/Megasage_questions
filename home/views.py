import os
from . import models
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.views.generic import TemplateView, View
from django.utils.decorators import method_decorator
from allauth.account.decorators import login_required
from userprofile.models import UserProfile
from django.contrib import messages
from .forms import SearchForm


class HomeView(TemplateView):
    template_name = "home/home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = models.Question.objects.filter(published=True)
        context["recent_questions"] = questions.order_by("-pub_date")
        context["search_form"]  = SearchForm()
        return context

class QuestionDetailsView(TemplateView):
    template_name = "home/question_details.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question =  models.Question.objects.get(id=kwargs["id"])
        context["question"] = question
        #SELECT * FROM course_table WHERE code = question.code
        course = models.Course.objects.get(code=question.course.code)
        #Get all the questions of the selected course excluding the currrent question
        related_questions = course.question_set.exclude(id=question.id)
        #take the first six questions3

        context["related_questions"] = related_questions[:6]

        return context

class CollegeProgrammesView(TemplateView):
    template_name = "home/college_programmes.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["college_name"] = models.College.objects.get(id=kwargs["id"])
        context["programmes"] = models.Programme.objects.filter(college=kwargs["id"])
        return context

class ProgrammeCoursesView(TemplateView):
    template_name = "home/programme_courses.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #FROM programme_table SELECT * WHERE id = "the id in the url"
        context["programme"] = models.Programme.objects.get(id=kwargs["id"])
        #SELECT course WHERE level=100 and programme = "the id in the url"
        context["level_100_courses"] = models.Course.objects.filter(level="100",programme=kwargs["id"])
        context["level_200_courses"] = models.Course.objects.filter(level="200",programme=kwargs["id"])
        context["level_300_courses"] = models.Course.objects.filter(level="300",programme=kwargs["id"])
        context["level_400_courses"] = models.Course.objects.filter(level="400",programme=kwargs["id"])
        return context

class CourseQuestionsView(TemplateView):
    template_name = "home/course_questions.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #Get the all question under the course
        context["course_title"] =  models.Course.objects.get(code=kwargs["code"]).title
        context["questions"] = models.Course.objects.get(code=kwargs["code"]).question_set.all()
        return context

class SearchResultsView(TemplateView):
    template_name = "home/search_results.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #Get the all question under the course
        form = SearchForm(self.request.GET)
        if form.is_valid():
            userInput = form.cleaned_data["searchInput"].upper()
            splitted_userInput = userInput.split(" ")
            try:
                #get all courses starting with the first word splitted input
                courses = models.Course.objects.filter(code__istartswith=splitted_userInput[0])
                questions = []
                for c in courses:
                    questions += (c.question_set.all())
                print(questions)
                context["questions"] = questions
            except models.Course.DoesNotExist as e:
                raise
            except IndexError as e:
                context["questions"] = courses.question_set.all()
        return context


errorMessage = {
    "SPR": "SUBSCRIPTION_PACKAGE_REQUIRED",
    "SPX": "SUBSCRIPTION_PACKAGE_REQUIRED_HAS_EXPIRED",
    "LR" : "LOGIN_REQUIRED",
    "NDL": "NO_DOWNLOADS_LEFT",
    "PUO": "PREMIUM_USERS_ONLY",
}

#handles download from site
class DownloadQuestionView(View):
    def get(self, request,*args, **kwargs):
        response = HttpResponseRedirect(reverse("home_question_details",args=[kwargs["id"]]))
        if self.request.user.is_authenticated:
            try:
                # Get the current user UserProfile
                userProfile = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist as e:
                messages.add_message(self.request, messages.ERROR,  errorMessage["SPR"])
                return response

            #check whether user has a subscription package
            if not userProfile.subscription_package:
                messages.add_message(self.request, messages.ERROR, errorMessage["SPR"])
                return response

            #check whether the subscription expiration_date has reached
            if userProfile.calc_expiration_date() < timezone.now():
                userProfile.subscription_package = None
                userProfile.save()
                messages.add_message(self.request, messages.ERROR, "SPX")
                return response


            #Get the question selected
            q = models.Question.objects.get(pk = kwargs["id"])


            #if user is on free subscription but trying to download a Premium question
            if q.question_type.upper() != "FREE" and userProfile.subscription_package.name.upper() == "FREE":
                messages.add_message(self.request,messages.ERROR,errorMessage["PUO"])
                return response

            # check if user has  some downloads left
            if  userProfile.calc_downloads_left() < 1:
                messages.add_message(self.request,messages.ERROR,errorMessage["NDL"])
                return response

            with open(q.question_file.path,"rb") as f:
                response = HttpResponse(f.read())
                response["content_type"] = "application/pdf"
                response["Content-Disposition"] = "attachment; filename={0}".format(q.question_file.name)
            q.number_of_downloads += 1

            #increase the user tital number of download if the question a premium
            if q.question_type.upper() != "FREE":
                userProfile.total_downloads +=1
                userProfile.save()

            return response

        messages.add_message(self.request, messages.ERROR,  errorMessage["LR"])
        return response


class DownloadSolutionView(View):
    def get(self, request,*args, **kwargs):
        if not self.request.user.is_anonymous:
            q = models.Question.objects.get(pk = kwargs["id"])
            with open(q.solution_file.path,"rb") as f:
                response = HttpResponse(f.read())
                response["content_type"] = "application/pdf"
                response["Content-Disposition"] = "attachment; filename={0}".format(q.solution_file.name)
                return response
        return JsonResponse({"user":"anonymous"})

# handles download from admin sites
@method_decorator(login_required,name="dispatch")
class QuestionsDowloadView(View):
    def get(self, request,*args, **kwargs):
        #generate question file absolute path => Question/code/year/filename
        filename = os.path.join("QUESTIONS",kwargs["code"],kwargs["year"],kwargs["filename"]).replace("\\","/")
        # get question using the generated absolute path
        q = models.Question.objects.get(question_file = filename)
        #open the question_file of the question and server it as attachment
        with open(q.question_file.path,"rb") as f:
            response = HttpResponse(f.read())
            response["content_type"] = "application/pdf"
            response["Content-Disposition"] = "attachment; filename={0}".format(q.question_file.name)
        return response

@method_decorator(login_required,name="dispatch")
class SolutionsDowloadView(View):
    def get(self, request,*args, **kwargs):
        filename = os.path.join("SOLUTIONS",kwargs["code"],kwargs["year"],kwargs["filename"]).replace("\\","/")
        q = models.Question.objects.get(solution_file = filename)
        with open(q.solution_file.path,"rb") as f:
            response = HttpResponse(f.read())
            response["content_type"] = "application/pdf"
            response["Content-Disposition"] = "attachment; filename={0}".format(q.solution_file.name)
        return response
