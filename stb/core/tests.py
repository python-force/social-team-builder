from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from collections import OrderedDict
from django.contrib.messages import get_messages

from stb.core.models import Profile, Skill, Project, Position, Position_Application

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

        """
        User 1 Applying for User 2 Project
        Position id = 3
        project=cls.project2,
        title='Rails Developer',
        description='Rails Development is...',
        :return:
        """
        # Applied for the Project
        url = '/project/2/apply/3/'
        self.client.get(url, data={})


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

    """
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
    """

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


    def test_apply_position_view(self):
        
        # Applied for the Project
        url = '/project/2/apply/4/'
        response = self.client.get(
            url,
            data={},
        )
        position = Position_Application.objects.filter(position_id=4)
        self.assertEqual(position.count(), 1)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), 'You have now applied for Android Developer.')



    def test_apply_for_same_position_view(self):

        # Applied for the same one
        url = '/project/2/apply/3/'
        response = self.client.get(
            url,
            data={},
        )
        position = Position_Application.objects.filter(position_id=3)
        self.assertEqual(position.count(), 1)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), 'You have already applied for Rails Developer position')


    def test_apply_for_my_own_position_view(self):

        url = '/project/1/apply/2/'
        response = self.client.get(
            url,
            data={},
        )
        position = Position_Application.objects.filter(position_id=3)
        self.assertEqual(position.count(), 1)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), 'You cannot apply for your own iOS Developer position')


    def test_apply_was_hired_view(self):

        position = Position_Application.objects.get(position_id=3)
        position.status = 1
        position.save()

        url = '/project/2/apply/3/'
        response = self.client.get(
            url,
            data={},
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), 'You were hired already for the Rails Developer position')

    def test_apply_was_rejected_view(self):

        position = Position_Application.objects.get(position_id=3)
        position.status = 2
        position.save()

        url = '/project/2/apply/3/'
        response = self.client.get(
            url,
            data={},
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), 'You were rejected already for the Rails Developer position')

    def test_cancel_apply_position_view(self):

        self.test_apply_position_view()

        # Cancel Apply for the project

        url = '/project/2/cancel-apply/4/'
        response = self.client.get(
            url,
            data={},
        )
        positions = Position_Application.objects.all()
        self.assertEqual(positions.count(), 1)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[2]), 'You have canceled the application.')

    def test_cancel_apply_position_already_hired_view(self):

        self.test_apply_position_view()

        # Cancel Apply for the project already hired
        position = Position_Application.objects.get(position_id=4)
        position.status = 1
        position.save()

        url = '/project/2/cancel-apply/4/'
        response = self.client.get(
            url,
            data={},
        )
        positions = Position_Application.objects.all()
        self.assertEqual(positions.count(), 2)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[2]), 'You were already hired for the Android Developer position. Too late buddy!')

    def test_cancel_apply_position_already_rejected_view(self):

        self.test_apply_position_view()

        # Cancel Apply for the project already rejected
        position = Position_Application.objects.get(position_id=4)
        position.status = 2
        position.save()

        url = '/project/2/cancel-apply/4/'
        response = self.client.get(
            url,
            data={},
        )
        positions = Position_Application.objects.all()
        self.assertEqual(positions.count(), 2)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[2]), 'You were already rejected for the Android Developer position. Too late buddy!')

    def test_cancel_apply_position_never_applied_view(self):

        url = '/project/2/cancel-apply/4/'
        response = self.client.get(
            url,
            data={},
        )
        positions = Position_Application.objects.all()
        self.assertEqual(positions.count(), 1)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), 'You have never applied for the Android Developer position. Maybe you should consider.')

    def test_accept_profile_position(self):
        """
        project=cls.project2,
        title='Rails Developer',
        description='Rails Development is...',
        :return:
        """

        self.client.login(username='linda', password='linda-terminator')

        url = '/profile/1/accept/3/'
        response = self.client.get(
            url,
            data={},
        )
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[1]), 'Applicant John Connor was accepted for the Rails Developer position')

    def test_accept_profile_position_already_hired_view(self):
        """
        project=cls.project2,
        title='Rails Developer',
        description='Rails Development is...',
        :return:
        """

        self.test_accept_profile_position()

        url = '/profile/1/accept/3/'
        response = self.client.get(
            url,
            data={},
        )
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[2]), 'The Rails Developer position was already filled')

    def test_accept_profile_with_no_position_applied(self):
        """
        project=cls.project2,
        title='Rails Developer',
        description='Rails Development is...',
        :return:
        """

        self.client.login(username='linda', password='linda-terminator')

        url = '/profile/1/accept/5/'
        response = self.client.get(
            url,
            data={},
        )
        self.assertEqual(response.status_code, 404)

    def test_applications_list_view(self):

        self.client.login(username='linda', password='linda-terminator')

        url = '/applications/'
        response = self.client.get(
            url,
            data={},
        )
        for key, value in response.context[-1]['applicant_dict'].items():
            self.assertEqual(key, 9)
            self.assertEqual(value[0].username, 'johnconnor')
            self.assertEqual(value[1].title, 'SPACE X')
            self.assertEqual(value[2].title, 'Rails Developer')
            self.assertEqual(value[3], 0)
        self.assertEqual(response.status_code, 200)

    def test_applications_list_status_view(self):

        self.client.login(username='linda', password='linda-terminator')

        url = '/applications/new-applications/'
        response = self.client.get(
            url,
            data={},
        )
        for key, value in response.context[-1]['applicant_dict'].items():
            self.assertEqual(key, 8)
            self.assertEqual(value[0].username, 'johnconnor')
            self.assertEqual(value[1].title, 'SPACE X')
            self.assertEqual(value[2].title, 'Rails Developer')
            self.assertEqual(value[3], 0)
        self.assertEqual(response.status_code, 200)

    def test_applications_list_project_view(self):

        self.client.login(username='linda', password='linda-terminator')

        url = '/applications/project/2/'
        response = self.client.get(
            url,
            data={},
        )
        for key, value in response.context[-1]['applicant_dict'].items():
            self.assertEqual(key, 7)
            self.assertEqual(value[0].username, 'johnconnor')
            self.assertEqual(value[1].title, 'SPACE X')
            self.assertEqual(value[2].title, 'Rails Developer')
            self.assertEqual(value[3], 0)
        self.assertEqual(response.status_code, 200)

    def test_applications_list_project_0_view(self):

        self.client.login(username='linda', password='linda-terminator')

        url = '/applications/project/3/'
        response = self.client.get(
            url,
            data={},
        )
        self.assertEqual(response.context[-1]['applicant_dict'], OrderedDict())
        self.assertEqual(response.status_code, 200)

    def test_applications_list_position_view(self):

        self.client.login(username='linda', password='linda-terminator')

        url = '/applications/position/3/'
        response = self.client.get(
            url,
            data={},
        )
        for key, value in response.context[-1]['applicant_dict'].items():
            self.assertEqual(key, 5)
            self.assertEqual(value[0].username, 'johnconnor')
            self.assertEqual(value[1].title, 'SPACE X')
            self.assertEqual(value[2].title, 'Rails Developer')
            self.assertEqual(value[3], 0)
        self.assertEqual(response.status_code, 200)