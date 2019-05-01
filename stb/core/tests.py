from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from collections import OrderedDict

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
        cls.user2 = User.objects.create_user(
            username='linda',
            email='linda@nasa.gov',
            password='linda-terminator'
        )
        cls.user3 = User.objects.create_user(
            username='arnold',
            email='arnold@nasa.gov',
            password='terminator'
        )

        # Profile, Skill & Project I
        cls.profile = Profile.objects.get(user=cls.user)
        cls.profile.full_name = 'John Connor'
        cls.profile.save()

        skill = Skill()
        skill.save()
        skill.profile.add(cls.profile.id)
        skill.title = 'rails'
        skill.save()

        cls.project = Project.objects.create(
            profile=cls.profile,
            title='NASA JPL',
        )
        cls.position_user1 = Position.objects.create(
            project=cls.project,
            title='Python Developer',
            description='Python Development is...',
        )
        cls.position2_user1 = Position.objects.create(
            project=cls.project,
            title='iOS Developer',
            description='iOS Development is...',
        )

        # Profile, Skill & Project II
        cls.profile2 = Profile.objects.get(user=cls.user2)

        skill = Skill()
        skill.save()
        skill.profile.add(cls.profile2.id)
        skill.title = 'python'
        skill.save()

        cls.project2 = Project.objects.create(
            profile=cls.profile2,
            title='SPACE X',
        )
        cls.position_user2 = Position.objects.create(
            project=cls.project2,
            title='Rails Developer',
            description='Rails Development is...',
        )
        cls.position2_user2 = Position.objects.create(
            project=cls.project2,
            title='Android Developer',
            description='Android Development is...',
        )

        cls.profile3 = Profile.objects.get(user=cls.user3)

        skill = Skill()
        skill.save()
        skill.profile.add(cls.profile3.id)
        skill.title = 'iOS'
        skill.save()

        cls.project3 = Project.objects.create(
            profile=cls.profile3,
            title='Digital Imaging',
        )
        cls.position_user3 = Position.objects.create(
            project=cls.project3,
            title='Rails Developer',
            description='Rails Development is...',
        )
        cls.position2_user3 = Position.objects.create(
            project=cls.project3,
            title='Python Developer',
            description='Python Development is...',
        )


    def setUp(self):
        self.client.login(username='johnconnor', password='terminator')


    def test_create_account(self):
        self.user = User.objects.get(email='dude@nasa.gov')
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
                'title': 'BLACK HOLE DISCOVERY',
                'position_formset-TOTAL_FORMS': 1,
                'position_formset-INITIAL_FORMS': 0,
                'position_formset-0-title': 'Rails Developer',
                'position_formset-0-description': 'description',
            },
        )
        project = Project.objects.get(id=4)
        position = Position.objects.filter(project=project)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(project.title, 'BLACK HOLE DISCOVERY')
        self.assertEqual(position[0].title, 'Rails Developer')

    def test_edit_project(self):
        url = '/project/1/edit/'
        response = self.client.put(
            url,
            data={
                'profile': self.profile,
                'title': 'BLACK HOLE DISCOVERY',
                'position_formset-TOTAL_FORMS': '3',
                'position_formset-INITIAL_FORMS': '2',
                'position_formset-0-title': 'Rails Developer',
                'position_formset-0-description': 'description',
                'position_formset-0-availability': '',
                'position_formset-1-title': 'Rails Developer',
                'position_formset-1-description': 'Rails Description',
                'position_formset-1-availability': '',
                'position_formset-2-title': 'C4D Developer',
                'position_formset-2-description': 'C4D Description',
                'position_formset-2-availability': '',
            },
        )
        project = Project.objects.get(title='BLACK HOLE DISCOVERY')
        position = Position.objects.filter(project=project)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(project.title, 'BLACK HOLE DISCOVERY')
        self.assertEqual(position[2].title, 'C4D Developer')

    def test_homepage(self):
        url = '/'
        response = self.client.get(
            url,
            data={},
        )
        self.assertEqual(response.context[-1]['projects'].count(), 3)
        self.assertEqual(response.context[-1]['positions'].count(), 4)
        self.assertEqual(response.status_code, 200)

    def test_homepage_term(self):
        url = '/?q=NASA'
        response = self.client.get(
            url,
            data={},
        )
        self.assertEqual(response.context[-1]['projects'][0].title, 'NASA JPL')
        self.assertEqual(response.status_code, 200)

    def test_homepage_no_term(self):
        url = '/?q='
        response = self.client.get(
            url,
            data={},
        )
        project = Project.objects.all()
        count = project.count()
        self.assertEqual(response.context[-1]['projects'].count(), count)
        self.assertEqual(response.status_code, 200)

    """
    NEED TO FIGURE SKILL IS THROUGH TABLE!
    def test_profile_update(self):
        url = '/profile/1/edit/'
        response = self.client.put(
            url,
            data={
                'full_name': 'Joe Black',
                'description': 'Is coding...',
                'avatar': '',
                'other_skills': '',
                'Skill_profile-TOTAL_FORMS': 4,
                'Skill_profile-INITIAL_FORMS': 1,
                'project_formset-TOTAL_FORMS': 2,
                'project_formset-INITIAL_FORMS': 1,
                'Skill_profile-0-title': 'Rails Developer',
                'Skill_profile-0-description': 'description',
            },
        )
        print(response.context)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.profile.full_name, 'Joe Black')
        self.assertEqual(self.profile.description, 'Is coding...')
    """

    def test_profile_view(self):
        url = '/profile/1/'
        response = self.client.get(
            url,
            data={},
        )
        self.assertEqual(response.context[-1]['profile'].full_name, 'John Connor')
        self.assertEqual(response.status_code, 200)

    def test_profile_someone_else_update(self):
        url = '/profile/2/edit/'
        response = self.client.put(
            url,
            data={
                'full_name': 'Joe Black',
                'description': 'Is coding...',
                'Skill_profile-TOTAL_FORMS': 4,
                'Skill_profile-INITIAL_FORMS': 1,
                'project_formset-TOTAL_FORMS': 2,
                'project_formset-INITIAL_FORMS': 1,
            },
        )
        self.assertEqual(response.status_code, 404)

    def test_project_view(self):
        url = '/project/1/'
        response = self.client.get(
            url,
            data={},
        )
        self.assertEqual(response.context[-1]['project'].title, 'NASA JPL')
        self.assertEqual(response.status_code, 200)


    def test_applications_empty(self):
        url = '/applications/'
        response = self.client.get(
            url,
            data={},
        )
        self.assertEqual(response.context[-1]['applicant_dict'], OrderedDict())
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
