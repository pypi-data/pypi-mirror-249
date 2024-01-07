from django.urls import path, include
from . import validators

app_name="stela_control"

urlpatterns = [
    path('validations/accounts/', validators.accountsData, name="accounts_data"),
    path('validations/booking/', validators.bookingData, name="booking_data"),
    path('validations/inputs/', validators.inputsData, name="inputs_data"),
    path('validations/jobs/', validators.jobApplication, name="jobs_data"),
    path('validations/handlers/', validators.coreHandlers, name="handlers_data"),
    path('validations/youtube-playlist/', validators.get_youtube_playlist_videos, name="playlist_data"),
    path('auth/password_reset_confirm/<uidb64>/<token>/', validators.new_password_activate, name="password_reset_token"),
    path('auth/account/<uidb64>/<token>/', validators.account_activate, name="account_token"),
 ]   