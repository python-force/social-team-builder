from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from stb.core.models import Profile, Skill, Project, Position

# TO DO
# Cannot change stuff when not logged in AnonymousUSER
# Create automatic project URL

class EntireAppTest(TestCase):

    """Updating Profile"""

    @classmethod
    def setUpClass(cls):
        """Creating User"""
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='johnconnor',
            email='dude@nasa.gov',
            password='terminator'
        )
        cls.profile = Profile.objects.get(user=cls.user)
        skill = Skill()
        skill.save()
        skill.profile.add(cls.profile.id)
        skill.title='python'
        skill.save()

    def setUp(self):
        self.client.login(username='johnconnor', password='terminator')


    def test_create_account(self):
        self.user = User.objects.get(email='dude@nasa.gov')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.username, 'johnconnor')
        self.assertEqual(self.user.email, 'dude@nasa.gov')


    def test_create_profile(self):
        self.profile = Profile.objects.get(user=self.user)
        now = timezone.now()
        self.assertLess(self.profile.pub_date, now)

    def test_create_project(self):
        url = '/project/new/'
        response = self.client.post(
            url,
            data={
                'profile': self.profile,
                'title': 'NASA JPL',
                'position_formset-TOTAL_FORMS': 1,
                'position_formset-INITIAL_FORMS': 0,
                'position_formset-0-title': 'Python Developer',
                'position_formset-0-description': 'description',
            },
        )
        project = Project.objects.get(id=1)
        position = Position.objects.get(project=project)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(project.title, 'NASA JPL')
        self.assertEqual(position.title, 'Python Developer')

    def test_homepage(self):
        url = '/'
        response = self.client.get(
            url,
            data={},
        )
        positions = Position.objects.all()
        project = Project.objects.all()
        print(project)
        print(positions)
        # print(response.context)
        self.assertEqual(response.status_code, 200)


    """
    def test_update_profile(self):

        url = '/profile/3/edit/'
        data = {"full_name": "John Doe",
                "description": "He likes to fly",
                "other_skills": "Kiteboarding, Technology",}
        response = self.client.put(url, data)
        print(response.status_code)

        

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.user.username, 'johnconnor')
        self.assertEqual(self.profile.bio, 'About John')
     
        self.profile = Profile.objects.get(user=self.user)
        self.profile.full_name = 'John Doe'
        self.profile.description = 'He likes to fly',
        self.profile.other_skills = 'Kiteboarding, Technology',
        self.profile.save()
        self.profile.refresh_from_db()
        now = timezone.now()
        self.assertLess(self.profile.pub_date, now)
        self.assertLess(self.profile.other_skills, 'Kiteboarding, Technology')

 




    Profile View
    def test_profile_view(self):
        
        # reverse('profile', 3)
        self.client = Client()
        print(self.profile)
        response = self.client.get('/profile/3/')
        self.assertEqual(response.status_code, 200)
        # print(response.context['profile'].full_name)
        #self.assertEqual(response.context[-1]['profile'].full_name, 'John Doe')
        ##self.assertEqual(response.context[-1]['skills'], '')
        #self.assertEqual(response.context[-1]['projects'], '')
        #self.assertEqual(response.context[-1]['approved_projects'], '')

"""
