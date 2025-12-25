
from django.urls import path
from . import views

urlpatterns = [

path('', views.index, name='index'),
path('phrase-practice/', views.phrase_practice, name='phrase_practice'),
path('phrase-practice/<int:scenario_id>/', views.phrase_practice_scenario, name='phrase_practice_scenario'),
path('select/', views.select_level_and_scenario, name='select_level_and_scenario'),
path('chat/<int:scenario_id>/start/', views.start_chat, name='start_chat'),
path('chat/<int:scenario_id>/continue/', views.continue_chat, name='continue_chat'),
path('chat/<int:scenario_id>/end/', views.end_chat, name='end_chat'),
path ("conversation/<int:scenario_id>/end/",views.end_conversation,name="end_conversation",
)
]