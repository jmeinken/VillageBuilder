from django.core.urlresolvers import reverse

from villagebuilder.settings import BASE_DIR

# used by account creation views to render wizard navigation
def build_nav(request, current_view):
    if current_view == 'account_info':
        nav_account_info = { 'label' : 'Account Info', 'class_attr' : 'active disabled' }
        nav_complete = { 'label' : 'Confirmation', 'class_attr' : 'disabled' }
        if 'account_info' in request.session.keys():
            nav_address = { 'label' : 'Address', 'link' : reverse('account:address') }
        else:
            nav_address = { 'label' : 'Address', 'class_attr' : 'disabled' }
        if 'address'  in request.session.keys():
            nav_personal_info = { 'label' : 'Personal Info and Privacy Settings', 'link' : reverse('account:personal_info') }
        else:
            nav_personal_info = { 'label' : 'Personal Info and Privacy Settings', 'class_attr' : 'disabled' }
    if current_view == 'address':
        nav_address = { 'label' : 'Address', 'class_attr' : 'active disabled' }
        nav_complete = { 'label' : 'Confirmation', 'class_attr' : 'disabled' }
        nav_account_info = { 'label' : 'Account Info', 'link' : reverse('account:account_info') }
        if 'address'  in request.session.keys():
            nav_personal_info = { 'label' : 'Personal Info and Privacy Settings', 'link' : reverse('account:personal_info') }
        else:
            nav_personal_info = { 'label' : 'Personal Info and Privacy Settings', 'class_attr' : 'disabled' }   
    if current_view == 'personal_info':
        nav_account_info = { 'label' : 'Account Info', 'link' : reverse('account:account_info') }
        nav_complete = { 'label' : 'Confirmation', 'class_attr' : 'disabled' }
        nav_address = { 'label' : 'Address', 'link' : reverse('account:address') }
        nav_personal_info = { 'label' : 'Personal Info and Privacy Settings', 'class_attr' : 'active disabled' }
    return [nav_account_info, nav_address, nav_personal_info, nav_complete]

def handle_uploaded_file(f):
    indexPath = BASE_DIR + '/main/static/uploads/user_pics.txt'
    indexFile = open(indexPath, 'a+')
    i = indexFile.read()
    indexFile.close()
    indexFile = open(indexPath, 'w')
    if i == '':
        j = 0
    else:
        j = 1 + int(i)
    indexFile.write(str(j))
    indexFile.close()
    fileName = 'user' + str(j) + '.png'
    path = BASE_DIR + '/main/static/uploads/user_pics/' + fileName
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return {
        'path' : '/static/uploads/user_pics/' + fileName,
        'file' : fileName,
    }
    
def ifkeyset(arr, key, ifempty='', ifset='[+]'):
    if key in arr.keys():
        return ifset.replace('[+]', str(arr[key]))
    else:
        return ifempty
    
    
    
    
    
    
    
    
    
    