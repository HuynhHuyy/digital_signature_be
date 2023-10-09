import base64
import io
import re
import uuid

import docx
import jwt
import pdfplumber
from PIL import Image
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding, utils
from cryptography.x509 import load_pem_x509_certificate
from django.contrib.auth.hashers import check_password, make_password
from pyhanko import stamp
from pyhanko.keys import load_cert_from_pemder
from pyhanko.pdf_utils import images, text
from pyhanko.pdf_utils.font import opentype
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko.sign import signers, fields as pyhanko_fields
from pyhanko.sign.validation import validate_pdf_signature
from pyhanko_certvalidator import ValidationContext
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from tdtu_cntt2.serializers import *
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from ..search_indexes import *
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    CompoundSearchFilterBackend,)
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import FileResponse, HttpResponse, JsonResponse
import os
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        # tai khoan chua kich hoat thi kiem tra mk binh thuong
        if not user.is_active:
            if password != user.password:
                return Response({'message': 'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)

            if user.department_id is None:
                role_serializer = RoleSerializer(user.role_id)
                role_data = role_serializer.data
                payload = {
                    'id': user.id,
                    'username': user.username,
                    'full_name': user.full_name,
                    'is_active': user.is_active,
                    'role_id': role_data['id'],
                    'role_name': role_data['name'],
                    'role_description': role_data['description'],
                }
                token = jwt.encode(payload,'secret', algorithm='HS256')
                user.save()
                return Response({'message': 'Login successful', 'id': user.id, 'username': user.username, 'full_name': user.full_name, 'is_active': user.is_active,  'role_id': role_data['id'],'role_name': role_data['name'], 'role_description': role_data['description'],'jwt': token}, status=status.HTTP_200_OK)
            if user.role_id is None:
                department_serializer = DepartmentSerializer(user.department_id)
                department_data = department_serializer.data
                payload = {
                    'id': user.id,
                    'username': user.username,
                    'full_name': user.full_name,
                    'is_active': user.is_active,
                    'department_id': department_data['id'],
                    'department_name': department_data['name'],
                    'department_description': department_data['description'],
                }
                token = jwt.encode(payload, 'secret', algorithm='HS256')
                user.save()
                return Response({'message': 'Login successful', 'id': user.id, 'username': user.username,'full_name': user.full_name, 'is_active': user.is_active, 'department_id': department_data['id'], 'department_name': department_data['name'], 'department_description': department_data['description'],'jwt': token}, status=status.HTTP_200_OK)
            if user.department_id is None and user.role_id is None:
                payload = {
                    'id': user.id,
                    'username': user.username,
                    'full_name': user.full_name,
                    'is_active': user.is_active,
                }
                token = jwt.encode(payload,'secret', algorithm='HS256')
                user.save()
                return Response({'message': 'Login successful', 'id': user.id, 'username': user.username,'full_name': user.full_name, 'is_active': user.is_active,'jwt': token}, status=status.HTTP_200_OK)
            else:
                department_serializer = DepartmentSerializer(user.department_id)
                department_data = department_serializer.data
                role_serializer = RoleSerializer(user.role_id)
                role_data = role_serializer.data

                payload = {
                    'id': user.id,
                    'username': user.username,
                    'full_name': user.full_name,
                    'is_active': user.is_active,
                    'department_id': department_data['id'],
                    'department_name': department_data['name'],
                    'department_description': department_data['description'],
                    'role_id': role_data['id'],
                    'role_name': role_data['name'],
                    'role_description': role_data['description'],
                }
                token = jwt.encode(payload, 'secret', algorithm='HS256')
                user.save()
                return Response({'message': 'Login successful', 'id': user.id, 'username': user.username, \
                                 'full_name': user.full_name, 'is_active': user.is_active, \
                                 'department_id': department_data['id'], \
                                 'department_name': department_data['name'], \
                                 'department_description': department_data['description'], \
                                 'role_id': role_data['id'],'role_name': role_data['name'], \
                                 'role_description': role_data['description'], 'jwt': token}, status=status.HTTP_200_OK)
        # tai khoan da kich hoat kiem tra mk bang check_password()
        else:
            if not check_password(password, user.password):
                return Response({'message': 'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)

            if user.department_id is None:
                role_serializer = RoleSerializer(user.role_id)
                role_data = role_serializer.data
                payload = {
                    'id': user.id,
                    'username': user.username,
                    'full_name': user.full_name,
                    'is_active': user.is_active,
                    'role_id': role_data['id'],
                    'role_name': role_data['name'],
                    'role_description': role_data['description'],
                }
                token = jwt.encode(payload, 'secret', algorithm='HS256')
                user.save()
                return Response({'message': 'Login successful', 'id': user.id, 'username': user.username,
                                 'full_name': user.full_name, 'is_active': user.is_active, 'role_id': role_data['id'],
                                 'role_name': role_data['name'], 'role_description': role_data['description'], 'jwt': token },
                                status=status.HTTP_200_OK)
            if user.role_id is None:
                department_serializer = DepartmentSerializer(user.department_id)
                department_data = department_serializer.data
                payload = {
                    'id': user.id,
                    'username': user.username,
                    'full_name': user.full_name,
                    'is_active': user.is_active,
                    'department_id': department_data['id'],
                    'department_name': department_data['name'],
                    'department_description': department_data['description'],
                }
                token = jwt.encode(payload, 'secret', algorithm='HS256')
                user.save()
                return Response({'message': 'Login successful', 'id': user.id, 'username': user.username,
                                 'full_name': user.full_name, 'is_active': user.is_active,
                                 'department_id': department_data['id'], 'department_name': department_data['name'],
                                 'department_description': department_data['description'], 'jwt': token}, status=status.HTTP_200_OK)
            if user.department_id is None and user.role_id is None:
                payload = {
                    'id': user.id,
                    'username': user.username,
                    'full_name': user.full_name,
                    'is_active': user.is_active,
                }
                token = jwt.encode(payload, 'secret', algorithm='HS256')
                user.save()
                return Response({'message': 'Login successful', 'id': user.id, 'username': user.username,
                                 'full_name': user.full_name, 'is_active': user.is_active,'jwt': token}, status=status.HTTP_200_OK)
            else:
                department_serializer = DepartmentSerializer(user.department_id)
                department_data = department_serializer.data
                role_serializer = RoleSerializer(user.role_id)
                role_data = role_serializer.data

                payload = {
                    'id': user.id,
                    'username': user.username,
                    'full_name': user.full_name,
                    'is_active': user.is_active,
                    'department_id': department_data['id'],
                    'department_name': department_data['name'],
                    'department_description': department_data['description'],
                    'role_id': role_data['id'],
                    'role_name': role_data['name'],
                    'role_description': role_data['description'],
                }
                token = jwt.encode(payload, 'secret', algorithm='HS256')
                user.save()

                return Response({'message': 'Login successful', 'id': user.id, 'username': user.username,
                                 'full_name': user.full_name, 'is_active': user.is_active,
                                 'department_id': department_data['id'], 'department_name': department_data['name'],
                                 'department_description': department_data['description'], 'role_id': role_data['id'],
                                 'role_name': role_data['name'], 'role_description': role_data['description'], 'jwt': token },
                                status=status.HTTP_200_OK)
def check_login(request):
    token = request.headers['Authorization']
    if not token or token == 'null':
        return Response({'message': 'Token not found'}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return Response({'message': 'Token expired'}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        return Response({'message': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
    return payload
class FirstTimeLoginView(APIView):
    def post(self, request):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        user = User.objects.get(id=payload['id'])
        username = user.username
        password = request.data.get('password')
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        if not user.is_active:
            user.password = make_password(password)
            user.is_active = True
            user.save()
            return Response({'message': 'Change password successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
class ChangePasswordView(APIView):
    def post(self, request):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        user = User.objects.get(id=payload['id'])
        username = user.username
        password = request.data.get('password')
        new_password = request.data.get('new_password')
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        if not check_password(password, user.password):
            return Response({'message': 'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)
        user.password = make_password(new_password)
        user.save()
        return Response({'message': 'Change password successful'}, status=status.HTTP_200_OK)
class AddApplication(APIView):
    def post(self, request):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        request.data['sender_id'] = payload['id']
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            application = serializer.save()
            return Response({'message': 'Add successful','id':application.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class DeleteApplication(APIView):
    def put(self, request, id):
        print('delete')
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        user_id = payload['id']
        application = Application.objects.get(id=id)
        receiver = ReceiverApplication.objects.filter(application_id=id)
        print('2')
        if application.sender_id.id == user_id:
            application.delete_by_sender = True
            application.save()
            return Response({'message': 'Delete successful'}, status=status.HTTP_200_OK)
        elif receiver.filter(user_receiver_id=user_id).exists():
            receiver.filter(user_receiver_id=user_id).update(delete=True)
            return Response({'message': 'Delete successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
class SignatureCreateView(APIView):
    def post(self, request):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        request.data['user_id'] = payload['id']
        user_id = request.data.get('user_id')
        user = User.objects.get(id=user_id)

        serializer = SignatureSerializer(data=request.data)
        if serializer.is_valid():
            signature = serializer.save()
            return Response({'message': 'Add Signature successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class SignatureDelete(APIView):
    def delete(self, request, id):
        # payload = check_login(request)
        # if isinstance(payload, Response):
        #     return payload
        try:
            signature = Signature.objects.get(id=id)
            signature.delete()
            return Response({'message': 'Signature deleted'}, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({'message': 'Signature not found'}, status=status.HTTP_404_NOT_FOUND)
class SignatureList(APIView):
    def get(self, request):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        get_user_id = payload['id']
        signatures = Signature.objects.filter(user_id=get_user_id)
        serializer = SignatureSerializer(signatures, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetPublicApplication(APIView):
    def get(self, request):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        applications = Application.objects.all()
#         get all application in db which status = 2 and is_public = 1
        applications = applications.filter(status=2, is_public=1)
        serializer = ApplicationSerializer(applications, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
class PublicApplication(APIView):
    def put(self, request, id):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        user_id = payload['id']
        application = Application.objects.get(id=id)
        if application.sender_id.id == user_id:
            application.is_public = 1
            application.save()
            return Response({'message': 'Public successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

class UnPublicApplication(APIView):
    def put(self, request, id):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        user_id = payload['id']
        application = Application.objects.get(id=id)
        if application.sender_id.id == user_id:
            application.is_public = 0
            application.save()
            return Response({'message': 'UnPublic successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
class GetAllApplication(APIView):
    def get(self, request):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        id = payload['id']
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        data = serializer.data
        for application in data:
            application_id = application['id']
            receiver_applications = ReceiverApplication.objects.filter(application_id=application_id)
            receiver_applications_serializer = ReceiverSerializer(receiver_applications, many=True)
            application['user_receiver'] = receiver_applications_serializer.data
        # filders data by sender_id and receiver_id and remove delete === true in user_receiver
        data = list(filter(lambda x: x['sender_id'] == id or any(user['user_receiver_id'] == id and user['delete'] == False for user in x['user_receiver']), data))
        # data = list(filter(lambda x: any( and  for user in x['user_receiver']), data))
        # data = list(filter(lambda x: x['sender_id'] == id or any(user['user_receiver_id'] == id for user in x['user_receiver']), data))
        # order by created_at
        data = sorted(data, key=lambda x: x['created_at'], reverse=True)
        return Response(data, status=status.HTTP_200_OK)
class ApplicationSenderList(APIView):
    def get(self, request):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        get_user_id = payload['id']
        applications = Application.objects.filter(sender_id=get_user_id)
        serializer = ApplicationSerializer(applications, many=True)
        data = serializer.data
        for application in data:
            application_id = application['id']
            receiver_applications = ReceiverApplication.objects.filter(application_id=application_id)
            receiver_applications_serializer = ReceiverSerializer(receiver_applications, many=True)
            application['user_receiver'] = receiver_applications_serializer.data
        return Response(data, status=status.HTTP_200_OK)
class GetApplicationById(APIView):
    def get(self, request, id):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        application = Application.objects.get(id=id)
        serializer = ApplicationSerializer(application)
        data = serializer.data
        application_id = data['id']
        receiver_applications = ReceiverApplication.objects.filter(application_id=application_id)
        receiver_applications_serializer = ReceiverSerializer(receiver_applications, many=True)
        data['user_receiver'] = receiver_applications_serializer.data
        return Response(data, status=status.HTTP_200_OK)
class AllReceiverApplicationList(APIView):
    def get(self, request):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        get_user_id = payload['id']
        receiver_applications = ReceiverApplication.objects.filter(user_receiver_id=get_user_id)
        serializer = ReceiverSerializer(receiver_applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class AddReceiverAPIView(APIView):
    def post(self, request):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        serializer = ReceiverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UpdateStatusReceiverAPIView(APIView):
    def put(self, request, id):
        try:
            payload = check_login(request)
            if isinstance(payload, Response):
                return payload
            receiver = ReceiverApplication.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({'message': 'Receiver not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReceiverSerializer(receiver, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Update successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UpdateReceiverAPIView(APIView):
    def put(self, request, id):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        try:
            receiver = ReceiverApplication.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({'message': 'Receiver not found'}, status=status.HTTP_404_NOT_FOUND)
        user_id = payload['id']
        user = User.objects.get(id=user_id)
        serializer = ReceiverSerializer(receiver, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Update successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UpdateSenderAPIView(APIView):
    def put(self, request, id):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        try:
            application = Application.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({'message': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
        print(request.data)
        serializer = ApplicationSerializer(application, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Update successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class GetAllReceiveIdByApplicationId(APIView):
    def get(self, request, application_id):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        try:
            application = Application.objects.get(id=application_id)
            receive_application = ReceiverApplication.objects.filter(application_id=application_id)
            serializer = ReceiverSerializer(receive_application, many=True)
            list_id = []
            for item in serializer.data:
                list_id.append(item['id'])
            return Response(list_id, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
class GetAllReceiveByApplicationId(APIView):
    def get(self, request, application_id):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        try:
            application = Application.objects.get(id=application_id)
            receive_application = ReceiverApplication.objects.filter(application_id=application_id)
            serializer = ReceiverSerializer(receive_application, many=True)
            list_status = []
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
class PublisherApplicationView(DocumentViewSet):
    document = ApplicationDocument
    serializer_class = SearchApplicationSerializer
    lookup_field = 'id'
    filter_backends = [FilteringFilterBackend, CompoundSearchFilterBackend]
    # search_fields = ('title', 'pdf_content','created_at')
    search_fields = ('title', 'pdf_content')
    multi_match_search_fields = ('title', 'pdf_content', 'sender_id')
    filter_fields = {
        'title': 'title',
        'pdf_content': 'pdf_content',
        'sender_id': 'sender_id',
    }
class CountApplicationReceiver(APIView):
    def get(self, request):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        user_count = payload['id']
        try:
            count = ReceiverApplication.objects.filter(user_receiver_id=user_count, status=0).count()
            return Response({'count': count}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class FileUploadView(APIView):
    parser_classes = [MultiPartParser]
    def generate_unique_filename(self, filename):
        # Tạo tên mới duy nhất bằng cách sử dụng uuid
        ext = filename.split('.')[-1]
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        return unique_filename
    def post(self, request, format=None):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        request.data['user_id'] = payload['id']
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file = request.FILES['file']
            upload_directory = 'tdtu_cntt2/files'
            if not os.path.exists(upload_directory):
                os.makedirs(upload_directory)
            # Generate a unique filename to avoid overwriting existing files
            unique_filename = self.generate_unique_filename(file.name)
            file_path = os.path.join(upload_directory, unique_filename)
            file_serializer.save(file=file_path, name=file.name)
            # Open the file in the specified directory and save the uploaded file
            with open(file_path, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            url_file = request.build_absolute_uri('/load-file/' + str(file_serializer.data['id']) + '/')
            response_data = file_serializer.data
            # response_data['urlFile'] = url_file.replace('http://', 'https://')
            response_data['urlFile'] = url_file
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoadFileView(APIView):
    def get(self, request, id):
        # payload = check_login(request)
        # if isinstance(payload, Response):
        #     return payload
        try:
            file = Files.objects.get(id=id)
            file_path = file.file.path
            return FileResponse(open(file_path, 'rb'))
        except ObjectDoesNotExist:
            return Response({'message': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

class GetStatusByApplicationUserReceiveId(APIView):
    def post(self, request):
        receiver_id = request.data.get('receiver_id')
        application_id = request.data.get('application_id')
        try:
            receiverApplication = ReceiverApplication.objects.get(application_id=application_id, user_receiver_id=receiver_id)
            return Response({'status': receiverApplication.status}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Receiver Application not found'}, status=status.HTTP_404_NOT_FOUND)


class ConvertFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
    #     check file is pdf or docx
        file = request.FILES['file']
        file_name = file.name
        file_type = file_name.split('.')[-1]
        if file_type == 'pdf':
            pdf_file = request.FILES['file']

            ## Tạo đối tượng pdfplumber để đọc nội dung từ PDF
            with pdfplumber.open(pdf_file) as pdf:
                pdf_text = ""
                for page in pdf.pages:
                    pdf_text += page.extract_text()

            # Tạo mã HTML từ nội dung PDF
            html_content = re.sub(r'\n', '<br>', pdf_text)
            html_content = f"<html><body>{html_content}</body></html>"

            # Trả về response với nội dung HTML
            return HttpResponse(html_content)
        elif file_type == 'docx':
            docx_file = request.FILES['file']

            # Đọc nội dung từ tệp DOCX và chuyển thành HTML
            html_content = self.docx_to_html(docx_file)

            # Trả về response với nội dung HTML
            return HttpResponse(html_content, content_type='text/html')
    def docx_to_html(self, docx_file):
        doc = docx.Document(docx_file)
        html_content = "<html><body>"

        for paragraph in doc.paragraphs:
            # Kiểm tra các đoạn văn bản trong đoạn
            formatted_runs = self.apply_formatting(paragraph.runs)

            # Thêm đoạn văn bản vào nội dung HTML
            html_content += f"<p>{formatted_runs}</p>"

        html_content += "</body></html>"
        return html_content

    def apply_formatting(self, runs):
        formatted_text = ""

        for run in runs:
            text = run.text
            if run.bold:
                text = f"<b>{text}</b>"
            if run.italic:
                text = f"<i>{text}</i>"
            # Xử lý thêm các thuộc tính định dạng khác ở đây
            if run.underline:
                text = f"<u>{text}</u>"
            if run.font.highlight_color:
                text = f"<span style='background-color: {run.font.highlight_color};'>{text}</span>"
            if run.font.color.rgb:
                text = f"<span style='color: {run.font.color.rgb};'>{text}</span>"

            formatted_text += text

        return formatted_text


class SignPdf(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def generate_unique_filename(self, filename):
        # Tạo tên mới duy nhất bằng cách sử dụng uuid
        ext = filename.split('.')[-1]
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        return unique_filename
    def post(self, request,id):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        try:
            user = User.objects.get(id=payload['id'])
            application = Application.objects.get(id=id)
            username = user.username

            private_key_path = None
            certificate_path = None
            if 'private_key_file' in request.FILES and 'certificate_file' in request.FILES:
                private_key = request.FILES['private_key_file']
                certificate = request.FILES['certificate_file']
                private_key_name = self.generate_unique_filename(private_key.name)
                certificate_name = self.generate_unique_filename(certificate.name)
                private_key_path = 'tdtu_cntt2/private_key/' + private_key_name
                certificate_path = 'tdtu_cntt2/certificates/' + certificate_name
                with open(private_key_path, 'wb+') as destination:
                    for chunk in private_key.chunks():
                        destination.write(chunk)
                with open(certificate_path, 'wb+') as destination:
                    for chunk in certificate.chunks():
                        destination.write(chunk)

            else:
                private_key_path = 'tdtu_cntt2/private_key/' + user.private_key + '_private.pem'
                certificate_path = 'tdtu_cntt2/certificates/' + user.certificate + '_certificate.pem'
            signer = signers.SimpleSigner.load(private_key_path,
                                            certificate_path, ca_chain_files=None,
                                            key_passphrase=None, other_certs=None, signature_mechanism=None,
                                            prefer_pss=False)
            # save signature_img base64 to folder
            signature_img = request.data.get('signature_img')
            signature_img_name = self.generate_unique_filename(signature_img.name)
            signature_img_path = 'tdtu_cntt2/logostamp/' + signature_img_name
            with open(signature_img_path, 'wb+') as destination:
                for chunk in signature_img.chunks():
                    destination.write(chunk)

            # get path signature_img
            signature_img_path = 'tdtu_cntt2/logostamp/' + signature_img_name

            pdf_file = application.file_id.file.path
            with open(pdf_file, 'rb') as pdf_file:
                pdf_data = pdf_file.read()
            r = PdfFileReader(io.BytesIO(pdf_data), strict=False)
            # Calculate the new position based on the number of existing signatures
            num_existing_signatures = len(r.embedded_signatures)
            new_x_position = 400 - (num_existing_signatures * 10)  # Adjust this value as needed
            new_x_position -= 150  # Increase this value to add more separation
            new_box = (new_x_position, 50, new_x_position + 100, 10)  # Adjust the width as needed
            if num_existing_signatures == 0:
                new_box = (400, 50, 500, 10)
            else:
                new_box = (new_x_position, 50, new_x_position + 100, 10)

            name_file = pdf_file.name
            pdf_writer = IncrementalPdfFileWriter(io.BytesIO(pdf_data), strict=False)
            pyhanko_fields.append_signature_field(pdf_writer, sig_field_spec=pyhanko_fields.SigFieldSpec(username, box=new_box))

            meta = signers.PdfSignatureMetadata(field_name=username)
            pdf_signer = signers.PdfSigner(meta, signer, stamp_style=stamp.TextStampStyle(
                stamp_text='Signed by: %(signer)s\nTime: %(ts)s',
                text_box_style=text.TextBoxStyle(
                    font=opentype.GlyphAccumulatorFactory('tdtu_cntt2/textboxstyle/NotoSans-Bold.ttf')
                ),
                # use signature_img to background
                background= images.PdfImage(signature_img_path)
                # background=images.PdfImage('tdtu_cntt2/logostamp/logo.png')
            ),
            )
            with open(os.path.join('files', name_file), 'wb') as outf:
                pdf_signer.sign_pdf(pdf_writer, output=outf)
            # return HttpResponse(pdf_data, content_type='application/pdf')
            return Response({'message': 'Sign success'}, status=200)
        except Exception as e:
            return Response({'message': 'Please check your private key and certificate'}, status=400)


class ValidatePdfSignatureView(APIView):
    parser_classes = (MultiPartParser,)
    def post(self, request):
        payload = check_login(request)
        if isinstance(payload, Response):
            return payload
        user = User.objects.get(id=payload['id'])
        certificate_path = 'tdtu_cntt2/certificates/' + user.certificate + '_certificate.pem'
        # Load root certificate for validation
        root_cert = load_cert_from_pemder(certificate_path)
        vc = ValidationContext(trust_roots=[root_cert])

        # Get the uploaded PDF file from the request
        pdf_file = request.FILES['pdf_file']

        # Read the uploaded PDF file
        with pdf_file.open('rb') as doc:
            r = PdfFileReader(doc, strict=False)
            if len(r.embedded_signatures) == 0:
                return JsonResponse({'message': 'No signatures found in the PDF.'}, status=400)
            signature_data = []
            for sig in r.embedded_signatures:
            # sig = r.embedded_signatures[0]
                status = validate_pdf_signature(sig, vc)
                # Trích xuất thông tin từ phần "Certificate subject"
                match = re.search(r'Certificate subject: "Common Name: (.*), Organization: (.*), Country: (.*)"',
                              status.pretty_print_details())
                if match:
                    common_name = match.group(1)
                    organization = match.group(2)
                    country = match.group(3)
                else:
                    common_name = organization = country = "N/A"
                signature_info = {
                    'valid_signature': status.valid,  # kiểm tra hợp lệ của chữ ký
                    'pdf': status.intact,  # kiểm tra tính toàn vẹn của tệp PDF
                    'certificate': status.trusted,  # kiểm tra chứng chỉ
                    'common_name': common_name,
                    'organization': organization,
                    'country': country,
                    'details': status.pretty_print_details()
                    }
                signature_data.append(signature_info)
            return Response(signature_data, status=200)




