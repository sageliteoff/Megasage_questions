from django.urls import path
from .views import (
    HomeView,
    CollegeProgrammesView,
    ProgrammeCoursesView,
    CourseQuestionsView,
    QuestionDetailsView,
    SearchResultsView,
    QuestionsDowloadView,
    SolutionsDowloadView,
    DownloadQuestionView,
    DownloadSolutionView)

urlpatterns = [
    path("", HomeView.as_view(), name="home_home" ),
    path("question/<int:id>/details",QuestionDetailsView.as_view(),name="home_question_details"),
    path("colleges/<int:id>/programmes",CollegeProgrammesView.as_view(),name="home_college_programmes"),
    path("programmes/<int:id>/courses",ProgrammeCoursesView.as_view(),name="home_programme_courses"),
    path("courses/<str:code>/questions",CourseQuestionsView.as_view(),name="home_course_questions"),
    path("search/results",SearchResultsView.as_view(),name="home_search_results"),
    path("questions/<int:id>/details",QuestionDetailsView.as_view(),name="home_question_details"),
    path("download/questions/<int:id>",DownloadQuestionView.as_view(),name="home_download_question"),
    path("download/solutions/<int:id>",DownloadSolutionView.as_view(),name="home_download_solution"),
    path("files/QUESTIONS/<str:code>/<str:year>/<str:filename>",QuestionsDowloadView.as_view(),name="home_get_solution"),
    path("files/SOLUTIONS/<str:code>/<str:year>/<str:filename>",SolutionsDowloadView.as_view(),name="home_get_solution"),
]
