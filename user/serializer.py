from rest_framework import serializers
from .models import CustomAbstractBaseUser

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomAbstractBaseUser
        fields = ('id', 'email', 'password', 'building_code', 'building_num', 'building_name', 'admin_check' )

    # 유저 password 암호화하여 DB저장
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    # 사용자 정보 변경 - UserAPIView patch와 연관
    def update(self, user, validated_data):
        # 수정된 정보일 경우만 저장
        if 'password' in self.validated_data: 
            if user.password != self.validated_data['password']:
                user.set_password(validated_data['password'])
        user.save()
        return user
