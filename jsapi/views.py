from .util import send_mail
from .serializers import (
    TodoSerilizers, 
    MovieSerilizers, 
    SearchSerializers,
    RegisterSerializer, 
    SavedMovieSerilizers,
    SetResetPasswordSerialzers
)
from rest_framework.views import APIView
from .models import Todo, Movie, SavedMovie
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.encoding import smart_bytes, force_str, smart_str, DjangoUnicodeDecodeError

@api_view(["POST"])
def SearchMovie(request):
    searchTitle = request.data.get('movieTitle')
    searchMovie = Movie.objects.filter(title__icontains=searchTitle)
    # searchTitle.is_valid(raise_exception=True)
    # print(searchMovie)
    # print(searchSerilizer.data)
    if len(searchMovie) != 0:
        searchSerilizer = MovieSerilizers(searchMovie, many=True)
        return Response({
            'movieResult':searchSerilizer.data
        }, status=status.HTTP_200_OK)
    return Response({
        'error':'No movie foud with such title'
    }, status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def Register_User(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    return Response({
        "Success":"You Registered Successfully"
    })

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def GetMovie(request, movieid):
    movies = Movie.objects.get(pk=movieid)
    movie = MovieSerilizers(movies)
    return Response(movie.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def SetPasswordReset(request):
    serializer = SetResetPasswordSerialzers(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({
        'message':'Password Reset completed'
    })
 
@api_view(['GET'])
def PasswordCheckTokenApi(request, uuid, token):
    try:
        id = smart_str(urlsafe_base64_decode(uuid))
        user = User.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({'error':'Token has been used once and cants be used anymore, request new one to reset password'})
        return Response({'success':'Valid', 'uuid':uuid, 'token':token}, status=status.HTTP_200_OK)

    except DjangoUnicodeDecodeError:
        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({'error':'Token has been used once and cants be used anymore, request new one to reset password'})

@api_view(['POST'])
def PasswordRequestEmail(request):
    # serializer = PasswordRequestEmailSerialzers(data=request.data)
    email = request.data.get('email')

    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        uuid = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        sending_to = 'http://localhost:3000/Password-Reset-Confirm'
        relativelink = '/' + uuid + '/' + str(token)
        absurl = sending_to + relativelink
        email_body = '<h1><center>Reset Password </center></h1> Use Link below to reset password ' + absurl
        data = {
            'email_body':email_body,
            'to_email':user.email,
            'email_subject':'Reset Password'
        }
        send_mail(data)
        return Response({
            'success':'An email has been sent to you to help reset ur password'
        }, status=status.HTTP_200_OK)
    return Response({
        'error':'Email does not seem to be registered with us'
    }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
def Movies(request):
    movies = Movie.objects.all()
    movie = MovieSerilizers(movies, many=True)
    return Response(movie.data, status=status.HTTP_200_OK)

class TodoListApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        user = request.user
        # print(user)
        todos = Todo.objects.all()
        # print(todos)
        serializer = TodoSerilizers(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):

        data = {
            'task':request.data.get('task'),
            'completed':request.data.get('completed'),
            'user':request.data.get('user')
        }

        serializer = TodoSerilizers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    