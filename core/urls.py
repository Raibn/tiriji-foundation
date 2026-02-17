from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('children/', views.children, name='children'),
    path('women/', views.women, name='women'),
    path('volunteer/', views.volunteer, name='volunteer'),
    path('programs/', views.programs, name='programs'),
    path('programs/<int:program_id>/', views.program_detail, name='program_detail'),
    path('volunteer/signup/', views.volunteer_signup, name='volunteer_signup'),
    path('donate/', views.donate, name='donate'),
    path('events/', views.events, name='events'),
    path('news/', views.news, name='news'),
    path('resources/', views.resources, name='resources'),
    path('faq/', views.faq, name='faq'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('gallery/', views.gallery, name='gallery'),
    path('team/', views.team, name='team'), 
    path('partners/', views.partners, name='partners'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('careers/', views.careers, name='careers'),
    path('careers/<int:career_id>/', views.career_detail, name='career_detail'),
    path('donate/success/', views.donate_success, name='donate_success'),
    path('feedback/', views.feedback, name='feedback'),
    path('feedback/success/', views.feedback_success, name='feedback_success'), 

    
    
]
