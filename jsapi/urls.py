from django.urls import path
from .views import (
    Movies, 
    GetMovie,
    SearchMovie,
    Register_User, 
    TodoListApiView, 
    SetPasswordReset,
    PasswordRequestEmail,
    PasswordCheckTokenApi,
    MyTokenObtainPairView
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('movies', Movies, name='movies'),
    path('api', TodoListApiView.as_view()),
    path('Search', SearchMovie, name="searchmovie"),
    path('register', Register_User, name="register"),
    path('Movie/<int:movieid>', GetMovie, name="getmovie"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('password-reset-complete/', SetPasswordReset, name='password-reset-complete'),
    path('password-reset-request/', PasswordRequestEmail, name='password-reset-request'),
    path('password-confirm-request/<str:uuid>/<str:token>', PasswordCheckTokenApi, name='password-confirm-request'),
]