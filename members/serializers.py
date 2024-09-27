from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Member
from django.contrib.auth import get_user_model





class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'email', 'dob', 'nid', 'role']
        def validate_role(self, value):
            valid_roles = ['gm', 'admin', 'MOD']
            if value not in valid_roles:
             
             raise serializers.ValidationError("Role must be 'gm', 'admin', or 'MOD'.")
            return value

class MemberINFOUPDATESerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = [
            'member_name',
            'email',
            'dob',
            'phone',
            'nid',
            'role',
            'facebook',
            'instagram',
            'gmail',
            'profile_pic',
            'availability',
        ]


class MemberRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Member
        fields = ['username', 'email', 'password',"phone","nid","dob","role", 'facebook', 'instagram', 'gmail']

    def create(self, validated_data):
        user = Member.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],  # Role of the user
            facebook=validated_data['facebook'],
            instagram=validated_data['instagram'],
            phone=validated_data['phone'],
            dob=validated_data['dob'],
            nid=validated_data['nid'],  # NID/Passport number
            gmail=validated_data['gmail']
        )
        return user
    

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