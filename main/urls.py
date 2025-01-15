from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('create_test', views.create_test, name='create_test'),
    path('ready_tests', views.ready_tests, name='ready_tests'),
    path('support', views.support, name='support'),
    path('download/<str:filename>/', views.download_test_file, name='download_test_file'),
    path('ready_tests/<int:test_id>/', views.test_detail, name='ready_test_detail'),
    path('save_test/', views.save_test, name='save_test'),
    path('submit-quiz/', views.submit_quiz, name='submit_quiz'),
    path('download-questions/<int:test_id>/', views.download_questions, name='download_questions'),
    path('download-answers/<int:test_id>/', views.download_answers, name='download_answers'),
]
