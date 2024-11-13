# myApp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),  # Main menu
    path("register/", views.register_attendee, name="register_attendee"),
    path("generate-qr/<int:attendee_id>/", views.generate_qr, name="generate_qr"),
    path("list-attendees/", views.list_attendees, name="list_attendees"),  # List attendees
    path("scan/", views.scan_qr_code, name="scan_qr_code"),  # QR code scanner (if implemented)
    path("log-attendance/", views.log_attendance, name="log_attendance"), 
    path("attendance-table/", views.attendance_table, name="attendance_table"),
     path("attendance-summary/<str:day>/", views.attendance_summary, name="attendance_summary"),  # Add this line
      path("delete-attendee/<int:attendee_id>/", views.delete_attendee, name="delete_attendee"),  # Delete URL
]
