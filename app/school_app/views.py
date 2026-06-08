from rest_framework.views import APIView
from rest_framework.response import Response

from auth_app.permissions import RBACPermission


class GraduateView(APIView):
    permission_classes = [RBACPermission]
    resourse = 'graduate'

    def get(self, request):
        return Response(
            {
                'id': 1,
                'students': 'Iskhakov Dayan',
                'subject': 'math',
                'graduate': 5,
                'datetime': '08.06.2026'
            }
        )
    
    def post(self, request):
        return Response(
            {
                'id': 1,
                'students': 'Iskhakov Dayan',
                'subject': 'math',
                'graduate': 5,
                'datetime': '08.06.2026'
            }
        )


class SubjectView(APIView):
    permission_classes = [RBACPermission]
    resourse = 'subject'

    def get(self, request):
        return Response(
            {
                'id': 1,
                'teacher': 'Dayan',
                'name': 'math',
                'class': 12
            }
        )
    
    def post(self, request):
        return Response(
            {
                'id': 1,
                'teacher': 'Dayan',
                'name': 'math',
                'class': 12
            }
        )
