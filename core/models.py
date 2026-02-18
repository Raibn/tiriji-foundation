from django.db import models

class Program(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='programs/')
class program(models.Model):
    program_id = models.IntegerField(primary_key=True, db_index=True)
    title = models.CharField(max_length=50, null=False, blank=False)
    program_description = models.TextField()
    image_url = models.URLField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Volunteer(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    def __str__(self):
        return f"{self.first_name} {self.last_name} registered for {self.program_id.title} program that starts on {self.start_date} and ends on {self.end_date}"


class events(models.Model):
    event_id = models.IntegerField(primary_key=True, db_index=True)
    title = models.CharField(max_length=50, null=False, blank=False)
    events_description = models.TextField()
    image_url = models.URLField(max_length=250, null=True, blank=True)
    program_id = models.ForeignKey(program, on_delete=models.CASCADE, null=True, blank=True, related_name='events')
    event_location = models.CharField(max_length=100)
    event_date = models.DateField()

    def __str__(self):
        return f"{self.title} event scheduled for {self.event_date} at {self.location} under {self.program_id.title} program"


class news(models.Model):
    news_id = models.IntegerField(primary_key=True, db_index=True)
    title = models.CharField(max_length=50, null=False, blank=False)
    news_description = models.TextField()
    image_url = models.URLField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    program_id = models.ForeignKey(program, on_delete=models.CASCADE, null=True, blank=True, related_name='news')
    event_id = models.ForeignKey(events, on_delete=models.CASCADE, null=True, blank=True, related_name='news')

    def __str__(self):
        if self.program_id and self.event_id:
            return f"{self.title} news related to {self.program_id.title} program and {self.event_id.title} event"
        elif self.program_id:
            return f"{self.title} news related to {self.program_id.title} program"
        elif self.event_id:
            return f"{self.title} news related to {self.event_id.title} event"
        else:
            return self.title

class resources(models.Model):
    resource_id = models.IntegerField(primary_key=True, db_index=True)
    title = models.CharField(max_length=50, null=False, blank=False)
    resources_description = models.TextField()
    image_url = models.URLField(max_length=250, null=True, blank=True)
    file_url = models.URLField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    program_id = models.ForeignKey(program, on_delete=models.CASCADE, null=True, blank=True, related_name='resources')

    def __str__(self):
        return f"{self.title} resource related to {self.program_id.title} program"


class employees(models.Model):
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(unique=True, primary_key=True)
    role = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    id_pass_no = models.CharField(max_length=50, verbose_name="ID/Passport No")
    starting_date = models.DateField(auto_now_add=True)
    residence = models.CharField(max_length=100)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=20)
    bio = models.TextField()
    profile_image_url = models.URLField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"


class patners(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    patners_description = models.TextField()
    profile_logo_url = models.URLField(max_length=250, null=True, blank=True)
    website_url = models.URLField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_employee = models.ForeignKey(employees, on_delete=models.SET_NULL, null=True, blank=True, related_name='patners')  
    program_id = models.ForeignKey(program, on_delete=models.CASCADE, null=True, blank=True, related_name='patners')

    def __str__(self):
        if self.assigned_employee:
            return f"{self.name} patner related to {self.program_id.title} program and assigned to {self.assigned_employee.first_name} {self.assigned_employee.last_name}" 
        else:
            return f"{self.name} patner related to {self.program_id.title} program"


class gallery(models.Model):
    image_id = models.IntegerField(primary_key=True, db_index=True)
    title = models.CharField(max_length=50, null=False, blank=False)
    image_description = models.TextField()
    image_url = models.URLField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    program_id = models.ForeignKey(program, on_delete=models.CASCADE, null=True, blank=True, related_name='program_gallery')
    event_id = models.ForeignKey(event, on_delete=models.CASCADE, null=True, blank=True, related_name='event_gallery')

    def __str__(self):
        if self.program_id and self.event_id:
            return f"{self.title} image related to {self.program_id.title} program and {self.event_id.title} event"
        elif self.program_id:
            return f"{self.title} image related to {self.program_id.title} program"
        elif self.event_id:
            return f"{self.title} image related to {self.event_id.title} event"
        else:
            return self.title    


class donations(models.Model):
    donations_id  = models.CharField(max_length=50, primary_key=True)
    merchant_reference_id = models.CharField(max_length=100, null=False, blank=False)
    pesapal_transaction_id = models.CharField(max_length=100, null=False, blank=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    status = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=50)
    donation_reason = models.CharField(max_length=255, null=True, blank=True)
    donor_email = models.EmailField(null=True, blank=True)
    donor_phone_number = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Donation {self.donations_id} of {self.amount} {self.currency} via {self.payment_method} with status {self.status}"


class feedback(models.Model):
    feedback_id = models.IntegerField(primary_key=True, db_index=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

######### Additional models for expanded functionality #########
    
class Career(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class News(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    published_at = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    image = models.ImageField(upload_to='resources/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    
class Testimonial(models.Model):
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=100, blank=True)  # e.g., Volunteer, Beneficiary
    message = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class TeamMember(models.Model):
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='team/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Partner(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='partners/', blank=True, null=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class Gallery(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
# D   
class Donation(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ${self.amount}"
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField(blank=True, null=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.event.title}"
    
class Career(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class JobApplication(models.Model):
    career = models.ForeignKey(Career, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    email = models.EmailField()
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.career.title}"
    
class Feedback(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
    
class SitemapEntry(models.Model):
    url = models.URLField()
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url

class SupportRequest(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"  
    
class TermsOfService(models.Model):
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Terms of Service - Last Updated: {self.updated_at.strftime('%Y-%m-%d')}"       

class PrivacyPolicy(models.Model):
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Privacy Policy - Last Updated: {self.updated_at.strftime('%Y-%m-%d')}"
class CookieConsent(models.Model):
    user_email = models.EmailField()
    consent_given = models.BooleanField(default=False)
    consent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_email} - Consent Given: {self.consent_given}"
    
class AccessibilityFeedback(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

class VolunteerOpportunity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title   
    
class PartnershipInquiry(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    organization = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.organization}" 

class EventFeedback(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    email = models.EmailField()
    rating = models.IntegerField()
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.event.title} - Rating: {self.rating}"
    
class DonationFeedback(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ${self.amount}"
    
class NewsletterFeedback(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

class ContactInquiry(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
    
class VolunteerSignup(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField(blank=True, null=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.event.title}"      

class JobApplication(models.Model):
    career = models.ForeignKey(Career, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    email = models.EmailField()
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.career.title}"     
    
class Feedback(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"    
    