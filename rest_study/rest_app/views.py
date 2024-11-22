from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import PersonSerializer,RegisterSerializer,LoginSerializer
from .models import Person
from rest_framework.views import APIView
from rest_framework import viewsets,status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import TokenAuthentication


#class based view
class PersonClass(APIView):
    #here the method is declared by fun name not if else
    def get(self,request):
        personobj = Person.objects.all()  #It is used to make a object of person model from db
        serializer = PersonSerializer(personobj, many = True) # many should be ither true or false if there is multiple data the it should be true else false
        return Response(serializer.data)
    def post(self,request):
        return Response("This is post method from Apiview")



#view based fun
@api_view(['GET','POST','PUT'])
def index(request):
    if request.method == 'GET':
        person={
            'name':'Jathu',
            'age':21
        }
        return Response(person)
    elif request.method == 'POST':
        return Response("THIS IS A POST METHOD")
    elif request.method == 'PUT':
        return Response("THIS IS A PUT METHOD")    

@api_view(['GET','POST','PUT','PATCH','DELETE'])
def person(request):
    #GET method
    if request.method == 'GET':
        personobj = Person.objects.all()  #It is used to make a object of person model from db
        serializer = PersonSerializer(personobj, many = True) # many should be ither true or false if there is multiple data the it should be true else false
        return Response(serializer.data)#sending serializer data 
    # POST method
    elif request.method == 'POST':
        data = request.data #this data is what we get on posting somethisng
        serializer = PersonSerializer(data = data) #deserializing the data to convert it from query to json
        if serializer.is_valid():  # checking if the data is valid 
            serializer.save()
            return Response(serializer.data)# returns the data
        return Response(serializer.errors)# returns an error msg
    #PUT method
    elif request.method == 'PUT':
        data = request.data 
        obj = Person.objects.get(id=data['id'])#fetch data using id
        serializer = PersonSerializer(obj,data = data, partial = False)#first the obj of data is passed then the data got from the request is passed and at last partial set to false as method is PUT
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    #PATCH method (same as put the only change is that partial is set to True)
    elif request.method == 'PATCH':
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(obj, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    # DELETE method
    else:
        data=request.data
        obj=Person.objects.get(id=data['id'])
        obj.delete()
        return Response("Deleted successfully")
        




#Model view set 

class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer #give the serializer class
    queryset = Person.objects.all() #model 

    #to search from dataset
    def list(self,request):
        search = request.GET.get('search')
        queryset =self.queryset

        if search:
           queryset = queryset.filter(name__startswith=search)#
        serializer = PersonSerializer(queryset,many = True)
        return Response({'status':200,'data':serializer.data})        
        



#registering
class RegisterApi(APIView):
    permission_classes = [] # or [AllowAny ]
    def post(self,request):
        data = request.data
        serialzer = RegisterSerializer(data = data)

        if not serialzer.is_valid():
            return Response({'message':serialzer.errors},status = status.HTTP_404_NOT_FOUND )
        serialzer.save()
        return Response({'message':"user created"},status = status.HTTP_201_CREATED)


class LoginApi(APIView):
     permission_classes = [] # or [AllowAny ]
     def post(self,request):
        data = request.data
        serializer = LoginSerializer(data = data)

        if not serializer.is_valid():
            return Response({'message':serializer.errors},status=status.HTTP_404_NOT_FOUND)
        
        user = authenticate(username = serializer.data['username'],password = serializer.data['password'])

        if not user:
            return Response({'message':"invalid user"},status=status.HTTP_404_NOT_FOUND)
        
        token, created = Token.objects.get_or_create(user=user)
        return Response({'message':"Login successufull",'token':str(token)},status=status.HTTP_302_FOUND)


class ClassPerson(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request,):
        objperson = Person.objects.filter(team__isnull=False) 
        serializer = PersonSerializer(objperson, many=True) 
        return Response(serializer.data)  
    def post(self, request):
         return Response("This is post")   

