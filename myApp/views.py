# myApp/views.py
from django.shortcuts import render, get_object_or_404  # Import get_object_or_404 here
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Attendee, Attendance

def scan_qr_code(request):
    return render(request, 'myApp/scan.html')

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Attendee, Attendance
@csrf_exempt
def log_attendance(request):
    if request.method == "POST":
        qr_data = request.POST.get("qr_data")
        print(f"QR Data: {qr_data}")  # Debug print statement
        
        try:
            attendee_id, _ = qr_data.split("-")
            print(f"Attendee ID: {attendee_id}")  # Debug print statement

            attendee = Attendee.objects.get(id=attendee_id)

            # Check if the attendee has already marked attendance today
            existing_attendance = Attendance.objects.filter(attendee=attendee, scanned_at__date=timezone.now().date()).first()

            if existing_attendance:
                return JsonResponse({"status": "error", "message": f"Attendee {attendee.first_name} {attendee.last_name} is already marked as present today."})
            
            # Create the attendance record
            Attendance.objects.create(attendee=attendee)
            
            return JsonResponse({"status": "success", "message": f"Attendance logged for {attendee.first_name} {attendee.last_name}"})
        
        except ValueError:
            return JsonResponse({"status": "error", "message": "Invalid QR data format."})
        except Attendee.DoesNotExist:
            return JsonResponse({"status": "error", "message": "No QR code attendee on record."})

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)




from django.shortcuts import render, redirect
from .forms import AttendeeRegistrationForm
from .models import Attendee

def register_attendee(request):
    if request.method == "POST":
        form = AttendeeRegistrationForm(request.POST)
        if form.is_valid():
            attendee = form.save()  # Save attendee data to the database
            return redirect('generate_qr', attendee_id=attendee.id)  # Redirect to QR generation page
    else:
        form = AttendeeRegistrationForm()
    
    return render(request, 'myApp/register_attendee.html', {'form': form})


# myApp/views.py
import qrcode
from django.shortcuts import render, get_object_or_404
from django.conf import settings
import os
from .models import Attendee

def generate_qr(request, attendee_id):
    attendee = get_object_or_404(Attendee, id=attendee_id)
    qr_data = f"{attendee.id}-{attendee.email}"  # Unique data for each attendee

    # Generate QR code
    qr = qrcode.make(qr_data)
    
    # Define the path to save QR codes in the 'assets/qr_codes' directory
    qr_filename = f"qr_{attendee.id}.png"
    qr_path = os.path.join(settings.BASE_DIR, 'myApp', 'static', 'assets', 'qr_codes', qr_filename)
    os.makedirs(os.path.dirname(qr_path), exist_ok=True)  # Create directory if it doesn't exist
    qr.save(qr_path)

    # URL for the QR code image to be accessed in templates
    qr_url = f"/static/assets/qr_codes/{qr_filename}"

    return render(request, 'myApp/display_qr.html', {'attendee': attendee, 'qr_url': qr_url})



# myApp/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'myApp/index.html')


# myApp/views.py
from django.shortcuts import render
from .models import Attendee

def list_attendees(request):
    attendees = Attendee.objects.all()
    return render(request, 'myApp/list_attendees.html', {'attendees': attendees})



from django.shortcuts import render
from django.utils import timezone
from pytz import timezone as pytz_timezone
from .models import Attendee, Attendance

def attendance_table(request):
    # Define the start date of the event and the three event days
    event_start_date = timezone.datetime(2024, 11, 12, tzinfo=timezone.get_current_timezone())  # Ensure the date is timezone-aware
    event_days = [event_start_date + timezone.timedelta(days=i) for i in range(3)]
    
    # Get all attendees
    attendees = Attendee.objects.all()
    
    # Prepare attendance data for each attendee and each day
    attendance_data = []
    today = timezone.now().date()  # Get today's date
    
    manila_tz = pytz_timezone('Asia/Manila')  # Manila Time (PST)
    
    for attendee in attendees:
        # Concatenate first name and last name
        full_name = f"{attendee.first_name} {attendee.last_name if attendee.last_name else ''}"
        
        row = {'name': full_name}
        
        for i, day in enumerate(event_days, start=1):
            # Ensure the event day is timezone-aware if you're using timezone-aware datetimes
            event_day = timezone.make_aware(day) if not day.tzinfo else day
            
            # Check if the day has already passed
            if event_day.date() <= today:
                # If the event day has passed, check for attendance
                attendance_record = Attendance.objects.filter(
                    attendee=attendee,
                    scanned_at__date=event_day.date()  # Compare only the date part
                ).first()
                
                if attendance_record:
                    # Convert the scan time to Manila Time (PST)
                    manila_time = attendance_record.scanned_at.astimezone(manila_tz)
                    # Record the exact scan time in 12-hour format (with AM/PM)
                    row[f'day_{i}'] = manila_time.strftime('%Y-%m-%d %I:%M:%S %p')
                else:
                    # Mark as absent
                    row[f'day_{i}'] = "Absent"
            else:
                # If the event day is in the future, mark as "Not yet happened"
                row[f'day_{i}'] = "Not yet happened"
                
        attendance_data.append(row)

    # Pass data to the template
    return render(request, 'myApp/attendance_table.html', {
        'attendance_data': attendance_data,
        'event_days': event_days,
    })


# myApp/views.py
from django.shortcuts import render
from django.utils import timezone
from .models import Attendance

def attendance_summary(request, day):
    # Convert 'day' parameter (e.g., '2024-11-12') to a date object
    day = timezone.datetime.strptime(day, "%Y-%m-%d").date()

    # Fetch all attendance records for this specific day
    attendance_records = Attendance.objects.filter(scanned_at__date=day)
    
    return render(request, 'myApp/attendance_summary.html', {
        'attendance_records': attendance_records,
        'day': day,
    })

from django.shortcuts import render, redirect, get_object_or_404
from .models import Attendee

def delete_attendee(request, attendee_id):
    # Get the attendee object or 404 if not found
    attendee = get_object_or_404(Attendee, id=attendee_id)
    
    # Delete the attendee
    attendee.delete()

    # Redirect back to the list of attendees
    return redirect('list_attendees')
