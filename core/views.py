from django.shortcuts import render
from .forms import  UserAddForm
from .models import DonorDonee, UserCustom

from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from rest_framework.authtoken.models import Token

from .serializer import UsersModelSer, DonorSerializer, TokenLoginSer

@api_view(['POST'])
def generate_token(request):
    user = request.data
    serializer = TokenLoginSer(data=user)
    if serializer.is_valid():
        try:
            user = UserCustom.objects.get(email=serializer.data['email'])
            if user.password == serializer.data['password']:
                # if Token.objects.filter(user_id=user.id).exists():
                #     token = Token.objects.get(user_id=user.id)
                #     return Response({"token":str(token.key)})
                # token = Token.objects.create(user=user)
                token = Token.objects.get_or_create(user=user)
                return Response({"token":str(token[0])})
            else:
                return Response({"ERROR":"Password Does not Match"})
        except Exception as e:
            return Response({"ERROR":str(e)})
    return Response({"ERROR":serializer.errors})


@api_view(['GET','POST'])
def users_api_view(request):
    if request.method == "GET":
        users = UserCustom.objects.all()
        serializer = UsersModelSer(users, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        user = request.data
        serializer = UsersModelSer(data=user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    return Response({"MSG":"CREATE / GET USERS"})

@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_donordonee_api(request, btype):
    if request.method == 'GET' and btype in ["donor","reciever"]:
        donors=DonorDonee.objects.filter(user_type=btype.upper())
        serialzer = DonorSerializer(donors,many=True)
        return Response(serialzer.data)

    if request.method == 'POST':
        data = request.data
        serialzer = DonorSerializer(data=data)
        if serialzer.is_valid():
            print(serialzer.data)
        return Response({"MSG":"THIS IS POST METHOD"})

    return Response({'ERROR',"PLEASE SPECIFY DONOR/RECIEVER PROPERLY"})

# Create your views here.
def home_view(request):
    context = {}
    users = UserCustom.objects.all()
    formuser = UserAddForm(request.POST or None)

    context['users'] = users
    context['form'] = formuser

    if request.POST:
        if formuser.is_valid():
            formuser.save()
    return render(request, 'base.html',context)

def add_view(request):
    context = {}
    if request.method == "POST":
        user_email = request.POST.get('useremail')
        user_type = request.POST.get('usertype')

        #delete all the migartaions next time and continue

        try:
            user = UserCustom.objects.get(email=user_email)
            addObj = DonorDonee.objects.create(user_dd=user,bg_of_user=user.blood_group,user_type=user_type)
            addObj.save()
        except Exception as e:
            print(e)

    return render(request, 'addtrade.html', context)