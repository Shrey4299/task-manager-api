
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import  RegisterUser
from .serializers import CustomUserSerializer, PasswordResetSerializer, UserUpdateSerializer
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import make_password
import jwt, datetime


class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):

        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        users = RegisterUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)


class GetUserById(APIView):
    def get(self, request, user_id):
        try:
            user = RegisterUser.objects.get(id=user_id)
            serializer = CustomUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except RegisterUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, user_id):
        try:
            user = RegisterUser.objects.get(id=user_id)
            serializer = UserUpdateSerializer(instance=user, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User updated successfully."}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except RegisterUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, user_id):
        try:
            user = RegisterUser.objects.get(id=user_id)
            user.delete()
            return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except RegisterUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class PasswordReset(APIView):
    def post(self, request, user_id):
        try:
            user = RegisterUser.objects.get(id=user_id)
            serializer = PasswordResetSerializer(data=request.data)

            if serializer.is_valid():
                new_password = serializer.validated_data.get('new_password')
                user.password = make_password(new_password)
                user.save()
                return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except RegisterUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class UserView(APIView):
    def get(self, request, format='json'):
        authorization_header = request.headers.get('Authorization')

        if not authorization_header or not authorization_header.startswith('Bearer '):
            raise AuthenticationFailed('Unauthenticated!')

        token = authorization_header.split(' ')[1]

        try:
            payload = jwt.decode(token, 'secret', algorithms='HS256') 
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        print(payload['id'])

        user = RegisterUser.objects.filter(id=payload['id']).first()
        
        if not user:
            raise AuthenticationFailed('User not found!')

        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = RegisterUser.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
    'id': user.id,
    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
    'iat': datetime.datetime.utcnow()
}
        #
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        #
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=False)
        response.data = {
            'jwt': token,
            'id': user.id,
        }
        return response





class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response







