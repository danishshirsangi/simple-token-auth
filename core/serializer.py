import email
from rest_framework import serializers

from .models import UserCustom, DonorDonee



class TokenLoginSer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return validated_data

    def validate(self, attr):
        if attr['email'] is not None and attr['password'] is not None:
            return attr
        else:
            raise serializers.ValidationError("Email/Password cannot be empty")

class UsersModelSer(serializers.ModelSerializer):
    class Meta:
        model = UserCustom
        exclude = ["last_login","is_admin"]

    def create_user(self, attr):
        if attr['email'] is not None and attr['password'] is not None:
            if UserCustom.objects.filter(email=attr['email']).exists():
                raise serializers.ValidationError('The User with Email Already Exists')
            else:
                user = UserCustom.objects.create_user(
                    email=attr['email'],
                    first_name=attr['first_name'],
                    last_name=attr['last_name'],
                    gender = attr['gender'],
                    blood_group=attr['blood_group'],
                    age=attr['age'],
                    mobile=attr['mobile'],
                    address=attr['address'],
                    is_active = True,  
                )
                user.set_password(attr['password'])
                return user


class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonorDonee
        fields = ["user_dd","user_type","bg_of_user"]

    
