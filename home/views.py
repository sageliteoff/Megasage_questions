import os
from . import models
from django.urls import reverse
from django.shortcuts import render_to_response
from django.utils import timezone
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic import TemplateView, View
from userprofile.models import UserProfile
from django.contrib import messages
from utils.error_messages import errorMessage
from utils.exceptions import *
from .forms import SearchForm
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from allauth.account.decorators import login_required


class HomeView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = models.Question.objects.filter(published=True)
        context["recent_questions"] = questions.order_by("-pub_date")[:10]
        context["search_form"]  = SearchForm()
        return context


class AboutView(TemplateView):
    template_name = "home/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = models.Question.objects.filter(published=True)
        context["recent_questions"] = questions.order_by("-pub_date")[:10] 
        return context


class QuestionsList(TemplateView):
    template_name = "home/questions_list.html"

    def get_context_data(self, **kwargs):
        context = super(QuestionsList, self).get_context_data(**kwargs)
        questions = models.Question.objects.all().order_by("-pub_date")
        paginator = Paginator(questions, 10)
        context["questions"] = paginator.get_page(kwargs["page"])
        context["search_form"]  = SearchForm()
        return context
    

class QuestionDetailsView(TemplateView):
    template_name = "home/question_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = models.Question.objects.get(id=kwargs["id"])
        context["question"] = question
        # SELECT * FROM course_table WHERE code = question.code
        course = models.Course.objects.get(code=question.course.code)
        # Get all the questions of the selected course excluding the current question
        related_questions = course.question_set.exclude(id=question.id)
        # take the first six questions3

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
        # FROM programme_table SELECT * WHERE id = "the id in the url"
        context["programme"] = models.Programme.objects.get(id=kwargs["id"])
        # SELECT course WHERE level=100 and programme = "the id in the url"
        context["level_100_courses"] = models.Course.objects.filter(level="100",programme=kwargs["id"])
        context["level_200_courses"] = models.Course.objects.filter(level="200",programme=kwargs["id"])
        context["level_300_courses"] = models.Course.objects.filter(level="300",programme=kwargs["id"])
        context["level_400_courses"] = models.Course.objects.filter(level="400",programme=kwargs["id"])
        return context


class CourseQuestionsView(TemplateView):
    template_name = "home/course_questions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the all question under the course
        context["course_title"] =  models.Course.objects.get(code=kwargs["code"]).title
        context["questions"] = models.Course.objects.get(code=kwargs["code"]).question_set.all()
        return context


class SearchResultsView(TemplateView):
    template_name = "home/search_results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the all question under the course
        form = SearchForm(self.request.GET)
        if form.is_valid():
            user_input = form.cleaned_data["searchInput"].upper()
            splitted_user_input = user_input.split(" ")
            try:
                # get all courses starting with the first word splitted input
                courses = models.Course.objects.filter(code__istartswith=splitted_user_input[0])
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


def makeVerifcations(request, kwargs):
     #Login required
    if not request.user.is_authenticated:
        raise LoginRequired(errorMessage["LR"])

    try:
        # Get the current user UserProfile
        userProfile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist as e:
        raise  SubscriptionPackageRequired(errorMessage["SPR"])

    # check whether user has a subscription package
    if not userProfile.subscription_package:
        raise SubscriptionPackageRequired(errorMessage["SPR"])

    # check whether the subscription expiration_date has reached
    if userProfile.calc_expiration_date() < timezone.now():
        userProfile.subscription_package = None
        userProfile.save()
        raise SubscriptionPackageExpired(errorMessage["SPX"])

    # if user is on free subscription but trying to download a Premium question
    q = models.Question.objects.get(pk = kwargs["id"])
    if q.question_type.upper() != "FREE" and userProfile.subscription_package.name.upper() == "FREE":
        raise PremiumUsersOnly(errorMessage["PUO"])

    # check if user has  some downloads left
    if  userProfile.calc_downloads_left() < 1:
            raise NodownloadsLeft(errorMessage["NDL"])

  
class DownloadQuestionView(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponseRedirect(reverse("home_question_details", args=[kwargs["id"]]))
        try:
            makeVerifcations(self.request, kwargs)
            context = {
                "question": models.Question.objects.get(pk=kwargs["id"])
            }
            # Get the current user UserProfile
            userProfile = UserProfile.objects.get(user=request.user)
            userProfile.total_downloads += 1
            userProfile.save()
            return render_to_response("home/question_content.html",context)
        except LoginRequired:
            messages.add_message(self.request, messages.ERROR, errorMessage["LR"])
            return response
        except SubscriptionPackageRequired:
            messages.add_message(self.request, messages.ERROR, errorMessage["SPR"])
            return response
        except SubscriptionPackageExpired:
            messages.add_message(self.request, messages.ERROR, errorMessage["SPX"])
            return response
        except PremiumUsersOnly:
            messages.add_message(self.request, messages.ERROR, errorMessage["PUO"])
            return response
        except NodownloadsLeft:
            messages.add_message(self.request, messages.ERROR, errorMessage["NDL"])
            return response


class DownloadSolutionView(View):
    pass

