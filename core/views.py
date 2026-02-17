from django.shortcuts import render
from .models import Program, Volunteer

def home(request):
    programs = Program.objects.all()
    return render(request, 'core/home.html', {'programs': programs})

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def children(request):
    return render(request, 'core/children.html')

def women(request):
    return render(request, 'core/women.html')   


def volunteer(request):
    return render(request, 'core/volunteer.html')

def programs(request):
    programs = Program.objects.all()
    return render(request, 'core/programs.html', {'programs': programs})

def program_detail(request, program_id):
    program = Program.objects.get(id=program_id)
    return render(request, 'core/program_detail.html', {'program': program})

def volunteer_signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Save volunteer information to the database
        Volunteer.objects.create(name=name, email=email, message=message)

        return render(request, 'core/volunteer_success.html', {'name': name})
    return render(request, 'core/volunteer_signup.html')

def donate(request):
    return render(request, 'core/donate.html') 

def events(request):
    return render(request, 'core/events.html')  

def news(request):
    return render(request, 'core/news.html')

def resources(request):
    return render(request, 'core/resources.html')

def faq(request):
    return render(request, 'core/faq.html')

def testimonials(request):
    return render(request, 'core/testimonials.html')

def gallery(request):
    return render(request, 'core/gallery.html')

def team(request):
    return render(request, 'core/team.html')

def partners(request):
    return render(request, 'core/partners.html')

def careers(request):
    return render(request, 'core/careers.html')

def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')

def terms_of_service(request):
    return render(request, 'core/terms_of_service.html')

def support(request):
    return render(request, 'core/support.html')

def sitemap(request):
    return render(request, 'core/sitemap.html')

def feedback(request):
    return render(request, 'core/feedback.html')

def newsletter(request):
    return render(request, 'core/newsletter.html')

def donate_success(request):
    return render(request, 'core/donate_success.html')

def donate_cancel(request):
    return render(request, 'core/donate_cancel.html')

def event_detail(request, event_id):
    # Placeholder for event detail view
    return render(request, 'core/event_detail.html', {'event_id': event_id})

def news_detail(request, news_id):
    # Placeholder for news detail view
    return render(request, 'core/news_detail.html', {'news_id': news_id})   

def resource_detail(request, resource_id):
    # Placeholder for resource detail view
    return render(request, 'core/resource_detail.html', {'resource_id': resource_id})

def testimonial_detail(request, testimonial_id):
    # Placeholder for testimonial detail view
    return render(request, 'core/testimonial_detail.html', {'testimonial_id': testimonial_id})

def gallery_detail(request, gallery_id):
    # Placeholder for gallery detail view
    return render(request, 'core/gallery_detail.html', {'gallery_id': gallery_id})  

def team_member_detail(request, member_id):
    # Placeholder for team member detail view
    return render(request, 'core/team_member_detail.html', {'member_id': member_id})

def partner_detail(request, partner_id):
    # Placeholder for partner detail view
    return render(request, 'core/partner_detail.html', {'partner_id': partner_id})

def career_detail(request, career_id):
    # Placeholder for career detail view
    return render(request, 'core/career_detail.html', {'career_id': career_id})

def blog(request):
    return render(request, 'core/blog.html')

def blog_detail(request, blog_id):
    # Placeholder for blog detail view
    return render(request, 'core/blog_detail.html', {'blog_id': blog_id})

def feedback_success(request):
    return render(request, 'core/feedback_success.html')
 