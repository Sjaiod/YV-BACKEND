from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import  permissions
from .models import Member
from .serializers import MemberSerializer,MemberINFOUPDATESerializer,MemberRegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import MemberRegistrationSerializer,LoginSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.parsers import MultiPartParser
from utils.drive_uploader import upload_single_file_to_drive,check_image_exists,delete_image_from_drive

# Create your views here.

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Validate the input using the LoginSerializer
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.data['email']
        password = serializer.data['password']

        # Authenticate using the email and password
        user_obj = authenticate(email=email, password=password)

        if user_obj is None:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)

        # Get or create token for the authenticated user
        token, _ = Token.objects.get_or_create(user=user_obj)

        # Return the token along with the user's role
        return Response({
            'token': token.key,
            'role': user_obj.role,  # Send back profile picture (image ID)
        }, status=status.HTTP_200_OK)


class SetAvailabilityView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        user.availability = request.data.get('availability', user.availability)
        user.save()
        return Response({'status': 'availability updated'})
    


class RegisterMemberView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        serializer = MemberRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GETallMembersView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        members = Member.objects.all()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)
    
class MemberInfoView(APIView):
    permission_classes = [IsAuthenticated]  # Only allow authenticated users

    def get(self, request):
        user = request.user  # Get the current user from the request
        user_info = {
            'id': user.id,
            'email': user.email,
            'member_name': user.member_name,
            'dob': user.dob,
            'phone': user.phone,
            'nid': user.nid,
            'role': user.role,
            'facebook': user.facebook,
            'instagram': user.instagram,
            'gmail': user.gmail,
            'availability': user.availability,
            # Include other fields as necessary
        }
        return Response(user_info, status=status.HTTP_200_OK)
     
class RoleViewAPI(APIView):
    permission_classes = [IsAuthenticated]  # Only allow authenticated users

    def get(self, request):
        user = request.user  # Get the current user from the request
        user_info = {
            'role': user.role,
            # Include other fields as necessary
        }
        return Response(user_info, status=status.HTTP_200_OK)

class SearchUserView(APIView):
    permission_classes = [IsAuthenticated]  # Only allow authenticated users

    def get(self, request):
        query = request.GET.get('member_name', None)  # Get the search query from the request
        if query is None:
            return Response({"error": "Query parameter 'member_name' is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Search for users with matching member_name (case-insensitive)
        users = Member.objects.filter(member_name__icontains=query)

        # Prepare a list of user info to return
        user_info_list = [{
            'id': user.id,
            'member_name': user.member_name,
            'email': user.email,
            'role': user.role,
            'availability': user.availability,
            # Include other fields as necessary
        } for user in users]

        return Response(user_info_list, status=status.HTTP_200_OK)
    
class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Only allow authenticated users

    def put(self, request):
        user = request.user  # Get the current user
        serializer = MemberINFOUPDATESerializer(user, data=request.data, partial=True)  # Use partial=True to allow partial updates

        if serializer.is_valid():
            serializer.save()  # Save the updated data
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SingleImageUploadView(APIView):
    permission_classes=[AllowAny]
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
       image=request.FILES.get('image')
       pre_image=request.data.get("pre_image",None)
       if not image:
            return Response({"error": "No image file provided."}, status=400)
       if pre_image:
           
           checkFileExist=check_image_exists(pre_image)
           if not check_image_exists:
               upload=upload_single_file_to_drive(image)
               if upload:
                   return Response({"id":upload},status=200)
           else :
               delfile=delete_image_from_drive(pre_image)
               if delfile:
                    upload=upload_single_file_to_drive(image)
               if upload:
                   return Response({"id":upload},status=200)
               
       else:
            upload=upload_single_file_to_drive(image)
            if upload:
                   return Response({"id":upload},status=200)
                   
               

     