from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Member
from django.contrib.auth import get_user_model




class MemberRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['email', 'password', 'dob', 'phone', 'nid', 'role', 'facebook', 'instagram', 'gmail', 'profile_pic']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True, 'allow_blank': False, 'error_messages': {'blank': 'Email is required.'}},
        }

    def create(self, validated_data):
        # Ensure the email is unique
        if Member.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})

        # Create the user instance with the provided profile_pic (which is now an image ID)
        user = Member(
            email=validated_data['email'],
            dob=validated_data.get('dob'),
            phone=validated_data.get('phone'),
            nid=validated_data.get('nid'),
            role=validated_data.get('role', 'gm'),
            facebook=validated_data.get('facebook'),
            instagram=validated_data.get('instagram'),
            gmail=validated_data.get('gmail'),
            profile_pic=validated_data.get('profile_pic'),  # Directly store the image ID
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'username', 'email', 'role', 'phone', 'facebook', 'instagram',"profile_pic" ]

    def validate_role(self, value):
        valid_roles = ['gm', 'admin', 'mod']  # Ensure 'mod' is in lowercase
        if value not in valid_roles:
            raise serializers.ValidationError("Role must be 'gm', 'admin', or 'mod'.")
        return value

class MemberINFOUPDATESerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

''' def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Try to fetch the user based on the email
        try:
            user = Member.objects.get(email=email)
        except Member.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        # Check if the password matches
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password")

        data['user'] = user  # Return the full user object if valid
        return data '''