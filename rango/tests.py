import os
from django.test import TestCase
from django.urls import reverse
from populate_rango import populate
from django.contrib.auth.models import User
from django.forms import fields as django_fields

from rango import forms
from rango.models import Page, Category, Comment, Like, Mark
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm, CommentForm

# Create your tests here.

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

f"{FAILURE_HEADER} {FAILURE_FOOTER}"

def create_user_object():
    """
    Helper function to create a User object.
    """
    user = User.objects.get_or_create(username='testuser',
                                      first_name='Test',
                                      last_name='User',
                                      email='test@test.com')[0]
    user.set_password('testabc123')
    user.save()

    return user


class PageDetailsTests(TestCase):
    """
    Tests to check whether the news detail page contains the expected elements
    """
    def test_elements_in_page_details(self):
        """
        Check the presence of a hyperlink, like button, mark button and comment button in news detail page.
        """
        populate()
        user_object = create_user_object()
        self.client.login(username='testuser', password='testabc123')

        response = self.client.get(reverse('rango:show_page',kwargs={'category_name_slug':'tech', 'page_title_slug':'facebook-and-academics-row-over-data-access'}))

        content = response.content.decode()
        self.assertTrue('https://www.bbc.co.uk/news/technology-58086628' in content, f"{FAILURE_HEADER}There is no hyperlinks to original page.{FAILURE_FOOTER}")
        self.assertTrue('id="like_page_btn"' in content, f"{FAILURE_HEADER}There is no like button.{FAILURE_FOOTER}")
        self.assertTrue('id="mark_page_btn"' in content, f"{FAILURE_HEADER}There is no mark button.{FAILURE_FOOTER}")
        self.assertTrue('<button class="submit" type="submit">Send Now</button>' in content, f"{FAILURE_HEADER}There is no element used for comments.{FAILURE_FOOTER}")
    
class CommentFunction(TestCase):
    """
    Tests that the comment-related functions are working correctly
    """
    def test_comments(self):
        """
        Check that the added comment entries are displayed correctly
        """
        populate()
        test_user = create_user_object()
        self.client.login(username='testuser', password='testabc123')

        test_page = Page.objects.get(slug='facebook-and-academics-row-over-data-access', url='https://www.bbc.co.uk/news/technology-58086628')

        test_data = {'content':'I love this page.'}
        test_comment_form = CommentForm(data=test_data)

        self.assertTrue(test_comment_form.is_valid(), f"{FAILURE_HEADER}The CommentForm was not valid after entering the required data.{FAILURE_FOOTER}")

        test_comment = test_comment_form.save(commit=False)
        test_comment.page = test_page
        test_comment.user = test_user
        test_comment.save()

        response = self.client.get(reverse('rango:show_page',kwargs={'category_name_slug':'tech', 'page_title_slug':'facebook-and-academics-row-over-data-access'}))
        content = response.content.decode()
        self.assertTrue('<ul id = "list">' in content, f"{FAILURE_HEADER}The comment do not successfully display.{FAILURE_FOOTER}")
        self.assertTrue('testuser' in content, f"{FAILURE_HEADER}The comment do not successfully display.{FAILURE_FOOTER}")
        self.assertTrue('I love this page.' in content, f"{FAILURE_HEADER}The comment do not successfully display.{FAILURE_FOOTER}")
        
    def test_comment_form(self):
        """
        Tests whether CommentForm is in the correct place, and whether the correct fields have been specified for it.
        """
        self.assertTrue('CommentForm' in dir(forms), f"{FAILURE_HEADER}We couldn't find the CommentForm class in Rango's forms.py module.{FAILURE_FOOTER}")
        
        comment_form = forms.CommentForm()
        self.assertEqual(type(comment_form.__dict__['instance']), Comment, f"{FAILURE_HEADER}Your CommentForm does not match up to the Comment model. {FAILURE_FOOTER}")

        fields = comment_form.fields
        
        expected_fields = {
            'content': django_fields.CharField,
        }
        
        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]

            self.assertTrue(expected_field_name in fields.keys(), f"{FAILURE_HEADER}The field {expected_field_name} was not found in the CommentForm form.{FAILURE_FOOTER}")
            self.assertEqual(expected_field, type(fields[expected_field_name]), f"{FAILURE_HEADER}The field {expected_field_name} in CommentForm was not of the correct type. Expected {expected_field}; got {type(fields[expected_field_name])}.{FAILURE_FOOTER}")    

class LikeFunction(TestCase):
    """
    Tests that the like-related functions are working correctly
    """
    def test_likes(self):
        """
        Check whether the like icon changes and remains after the user has liked it.
        """
        populate()
        test_user = create_user_object()
        self.client.login(username='testuser', password='testabc123')

        test_page = Page.objects.get(slug='facebook-and-academics-row-over-data-access', url='https://www.bbc.co.uk/news/technology-58086628')

        test_data = {'user':test_user, 'page':test_page}
        test_like = Like()
        test_like.user = test_user
        test_like.page = test_page
        test_like.save()

        response = self.client.get(reverse('rango:show_page',kwargs={'category_name_slug':'tech', 'page_title_slug':'facebook-and-academics-row-over-data-access'}))

        content = response.content.decode()
        self.assertTrue('class="iconfont icon-dianzan1"' in content, f"{FAILURE_HEADER}The like icon does not change after a like.{FAILURE_FOOTER}")

class MarkFunction(TestCase):
    """
    Tests that the mark-related functions are working correctly
    """
    def test_marks(self):
        """
        Check whether the mark icon changes and remains after the user has marked it.
        """
        populate()
        test_user = create_user_object()
        self.client.login(username='testuser', password='testabc123')

        test_page = Page.objects.get(slug='facebook-and-academics-row-over-data-access', url='https://www.bbc.co.uk/news/technology-58086628')

        test_data = {'user':test_user, 'page':test_page}
        test_mark = Mark()
        test_mark.user = test_user
        test_mark.page = test_page
        test_mark.save()

        response = self.client.get(reverse('rango:show_page',kwargs={'category_name_slug':'tech', 'page_title_slug':'facebook-and-academics-row-over-data-access'}))

        content = response.content.decode()
        self.assertTrue('class="iconfont icon-shoucang6"' in content, f"{FAILURE_HEADER}The mark icon changes and remains when the user clicks on the marks.{FAILURE_FOOTER}")