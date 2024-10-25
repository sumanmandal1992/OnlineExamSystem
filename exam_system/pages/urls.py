from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='IndexPage'),
    path('exam/', views.get_std_login_info, name='ExamLoginInfo'),
    path('exam/qns/', views.exam_qns_and_save_next, name='ExamQnsViewSave'),
    path('exam/qns/saveprev/', views.qns_save_preview, name='ExamQnsSavePrev'),
    path('exam/qns/savejump/', views.qns_save_jump, name='ExamQnsSaveJump'),
    path('exam/secure/', views.secure_exam_form, name='SecureExam'),
    path('exam/qns/submit/', views.submit_exam, name='SubmitExam'),
    path('super/', views.get_admin_info, name='AdmnInfo'),
    path('super/upload/', views.admin_panel, name='AdminPanel'),
    path('super/upload/stddb/', views.upload_std_db_file, name='StdDb'),
    path('super/upload/qnsdb/', views.upload_qns_db_file, name='QnsDb'),
]
