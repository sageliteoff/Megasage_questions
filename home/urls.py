from django.urls import path
from .views import (
    HomeView,
    QuestionsList,
    CollegeProgrammesView,
    ProgrammeCoursesView,
    CourseQuestionsView,
    QuestionDetailsView,
    SearchResultsView,
    DownloadQuestionView,
    DownloadSolutionView)

urlpatterns = [
    path("", HomeView.as_view(), name="home_home" ),
    path("questions", QuestionsList.as_view(), name="home_questions_list"),
    path("question/<int:id>/details",QuestionDetailsView.as_view(),name="home_question_details"),
    path("colleges/<int:id>/programmes",CollegeProgrammesView.as_view(),name="home_college_programmes"),
    path("programmes/<int:id>/courses",ProgrammeCoursesView.as_view(),name="home_programme_courses"),
    path("courses/<str:code>/questions",CourseQuestionsView.as_view(),name="home_course_questions"),
    path("search/results",SearchResultsView.as_view(),name="home_search_results"),
    path("questions/<int:id>/details",QuestionDetailsView.as_view(),name="home_question_details"),
    path("download/questions/<int:id>",DownloadQuestionView.as_view(),name="home_download_question"),
    path("download/solutions/<int:id>",DownloadSolutionView.as_view(),name="home_download_solution"),
]
