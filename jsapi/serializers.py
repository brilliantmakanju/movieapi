from attr import field
from .models import Todo, Movie, SavedMovie
from django.contrib.auth.models import User
from rest_framework import serializers, validators
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_bytes, force_str, smart_str, DjangoUnicodeDecodeError

class SearchSerializers(serializers.Serializer):
    movieTitle = serializers.CharField(min_length=2)

    class Meta:
        fields = ['movieTitle']

    def validate(self, attrs):
        movieTitle = attrs.get('movieTitle')
        movieError = 'No movie with title found'
        movieResult = Movie.objects.filter(title=movieTitle)
        if movieResult:
            return (movieResult)
        else:
            return (movieError)
        
        return super().validate(attrs)

class SetResetPasswordSerialzers(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=68, write_only=True)
    uuid = serializers.CharField(min_length=1, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'uuid', 'token']
    
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            uuid = attrs.get('uuid')
            token = attrs.get('token')

            id = force_str(urlsafe_base64_decode(uuid))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The Reset Link is invalid', 401)
            
            user.set_password(password)
            user.save()

            return (user)

        except Exception as e:
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('Link is not active anymore', 401)

        return super().validate(attrs)

class PasswordRequestEmailSerialzers(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']

class MovieSerilizers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['pk', 'categories', 'title', 'short_desc', 'full_desc', 'poster_pic', 'video_file']

class SavedMovieSerilizers(serializers.ModelSerializer):
    class Meta:
        model = SavedMovie
        fields = ['pk', 'saved_by', 'movie']

class TodoSerilizers(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['task', 'completed', 'timestamp', 'updated', 'user']
    

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password':{'write_only':True},
            'username': {
                'required': True,
                'allow_blank': False,
                'validators': [
                    validators.UniqueValidator(
                        User.objects.all(), "Username Exists Already"
                    )
                ]
            },
            'email': {
                'required': True,
                'allow_blank': False,
                'validators': [
                    validators.UniqueValidator(
                        User.objects.all(), "Email Exists Already"
                    )
                ]
            }
        }

        def create(self, validated_data):
            email = validated_data.get('email')
            username = validated_data.get('username')
            password = validated_data.get('password')

            user = User.objects.create(
                username=username,
                password= password,
                email=email
            )
            
            return user



            