from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = 'id', 'email', 'name', 'password',
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'user-input': 'password'}}
        }

    def run_validation(self, data):
        self.user = User(email=data['email'], name=data['name'])
        return super().run_validation(data)

    def validate_password(self, value):
        validate_password(value, user=self.user)
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the users authentications sys"""
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        """validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), email=email, password=password)
        if not user:
            msg = _('Unable to authenticate with provided credintials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
