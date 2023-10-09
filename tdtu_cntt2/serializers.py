from rest_framework import serializers
from tdtu_cntt2.models import *
from .search_indexes import *
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

class UserSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role_id.name', read_only=True)
    role_description = serializers.CharField(source='role_id.description', read_only=True)
    department_name = serializers.CharField(source='department_id.name', read_only=True)
    department_description = serializers.CharField(source='department_id.description', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'full_name', 'username', 'password', "role_id", "role_name", "role_description",
                  "department_id", "department_name", "department_description", "private_key", "public_key","certificate"]

    def create(self, validated_data):
        username = validated_data['username']
        full_name = validated_data['full_name']
        password = validated_data.get('password', username)
        validated_data['password'] = username
        role_id = validated_data['role_id']
        department_id = validated_data['department_id']
        private_key = validated_data['private_key']
        public_key = validated_data['public_key']
        certificate = validated_data['certificate']
        user = User.objects.create_user(username=username, password=password, full_name=full_name, role_id=role_id,
                                        department_id=department_id, private_key=private_key, public_key=public_key,certificate=certificate)
        user.save()
        return user
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'username','password', 'role_id', 'department_id']
class RoleSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department_id.name', read_only=True)
    class Meta:
        model = Role
        fields = ['id', 'name', 'description','department_id','department_name']
class DepartmentSerializer(serializers.ModelSerializer):
    total_user = serializers.SerializerMethodField(read_only=True)

    def get_total_user(self, obj):
        return User.objects.filter(department_id=obj.id).count()

    class Meta:
        model = Departments
        fields = ['total_user', 'id', 'name', 'description']
class ApplicationSerializer(serializers.ModelSerializer):
    process_name = serializers.CharField(source='process_id.name', read_only=True)
    sender_name = serializers.CharField(source='sender_id.full_name', read_only=True)
    class Meta:
        model = Application
        fields = ['id', 'title', 'content', 'sender_id','status','delete_by_sender','process_id','process_name','sender_name','created_at','updated_at','file_id','pdf_content','is_public']
class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = ['id', 'name', 'description']
class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['id', 'name', 'process_id','department_id', 'role_id', 'user_id']
class StepDetailSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user_id.username')
    user_id = serializers.CharField(source='user_id.id')
    user_full_name = serializers.CharField(source='user_id.full_name')
    role_name = serializers.CharField(source='role_id.name')

    class Meta:
        model = Step
        fields = ['id', 'name', 'user_name','user_id', 'role_name', 'user_full_name']
class SignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signature
        fields = ['id', 'signature','user_id']
class ReceiverSerializer(serializers.ModelSerializer):
    user_receiver_name = serializers.CharField(source='user_receiver_id.full_name', read_only=True)
    class Meta:
        model = ReceiverApplication
        fields = ['id','application_id', 'user_receiver_id','delete', 'status','user_receiver_name','updated_at']
class SearchApplicationSerializer(DocumentSerializer):
    class Meta:
        model = Application
        document = ApplicationDocument
        fields = ('id', 'title', 'content', 'sender_id','user_receiver_id','delete_by_sender','user_receive','pdf_content')


#file
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ['id' ,'file','user_id']
class AdminLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminAccounts
        fields = ['id','username','password']