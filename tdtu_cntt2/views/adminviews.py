import base64
import datetime
import os
import uuid

import jwt
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from tdtu_cntt2.models import User, AdminAccounts, Role, Departments, Process, Step
from tdtu_cntt2.serializers import *
from tdtu_cntt2.views.userviews import check_login


class LogoutView(APIView):
    def post(self, request):
        try:
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except KeyError:
            return Response({'message': 'Logout failed'}, status=status.HTTP_400_BAD_REQUEST)
class AdminLogin(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        admin = AdminAccounts.objects.filter(username=username).first()
        if admin is None:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        if not check_password(password, admin.password):
            return Response({'message': 'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)
        payload = {
            'id': admin.id,
            'is_admin': True,
            'username': admin.username,
        }
        token = jwt.encode(payload, 'secret',algorithm='HS256')
        response = Response()
        response.data = {
            'username': admin.username,
            'id': admin.id,
            'jwt': token
        }
        return response
def is_admin(payload):
    return payload['is_admin']
class ChangePasswordAdmin(APIView):
    def post(self, request):
        try:
            payload = check_login(request)
            if isinstance(payload, Response):
                return payload
            if not is_admin(payload):
                return Response({'message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
            user_id = payload['id']
            user = AdminAccounts.objects.get(id=user_id)
            if not check_password(request.data.get('old_password'), user.password):
                return Response({'message': 'Incorrect old password'}, status=status.HTTP_400_BAD_REQUEST)
            user.password = make_password(request.data.get('new_password'))
            user.save()
            return Response({'message': 'Change password successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Change password failed, please try again'}, status=status.HTTP_400_BAD_REQUEST)

def create_signature(private_key, data):
    signature = private_key.sign(
        data,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return base64.b64encode(signature).decode('utf-8')

class AddUserView(APIView):
    def post(self, request):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        if not is_admin(payload):
            return Response({'message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()  # Tạo bản sao của dữ liệu đầu vào
        if 'password' not in data:
            data['password'] = data.get('username')
        # tạo khóa rsa
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        # lưu trữ dưới dạng pem
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        unique_name = uuid.uuid4()
        random_name = str(unique_name)[:8]
        private_filename = f"{random_name}_private.pem"
        private_path = os.path.join('tdtu_cntt2/private_key', private_filename)
        os.makedirs(os.path.dirname(private_path), exist_ok=True)

        with open(private_path, "wb") as private_file:
            private_file.write(private_key_pem)

        # lưu vào db dưới dạng string
        # data['private_key'] = private_key_pem.decode('utf-8')
        data['private_key'] = random_name
        # tạo public key
        public_key = private_key.public_key()
        # lưu trữ dưới dạng pem
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        public_filename = f"{random_name}_public.pem"
        public_path = os.path.join('tdtu_cntt2/public_key', public_filename)
        os.makedirs(os.path.dirname(public_path), exist_ok=True)

        with open(public_path, "wb") as public_file:
            public_file.write(public_key_pem)


        # lưu vào db dưới dạng string
        # data['public_key'] = public_key_pem.decode('utf-8')

        data['public_key'] = random_name
        # tạo chứng chỉ số
        subject = x509.Name([
            x509.NameAttribute(x509.NameOID.COMMON_NAME, u'{} - {}'.format(data['username'], data['full_name'])),
            x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, u'TDTU-VietNam'),
            x509.NameAttribute(x509.NameOID.COUNTRY_NAME, u'VN'),
        ])
        builder = x509.CertificateBuilder().subject_name(subject).issuer_name(subject)
        builder = builder.public_key(public_key)
        builder = builder.serial_number(x509.random_serial_number())
        builder = builder.not_valid_before(datetime.datetime.utcnow())
        builder = builder.not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
        certificate = builder.sign(
            private_key=private_key,
            algorithm=hashes.SHA256(),
            backend=default_backend()
        )
        certificate_pem = certificate.public_bytes(serialization.Encoding.PEM)
        # data['certificate'] = certificate_pem.decode('utf-8')
        data['certificate'] = random_name

        certificate_filename = f"{random_name}_certificate.pem"
        certificate_path = os.path.join('tdtu_cntt2/certificates', certificate_filename)

        os.makedirs(os.path.dirname(certificate_path), exist_ok=True)

        with open(certificate_path, "wb") as cert_file:
            cert_file.write(certificate_pem)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User created successfully', 'user_id': user.id, 'username': user.username, 'full_name': user.full_name, 'is_active': user.is_active},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUser(APIView):
    def delete(self, request, id):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        if not is_admin(payload):
            return Response({'message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        user = get_object_or_404(User, id=id)
        Step.objects.filter(user_id=id).delete()
        user.delete()
        return Response({'message': 'Delete successful'}, status=status.HTTP_200_OK)


class UpdateUser(APIView):
    def put(self, request, id):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        if not is_admin(payload):
            return Response({'message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        user = get_object_or_404(User, id=id)
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if User.objects.filter(username=request.data['username']).exclude(id=id).exists():
            return Response({'message': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if 'username' in request.data:
            username = request.data['username']
            if user.password == user.username:
                user.password = username
        if serializer.is_valid():
            serializer.save()
        return Response({'message': 'Update successful'}, status=status.HTTP_200_OK)

class GetAllUser(APIView):
    def get(self, request):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        users = User.objects.select_related('role_id', 'department_id').all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
# Role
class AddRole(APIView):
    def post(self, request):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        if not is_admin(payload):
            return Response({'message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            role = serializer.save()
            return Response({'message': 'Add successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class DeleteRole(APIView):
    def delete(self, request, id):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        if not is_admin(payload):
            return Response({'message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        role = get_object_or_404(Role, id=id)
        role.delete()
        return Response({'message': 'Delete successful'}, status=status.HTTP_200_OK)
class UpdateRole(APIView):
    def put(self, request, id):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        if not is_admin(payload):
            return Response({'message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        role = get_object_or_404(Role, id=id)
        serializer = RoleSerializer(role, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Update successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class GetAllRole(APIView):
    def get(self, request):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
# Department API
class AddDepartment(APIView):
    def post(self, request):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        if not is_admin(payload):
            return Response({'message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            department = serializer.save()
            return Response({'message': 'Add successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class DeleteDepartment(APIView):
    def delete(self, request, id):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        if not is_admin(payload):
            return Response({'message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        department = get_object_or_404(Departments, id=id)
        department.delete()
        return Response({'message': 'Delete successful'}, status=status.HTTP_200_OK)
class UpdateDepartment(APIView):
    def put(self, request, id):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        if not is_admin(payload):
            return Response({'message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        department = get_object_or_404(Departments, id=id)
        serializer = DepartmentSerializer(department, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Update successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllDepartment(APIView):
    def get(self, request):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        departments = Departments.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class ResetPassword(APIView):
    def put(self, request, user_id):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        try:
            user = User.objects.get(id = user_id)
            user.password = user.username
            user.is_active = False
            user.save()
            return Response({'message': 'Reset password successful'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

# Process
class ProcessCreateView(APIView):
    def post(self, request):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        if not is_admin(payload):
            return Response({'message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProcessSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProcessUpdateView(APIView):
    def put(self, request, process_id):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        if not is_admin(payload):
            return Response({'message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            process = Process.objects.get(id=process_id)
        except ObjectDoesNotExist:
            return Response({'message': 'Process not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProcessSerializer(process, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteProcess(APIView):
    def delete(self, request, process_id):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        if not is_admin(payload):
            return Response({'message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            process = Process.objects.get(id=process_id)
            step = Step.objects.filter(process_id=process_id)
            process.delete()
            step.delete()
            return Response({'message': 'Process delete successful'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Process not found'}, status=status.HTTP_404_NOT_FOUND)
class ProcessDetailByIdView(APIView):
    def get(self, request, process_id):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        try:
            process = Process.objects.get(id=process_id)
            steps = Step.objects.filter(process_id=process_id)
            process_serializer = ProcessSerializer(process)
            steps_serializer = StepDetailSerializer(steps, many=True)
            process_data = process_serializer.data
            process_data['steps'] = steps_serializer.data
            return Response(process_data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Process not found'}, status=status.HTTP_404_NOT_FOUND)
class ProcessListView(APIView):
    def get(self, request):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        processes = Process.objects.all()
        serializer = ProcessSerializer(processes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
# Step
class StepCreateView(APIView):
    def post(self, request):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        serializer = StepSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StepUpdateView(APIView):
    def put(self, request, step_id):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        if not is_admin(payload):
            return Response({'message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            step = Step.objects.get(id=step_id)
        except ObjectDoesNotExist:
            return Response({'message': 'Step not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StepSerializer(step, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class DeleteStep(APIView):
    def delete(self, request, step_id):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        if not is_admin(payload):
            return Response({'message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            step = Step.objects.get(id=step_id)
            step.delete()
            return Response({'message': 'Step delete successful'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Step not found'}, status=status.HTTP_404_NOT_FOUND)
class StepDetailView(APIView):
    def get(self, request, step_id):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        try:
            step = Step.objects.get(id=step_id)
            serializer = StepSerializer(step)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Step not found'}, status=status.HTTP_404_NOT_FOUND)
class StepListView(APIView):
    def get(self, request):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        steps = Step.objects.all()
        serializer = StepSerializer(steps, many=True)
        data = serializer.data
        for step_data in data:
            role_id = step_data['role_id']
            try:
                role = Role.objects.get(id=role_id)
                role_serializer = RoleSerializer(role)
                step_data['role'] = role_serializer.data
            except ObjectDoesNotExist:
                step_data['role'] = None

            user_id = step_data['user_id']
            try:
                user = User.objects.get(id=user_id)
                user_serializer = UserSerializer(user)
                step_data['user'] = user_serializer.data
            except ObjectDoesNotExist:
                step_data['user'] = None

            process_id = step_data['process_id']
            try:
                process = Process.objects.get(id=process_id)

                process_serializer = ProcessSerializer(process)
                step_data['process'] = process_serializer.data
            except ObjectDoesNotExist:
                step_data['process'] = None
        return Response(serializer.data, status=status.HTTP_200_OK)








