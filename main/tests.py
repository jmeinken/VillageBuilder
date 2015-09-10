from django.test import TestCase
from django.core.urlresolvers import reverse


class TestAccountCreationViews(TestCase):
    # fixtures = ['account_test.json']
    
    def test_call_account_info(self):
        '''Load account info page successful and required fields present'''
        response = self.client.get(reverse('account:account_info'))
        assert response.status_code == 200
        assert 'name="email"' in response.content
        assert 'name="first_name"' in response.content
        assert 'name="last_name"' in response.content
        assert 'name="password"' in response.content
        assert 'name="resubmit_password"' in response.content
        assert 'name="redirect-url"' in response.content
        
    def test_call_address(self):
        '''Load address page redirects to account_info'''
        response = self.client.get(reverse('account:address'), follow=True)
        self.assertRedirects(response, reverse('account:account_info'))
        
    def test_call_personal_info(self):
        '''Load Personal info page redirects to account_info'''
        response = self.client.get(reverse('account:personal_info'), follow=True)
        self.assertRedirects(response, reverse('account:account_info'))
        
    def test_whole_account_creation(self):
        '''Create account start to finish'''
        response = self.client.post(reverse('account:account_info'), {
           'email' : 'test@test.com',
           'first_name' : 'John',
           'last_name' : 'Meinken',
           'password' : 'qwerqwer',
           'resubmit_password' : 'qwerqwer', 
           'redirect-url' : '',                                                      
        }, follow=True)
        self.assertRedirects(response, reverse('account:address'))
        
        assert 'name="full_address"' in response.content
        assert 'name="street"' in response.content
        assert 'name="city"' in response.content
        assert 'name="neighborhood"' in response.content
        assert 'name="state"' in response.content
        assert 'name="zip_code"' in response.content
        assert 'name="latitude"' in response.content
        assert 'name="longitude"' in response.content   
        assert 'name="redirect-url"' in response.content
        
        response = self.client.post(reverse('account:address'), {
           'full_address' : '123 Fake St., Cincinnati, OH 45220',
           'street' : '123 Fake St.',
           'city' : 'Cincinnati',
           'neighborhood' : 'Wick Park',
           'state' : 'OH',
           'zip_code' : '45220',
           'latitude' : '81.155590',
           'longitude' : '-127.14321',
           'redirect-url' : '',                                                       
        }, follow=True)
        self.assertRedirects(response, reverse('account:personal_info'))
        
        assert 'name="email"' in response.content   
        assert 'name="first_name"' in response.content   
        assert 'name="last_name"' in response.content   
        assert 'name="password"' in response.content   
        assert 'name="resubmit_password"' in response.content   
        assert 'name="image"' in response.content   
        assert 'name="thumb"' in response.content   
        assert 'name="state"' in response.content   
        assert 'name="zip_code"' in response.content   
        assert 'name="full_address"' in response.content   
        assert 'name="street"' in response.content   
        assert 'name="city"' in response.content   
        assert 'name="neighborhood"' in response.content   
        assert 'name="share_street"' in response.content   
        assert 'name="share_email"' in response.content   
        
        response = self.client.post(reverse('account:personal_info'), {
           'email' : 'test@test.com',
           'first_name' : 'John',
           'last_name' : 'Meinken',
           'password' : 'qwerqwer',
           'resubmit_password' : 'qwerqwer',    
           'image' : '',
           'thumb' : '',
           'state' : 'OH',
           'zip_code' : '45220',    
           'full_address' : '123 Fake St., Cincinnati, OH 45220',
           'street' : '123 Fake St.',
           'city' : 'Cincinnati',
           'neighborhood' : 'Wick Park',    
           'share_street' : True,
           'share_email' : True,                                        
        }, follow=True)
        assert response.status_code == 200
        self.assertRedirects(response, reverse('home'))
 
        
class TestLoggedInViews(TestCase):
    fixtures = ['test_data.json']
    
    def test_login_page(self):
        response = self.client.get(reverse('login'))
        assert response.status_code == 200
        
    def test_login(self):
        response = self.client.post(reverse('login'), {
           'username' : 'test@test.com',
           'password' : 'qwerqwer',                                            
        }, follow=True)
        self.assertRedirects(response, reverse('home'))
        
    def test_failed_login(self):
        response = self.client.post(reverse('login'), {
           'username' : 'test@test.com',
           'password' : 'qwerqwerqwer',                                            
        })
        assert response.status_code == 200      # doesn't redirect
        
    def test_account_view(self):
        self.client.login(username='test@test.com', password='qwerqwer')
        response = self.client.get( reverse('account:view', args=[1]) )
        assert response.status_code == 200
        
    def test_sharing_items_view(self):
        self.client.login(username='test@test.com', password='qwerqwer')
        response = self.client.get( reverse('sharing:items') )
        assert response.status_code == 200
        
    def test_sharing_my_items_view(self):
        self.client.login(username='test@test.com', password='qwerqwer')
        response = self.client.get( reverse('sharing:my_items') )
        assert response.status_code == 200
        
    def test_sharing_share_item_view(self):
        self.client.login(username='test@test.com', password='qwerqwer')
        response = self.client.get( reverse('sharing:share_item') )
        assert response.status_code == 200
        
    def test_relationships_relationships_view(self):
        self.client.login(username='test@test.com', password='qwerqwer')
        response = self.client.get( reverse('relationships:relationships') )
        assert response.status_code == 200
        
    def test_pm_messages_view(self):
        self.client.login(username='test@test.com', password='qwerqwer')
        response = self.client.get( reverse('pm:messages', args=[0]) )
        assert response.status_code == 200
        
    def test_account_account_view(self):
        self.client.login(username='test@test.com', password='qwerqwer')
        response = self.client.get( reverse('account:account') )
        assert response.status_code == 200
        
from django.test import TestCase

# Create your tests here.
