from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver



class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The username field must be set')
        username = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        if password is not None:
            user.password = password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)
class Departments(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Role(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    department_id = models.ForeignKey(Departments, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class User(AbstractBaseUser):
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    role_id = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    department_id = models.ForeignKey(Departments, on_delete=models.SET_NULL, null=True)
    private_key = models.TextField(default=None, null=True)
    public_key = models.TextField(default=None, null=True)
    certificate = models.TextField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()
class AdminAccounts(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    password = models.TextField()
    last_login = models.DateTimeField(null=True, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    email = None
    is_staff = None
    is_superuser = None
    is_active = None
    first_name = None
    last_name = None
    date_joined = None

class ProcessManager(models.Manager):
    pass
class StepManager(models.Manager):
    pass
class Process(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    objects = ProcessManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Step(models.Model):
    name = models.CharField(max_length=255)
    process_id = models.ForeignKey(Process, on_delete=models.SET_NULL, null=True)
    department_id = models.ForeignKey(Departments, on_delete=models.SET_NULL, null=True)
    role_id = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    objects = StepManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Signature(models.Model):
    signature = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Application(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    status = models.IntegerField(default=0)
    sender_id = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    process_id = models.ForeignKey(Process, on_delete=models.SET_NULL, default=None, null=True)
    delete_by_sender = models.BooleanField(default=False)
    # signature = models.TextField(default=None, null=True)
    pdf_content = models.TextField(default=None, null=True)
    file_id = models.ForeignKey('Files', on_delete=models.SET_NULL, default=None, null=True)
    # digital_signature = models.TextField(default=None, null=True)
    is_public = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_user_receiver_id(self):
        try:
            receiver_applications = ReceiverApplication.objects.filter(application_id=self.id)
            user_receiver_ids = receiver_applications.values_list('user_receiver_id', flat=True)
            return list(user_receiver_ids)
        except ObjectDoesNotExist:
            return None

class ReceiverApplication(models.Model):
    application_id = models.ForeignKey(Application, on_delete=models.SET_NULL, default=None, null=True)
    user_receiver_id = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    status = models.IntegerField(default=0)
    # signature = models.TextField(default=None, null=True)
    delete = models.BooleanField(default=False)
    # digital_signature = models.TextField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Files(models.Model):
    name = models.TextField()
    file = models.FileField(upload_to='files/')
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
@receiver(post_save, sender=ReceiverApplication)
def update_application_status(sender, instance, **kwargs):
    application = instance.application_id
    receiver_statuses = ReceiverApplication.objects.filter(application_id=application)
    unique_statuses = set(receiver_statuses.values_list('status', flat=True))
    # Tất cả các giá trị status đều = 1
    if len(unique_statuses) == 1 and 1 in unique_statuses:
        application.status = 2
    # Nếu có 1 giá trị = 2 thì status của application là 3
    elif 2 in unique_statuses:
        application.status = 3
    # Nếu có 1 giá trị = 1 và 1 giá trị = 0 thì status của application là 1
    elif 1 in unique_statuses and 0 in unique_statuses:
        application.status = 1
    else:
        application.status = 0  # Hoặc giá trị khác tùy thuộc vào logic của bạn
    application.save()

