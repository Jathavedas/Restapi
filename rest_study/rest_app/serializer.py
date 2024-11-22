from rest_framework import serializers
from .models import Person,Team
from django.contrib.auth.models import User

#only display particular field of a foriegn key
class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ['team_name']

class PersonSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)# not req for disp all fields

    class Meta:
        model = Person
        fields = '__all__'
        depth = 1 #(all fields of the team class will be displayed)

    #all the needed validation can be done like this also 
    def validate(self, data):
        spl_char = "!@#$%^&*()_-:;{[]}-=/`~,.'<>"

        if any(char in spl_char for char in data['name']):
            raise serializers.ValidationError("Name shouldnot have any special charachters")
        
        if data['age'] < 18:
            raise serializers.ValidationError("Age should be above 18")

        return data

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
     
    #validating user 
    def validate(self, data):
        if data['username']:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError("User already exists")
        
        if data['email']:
            if data['email']:
                if User.objects.filter(email = data['email']).exists():
                    raise serializers.ValidationError("User already exists")
        
        return data

    def create(self, validated_data):
        user=User.objects.create(username = validated_data['username'], email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data
    
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()