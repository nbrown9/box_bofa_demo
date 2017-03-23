from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login
from boxsdk import JWTAuth
from boxsdk import Client
from StringIO import StringIO
from boxsdk.object.collaboration import CollaborationRole
from boxsdk.exception import BoxAPIException
import os



auth = JWTAuth(
    client_id='00000000',
    client_secret='00000000',
    enterprise_id='00000000',
    jwt_key_id='00000000',
    rsa_private_key_file_sys_path='loans/private_key.pem',
    rsa_private_key_passphrase='00000000',
)

access_token = auth.authenticate_instance()
client = Client(auth)

ned_stark_user = client.create_user('Phillip Fry')


ned_auth = JWTAuth(
    client_id='00000000',
    client_secret='00000000',
    enterprise_id='00000000',
    jwt_key_id='00000000',
    rsa_private_key_file_sys_path='loans/private_key.pem',
    rsa_private_key_passphrase='00000000',
)

ned_auth.authenticate_app_user(ned_stark_user)
ned_client = Client(ned_auth)

#phil_fry_user = client.create_user('Phil Fry',user_id='10000')

#file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'file.txt')
#print(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media'))

me = ned_client.user(user_id='me').get()
print 'user_login: ' + me['login']
print 'uname: ' + me['name']



loan_folder = ned_client.folder(folder_id='0').create_subfolder(str(me['name']+' - Loan Application'))
upload_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media')


def apply(request):

    ned_root_folder = ned_client.folder(folder_id='0')

    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        dir_file = os.path.join(upload_path, filename)
        a_file = loan_folder.upload(dir_file, file_name='LoanApplication.pdf')

        try:
            collaboration = loan_folder.add_collaborator(u'nlbrown@syr.edu', CollaborationRole.CO_OWNER)
            try:
                my_meta_data = a_file.metadata()
                my_meta_data.create({'Status':'Processing'})
            finally:
                print('Created metadata: {0}'.format(my_meta_data.get()))
        finally:
            print 'hello'
        return render(request, 'loans/upload.html')
            # delete or change 
    return render(request, 'loans/apply.html')


def index(request):
    return render(request, 'loans/index.html')

def upload(request):
    if a_file['Loan Status'] == 'Approved':
        return render(request, 'loans/approved.html')
    return render(request, 'loans/upload.html')

def approved(request):
    return render(request, 'loans/approved.html')
