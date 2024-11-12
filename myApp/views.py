from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.http import JsonResponse

def index(request):
    context={}
    return render(request, 'myApp/index.html', context)


def subscribe(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')

        # Define the subject
        subject = "Thank you for subscribing!"

        # Render the HTML email template with context
        message_html = render_to_string('myApp/subscribers_email.html', {
            'full_name': full_name
        })

        # Send email with HTML content
        email_message = EmailMessage(
            subject=subject,
            body=message_html,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email]
        )
        email_message.content_subtype = 'html'  # Specify that the email content is HTML
        email_message.send(fail_silently=False)

        # Return a JSON response for AJAX success
        return JsonResponse({"message": "Thank you for subscribing!"})
    
    return JsonResponse({"error": "Invalid request"}, status=400)


from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings

def contact(request):
    if request.method == "POST":
        # Capture form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Construct the email message to the admin
        subject = f"New Contact Form Submission from {name}"
        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        # Send the contact message email to admin or support
        try:
            send_mail(
                subject,
                full_message,
                settings.DEFAULT_FROM_EMAIL,  # From email
                ['feed.teach.love@gmail.com'],  # Replace with admin/support email
                fail_silently=False,
            )
            # Return a JSON response for AJAX success
            response_data = {"message": "Thank you for getting in touch!"}
            print("Success response:", response_data)  # Debug print to verify structure
            return JsonResponse(response_data)

        except Exception as e:
            # In case of an error during email sending, return an error response
            print("Error sending email:", e)  # Log the error for debugging
            return JsonResponse({"error": "Failed to send message. Please try again later."}, status=500)

    # If request method is not POST, return an error
    error_response = {"error": "Invalid request method"}
    print("Error response:", error_response)  # Debug print for non-POST requests
    return JsonResponse(error_response, status=400)
