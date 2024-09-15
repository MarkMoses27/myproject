from django.http import JsonResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import json
import os
import logging

logger = logging.getLogger(__name__)

@csrf_exempt  # Consider enabling CSRF protection in production
def booking_form(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)

            # Extract data sent from React form
            name = data.get('name')
            email = data.get('email')
            subject = data.get('subject', 'Booking Request')  # Default subject if not provided
            message = data.get('message')
            services = data.get('services', [])

            # Validate required fields and data format
            if not all([name, email, message]) or not isinstance(services, list):
                return JsonResponse({'error': 'Missing required fields or invalid data format'}, status=400)

            # Validate email format
            try:
                validate_email(email)
            except ValidationError:
                return JsonResponse({'error': 'Invalid email address'}, status=400)

            # Send email to the admin
            admin_email = os.getenv('ADMIN_EMAIL', 'your_admin_email@example.com')  # Default admin email
            admin_message = f"Booking request from {name} ({email})\n\nServices: {', '.join(services)}\nMessage: {message}"

            send_mail(
                subject=f'New Booking: {subject}',
                message=admin_message,
                from_email=email,
                recipient_list=[admin_email],
                fail_silently=False,
            )

            # Send confirmation email to the client
            client_message = f"Dear {name},\n\nThank you for booking the following services:\n{', '.join(services)}\n\nWe will contact you shortly."
            send_mail(
                subject='Booking Confirmation',
                message=client_message,
                from_email=admin_email,
                recipient_list=[email],
                fail_silently=False,
            )

            return JsonResponse({'message': 'Booking successful!'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            logger.error(f"Error during booking: {str(e)}")  # Log the error for debugging
            return JsonResponse({'error': 'An error occurred. Please try again later.'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
