# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView


# GET


class ContactView(APIView):
    """类视图处理"""
    def get(self,request):
        contact_str="""\r\n%s>>>%s>>>
        %s
        """%(request.GET.get('name'),request.GET.get('email'),request.GET.get('message'))
        with open('subject.txt','a') as f:
            f.write(contact_str)
        return Response({'message':'感谢您的建议!'})
