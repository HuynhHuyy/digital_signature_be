from django.urls import path, include

from tdtu_cntt2.views.adminviews import *
from tdtu_cntt2.views.userviews import *

urlpatterns = [
    # User url
    path('login/', LoginView.as_view(), name='login'),
    path('first-login/', FirstTimeLoginView.as_view(), name='first-login'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('add-receiver/', AddReceiverAPIView.as_view(), name='add-receiver'),
    path('search/', PublisherApplicationView.as_view({'get': 'list'}), name='search-applications'),
    # Admin url
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin-login/', AdminLogin.as_view(), name='admin-login'),
    path('admin-change-password/', ChangePasswordAdmin.as_view(), name='admin-change-password'),
    path('add-user/', AddUserView.as_view(), name='add-user'),
    path('update-user/<int:id>/', UpdateUser.as_view(), name='update-user'),
    path('delete-user/<int:id>/', DeleteUser.as_view(), name='delete-user'),
    path('get-user/', GetAllUser.as_view(), name='get-user'),
    # ResetPassword
    path('users/<int:user_id>/reset-password/', ResetPassword.as_view(), name='reset-password'),
    # Process
    path('process/create/', ProcessCreateView.as_view(), name='process-create'),
    path('processes/<int:process_id>/', ProcessUpdateView.as_view(), name='process-update'),
    path('delete-process/<int:process_id>/', DeleteProcess.as_view(), name='process-delete'),
    path('process/<int:process_id>/', ProcessDetailByIdView.as_view(), name='process-detail-by-id'),
    path('processes/', ProcessListView.as_view(), name='process-list'),
    # Step
    path('step/create/', StepCreateView.as_view(), name='step-create'),
    path('steps/<int:step_id>/', StepUpdateView.as_view(), name='step-update'),
    path('delete-step/<int:step_id>/', DeleteStep.as_view(), name='step-delete'),
    path('step-info/<int:step_id>/', StepDetailView.as_view(), name='step-detail'),
    path('steps-list/', StepListView.as_view(), name='step-list'),
    # Role url
    path('add-role/', AddRole.as_view(), name='add-role'),
    path('update-role/<int:id>/', UpdateRole.as_view(), name='update-role'),
    path('delete-role/<int:id>/', DeleteRole.as_view(), name='delete-role'),
    path('get-role/', GetAllRole.as_view(), name='get-role'),
    # Department url
    path('add-department/', AddDepartment.as_view(), name='add-department'),
    path('update-department/<int:id>/', UpdateDepartment.as_view(), name='update-department'),
    path('delete-department/<int:id>/', DeleteDepartment.as_view(), name='delete-department'),
    path('get-department/', GetAllDepartment.as_view(), name='get-department'),
    # Application url
    path('add-application/', AddApplication.as_view(), name='add-application'),
    path('delete-application/<int:id>/', DeleteApplication.as_view(), name='delete-application'),
    path('get-application/', GetAllApplication.as_view(), name='get-application'),
    path('get-public-application/', GetPublicApplication.as_view(), name='get-public-application'),
    path('update-receiver/<int:id>/', UpdateReceiverAPIView.as_view(), name='update-receiver'),
    path('update-sender/<int:id>/', UpdateSenderAPIView.as_view(), name='update-sender'),
    path('update-status-receiver/<int:id>/', UpdateStatusReceiverAPIView.as_view(), name='update-status-receiver'),
    path('count-application-receiver/', CountApplicationReceiver.as_view(), name='count-application-receiver'),
    path('get-application-receiver/', AllReceiverApplicationList.as_view(), name='get-application-receiver'),
    path('get-application-sender/', ApplicationSenderList.as_view(), name='get-application-sender'),
    path('get-receiveid-by-applicationid/<int:application_id>/', GetAllReceiveIdByApplicationId.as_view(), name='get-receiveid-by-applicationid'),
    path('get-receive-by-applicationid/<int:application_id>/', GetAllReceiveByApplicationId.as_view(), name='get-receive-by-applicationid'),
    path('get-application-by-id/<int:id>/', GetApplicationById.as_view(), name='get-application-by-id'),
    path('get-status-by-application-receive/', GetStatusByApplicationUserReceiveId.as_view(), name='get-status-by-application-receive'),
    path('public-application/<int:id>/', PublicApplication.as_view(), name='public-application'),
    path('unpublic-application/<int:id>/', UnPublicApplication.as_view(), name='unpublic-application'),
    # Signature url
    path('add-signature/', SignatureCreateView.as_view(), name='add-signature'),
    path('delete-signature/<int:id>/', SignatureDelete.as_view(), name='delete-signature'),
    path('get-signature/', SignatureList.as_view(), name='get-signature'),
    #file
    path('upload-file/', FileUploadView.as_view(), name='file-upload'),
    path('load-file/<int:id>/', LoadFileView.as_view(), name='load-file'),
    path('convert-to-text/', ConvertFileView.as_view(), name='convert-to-text'),
    path('sign-pdf/<int:id>/', SignPdf.as_view(), name='py-read'),
    path('validate-pdf-signature', ValidatePdfSignatureView.as_view(), name='validate-pdf-signature'),
]

