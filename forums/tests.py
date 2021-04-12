import json

from rest_framework.test import APITestCase, APIClient

from authentication.models import User

from .models import Forum, Topic, Comment

class ForumNotLoginedTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user('test', 'test@test.com', 'testtest')

        for i in range(3):
            forum = Forum.objects.create(title='test'+str(i+1))
            for j in range(7):
                Topic.objects.create(title='test'+str(i+1)+'-'+str(j+1), forum=forum, creator=user)

    def test_get_forum_list(self):
        response = self.client.get('/api/forums/')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 3)
        self.assertEqual(response_jsonified['results'][0]['title'], 'test1')
        self.assertEqual(response_jsonified['results'][0]['topics'][0], 'test1-3')
        self.assertEqual(response_jsonified['results'][0]['topics'][4], 'test1-7')

    def test_get_forum(self):
        response = self.client.get('/api/forums/test1/')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['title'], 'test1')

    def test_create_forum(self):
        response = self.client.post('/api/forums/', {'title': 'test-test'})

        self.assertEqual(response.status_code, 401)

    def test_delete_forum(self):
        response = self.client.delete('/api/forums/test1/')

        self.assertEqual(response.status_code, 401)

class ForumLoginedTestCase(APITestCase):

    def setUp(self):
        user = User.objects.create_user('test', 'test@test.com', 'testtest')

        login = self.client.post('/api/token', {'email': 'test@test.com', 'password': 'testtest'})
        token = 'Bearer ' + json.loads(login.content)['access']
        self.client = APIClient(HTTP_AUTHORIZATION=token)

        for i in range(3):
            forum = Forum.objects.create(title='test'+str(i+1))
            for j in range(7):
                Topic.objects.create(title='test'+str(i+1)+'-'+str(j+1), forum=forum, creator=user)

    def test_get_forum_list(self):
        response = self.client.get('/api/forums/')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 3)
        self.assertEqual(response_jsonified['results'][0]['title'], 'test1')
        self.assertEqual(response_jsonified['results'][0]['topics'][0], 'test1-3')
        self.assertEqual(response_jsonified['results'][0]['topics'][4], 'test1-7')

    def test_get_forum(self):
        response = self.client.get('/api/forums/test1/')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['title'], 'test1')

    def test_create_forum(self):
        response = self.client.post('/api/forums/', {'title': 'test-test'})

        self.assertEqual(response.status_code, 403)

    def test_delete_forum(self):
        response = self.client.delete('/api/forums/test1/')

        self.assertEqual(response.status_code, 403)

class ForumLoginedSuperuserTestCase(APITestCase):

    def setUp(self):
        user = User.objects.create_superuser('test', 'test@test.com', 'testtest')

        login = self.client.post('/api/token', {'email': 'test@test.com', 'password': 'testtest'})
        token = 'Bearer ' + json.loads(login.content)['access']
        self.client = APIClient(HTTP_AUTHORIZATION=token)

        for i in range(3):
            forum = Forum.objects.create(title='test'+str(i+1))
            for j in range(7):
                Topic.objects.create(title='test'+str(i+1)+'-'+str(j+1), forum=forum, creator=user)

    def test_get_forum_list(self):
        response = self.client.get('/api/forums/')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 3)
        self.assertEqual(response_jsonified['results'][0]['title'], 'test1')
        self.assertEqual(response_jsonified['results'][0]['topics'][0], 'test1-3')
        self.assertEqual(response_jsonified['results'][0]['topics'][4], 'test1-7')

    def test_get_forum(self):
        response = self.client.get('/api/forums/test1/')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['title'], 'test1')

    def test_create_forum(self):
        response = self.client.post('/api/forums/', {'title': 'test-test'})

        self.assertEqual(response.status_code, 201)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['title'], 'test-test')
        self.assertEqual(response_jsonified['slug'], 'test-test')

    def test_delete_forum(self):
        Forum.objects.create(title='test-test')

        response = self.client.delete('/api/forums/test-test/')

        self.assertEqual(response.status_code, 204)

class TopicsNotLoginedTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user('test', 'test@test.com', 'testtest')

        for i in range(3):
            forum = Forum.objects.create(title='test'+str(i+1))
            for j in range(7):
                Topic.objects.create(title='test'+str(i+1)+'-'+str(j+1), forum=forum, creator=user)

    def test_get_topic_list(self):
        response = self.client.get('/api/topics/')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 21)
        self.assertEqual(response_jsonified['results'][0]['title'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['slug'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['creator'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][0]['forum'], 'test1')
        self.assertEqual(response_jsonified['results'][20]['title'], 'test3-7')

    def test_get_topic_list_search(self):
        response = self.client.get('/api/topics/?search=test1')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 7)
        self.assertEqual(response_jsonified['results'][0]['title'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['slug'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['creator'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][0]['forum'], 'test1')
        self.assertEqual(response_jsonified['results'][6]['title'], 'test1-7')

    def test_get_topic_list_filter(self):
        response = self.client.get('/api/topics/?title=test1-1')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 1)

        response = self.client.get('/api/topics/?forum=test1')
        self.assertEqual(response_jsonified['results'][0]['title'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['slug'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['creator'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][0]['forum'], 'test1')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 7)
        self.assertEqual(response_jsonified['results'][0]['title'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['slug'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['creator'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][0]['forum'], 'test1')
        self.assertEqual(response_jsonified['results'][6]['title'], 'test1-7')

        response = self.client.get('/api/topics/?creator=test')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 21)
        self.assertEqual(response_jsonified['results'][0]['title'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['slug'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['creator'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][0]['forum'], 'test1')
        self.assertEqual(response_jsonified['results'][20]['title'], 'test3-7')

    def test_get_topic(self):
        response = self.client.get('/api/topics/test1-1/')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['title'], 'test1-1')
        self.assertEqual(response_jsonified['slug'], 'test1-1')
        self.assertEqual(response_jsonified['creator'], 'test@test.com')
        self.assertEqual(response_jsonified['forum'], 'test1')

    def test_create_topic(self):
        response = self.client.post('/api/topics/', {'title': 'test1-test', 'forum':'test1'})

        self.assertEqual(response.status_code, 401)

    def test_update_topic(self):
        Topic.objects.create(title='test1-test', forum=Forum.objects.filter(title='test1')[0], creator=User.objects.filter(username='test')[0])

        response = self.client.put('/api/topics/test1-test/', {'title': 'test1-test-changed'})

        self.assertEqual(response.status_code, 401)

    def test_delete_topic(self):
        Topic.objects.create(title='test1-test', forum=Forum.objects.filter(title='test1')[0], creator=User.objects.filter(username='test')[0])

        response = self.client.delete('/api/topics/test1-test/')

        self.assertEqual(response.status_code, 401)

class TopicsLoginedTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user('test', 'test@test.com', 'testtest')

        login = self.client.post('/api/token', {'email': 'test@test.com', 'password': 'testtest'})
        token = 'Bearer ' + json.loads(login.content)['access']
        self.client = APIClient(HTTP_AUTHORIZATION=token)

        for i in range(3):
            forum = Forum.objects.create(title='test'+str(i+1))
            for j in range(7):
                Topic.objects.create(title='test'+str(i+1)+'-'+str(j+1), forum=forum, creator=user)

    def test_get_topic_list(self):
        response = self.client.get('/api/topics/')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 21)
        self.assertEqual(response_jsonified['results'][0]['title'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['slug'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['creator'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][0]['forum'], 'test1')
        self.assertEqual(response_jsonified['results'][20]['title'], 'test3-7')

    def test_get_topic_list_search(self):
        response = self.client.get('/api/topics/?search=test1')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 7)
        self.assertEqual(response_jsonified['results'][0]['title'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['slug'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['creator'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][0]['forum'], 'test1')
        self.assertEqual(response_jsonified['results'][6]['title'], 'test1-7')

    def test_get_topic_list_filter(self):
        response = self.client.get('/api/topics/?title=test1-1')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 1)

        response = self.client.get('/api/topics/?forum=test1')
        self.assertEqual(response_jsonified['results'][0]['title'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['slug'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['creator'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][0]['forum'], 'test1')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 7)
        self.assertEqual(response_jsonified['results'][0]['title'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['slug'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['creator'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][0]['forum'], 'test1')
        self.assertEqual(response_jsonified['results'][6]['title'], 'test1-7')

        response = self.client.get('/api/topics/?creator=test')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 21)
        self.assertEqual(response_jsonified['results'][0]['title'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['slug'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['creator'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][0]['forum'], 'test1')
        self.assertEqual(response_jsonified['results'][20]['title'], 'test3-7')

    def test_get_topic(self):
        response = self.client.get('/api/topics/test1-1/')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['title'], 'test1-1')
        self.assertEqual(response_jsonified['slug'], 'test1-1')
        self.assertEqual(response_jsonified['creator'], 'test@test.com')
        self.assertEqual(response_jsonified['forum'], 'test1')

    def test_create_topic(self):
        response = self.client.post('/api/topics/', {'title': 'test1-test', 'forum':'test1'})

        self.assertEqual(response.status_code, 201)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['title'], 'test1-test')
        self.assertEqual(response_jsonified['slug'], 'test1-test')
        self.assertEqual(response_jsonified['creator'], 'test@test.com')
        self.assertEqual(response_jsonified['forum'], 'test1')

    def test_update_topic(self):
        Topic.objects.create(title='test1-test', forum=Forum.objects.filter(title='test1')[0], creator=User.objects.filter(username='test')[0])

        response = self.client.put('/api/topics/test1-test/', {'title': 'test1-test-changed'})

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['title'], 'test1-test-changed')
        self.assertEqual(response_jsonified['slug'], 'test1-test-changed')
        self.assertEqual(response_jsonified['creator'], 'test@test.com')
        self.assertEqual(response_jsonified['forum'], 'test1')

    def test_update_other_user_topic(self):
        other_user = User.objects.create_user(username='test2', email='test2@test.com', password='testtest')
        Topic.objects.create(title='test1-test', forum=Forum.objects.filter(title='test1')[0], creator=other_user)

        response = self.client.put('/api/topics/test1-test/', {'title': 'test1-test-changed'})
        self.assertEqual(response.status_code, 403)

    def test_update_change_forum_topic(self):
        Topic.objects.create(title='test1-test', forum=Forum.objects.filter(title='test1')[0], creator=User.objects.filter(username='test')[0])

        response = self.client.put('/api/topics/test1-test/', {'title': 'test1-test-changed', 'forum': 'test2'})

        self.assertEqual(response.status_code, 403)

    def test_delete_topic(self):
        Topic.objects.create(title='test1-test', forum=Forum.objects.filter(title='test1')[0], creator=User.objects.filter(username='test')[0])

        response = self.client.delete('/api/topics/test1-test/')

        self.assertEqual(response.status_code, 204)

    def test_delete_other_user_topic(self):
        other_user = User.objects.create_user(username='test2', email='test2@test.com', password='testtest')
        Topic.objects.create(title='test1-test', forum=Forum.objects.filter(title='test1')[0], creator=other_user)

        response = self.client.delete('/api/topics/test1-test/')
        self.assertEqual(response.status_code, 403)

class TopicsLoginedSuperuserTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_superuser('test', 'test@test.com', 'testtest')

        login = self.client.post('/api/token', {'email': 'test@test.com', 'password': 'testtest'})
        token = 'Bearer ' + json.loads(login.content)['access']
        self.client = APIClient(HTTP_AUTHORIZATION=token)

        for i in range(3):
            forum = Forum.objects.create(title='test'+str(i+1))
            for j in range(7):
                Topic.objects.create(title='test'+str(i+1)+'-'+str(j+1), forum=forum, creator=user)

    def test_get_topic_list(self):
        response = self.client.get('/api/topics/')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 21)
        self.assertEqual(response_jsonified['results'][0]['title'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['slug'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['creator'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][0]['forum'], 'test1')
        self.assertEqual(response_jsonified['results'][20]['title'], 'test3-7')

    def test_get_topic_list_search(self):
        response = self.client.get('/api/topics/?search=test1')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 7)
        self.assertEqual(response_jsonified['results'][0]['title'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['slug'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['creator'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][0]['forum'], 'test1')
        self.assertEqual(response_jsonified['results'][6]['title'], 'test1-7')

    def test_get_topic_list_filter(self):
        response = self.client.get('/api/topics/?title=test1-1')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 1)

        response = self.client.get('/api/topics/?forum=test1')
        self.assertEqual(response_jsonified['results'][0]['title'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['slug'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['creator'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][0]['forum'], 'test1')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 7)
        self.assertEqual(response_jsonified['results'][0]['title'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['slug'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['creator'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][0]['forum'], 'test1')
        self.assertEqual(response_jsonified['results'][6]['title'], 'test1-7')

        response = self.client.get('/api/topics/?creator=test')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 21)
        self.assertEqual(response_jsonified['results'][0]['title'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['slug'], 'test1-1')
        self.assertEqual(response_jsonified['results'][0]['creator'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][0]['forum'], 'test1')
        self.assertEqual(response_jsonified['results'][20]['title'], 'test3-7')

    def test_get_topic(self):
        response = self.client.get('/api/topics/test1-1/')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['title'], 'test1-1')
        self.assertEqual(response_jsonified['slug'], 'test1-1')
        self.assertEqual(response_jsonified['creator'], 'test@test.com')
        self.assertEqual(response_jsonified['forum'], 'test1')

    def test_create_topic(self):
        response = self.client.post('/api/topics/', {'title': 'test1-test', 'forum':'test1'})

        self.assertEqual(response.status_code, 201)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['title'], 'test1-test')
        self.assertEqual(response_jsonified['slug'], 'test1-test')
        self.assertEqual(response_jsonified['creator'], 'test@test.com')
        self.assertEqual(response_jsonified['forum'], 'test1')

    def test_update_topic(self):
        Topic.objects.create(title='test1-test', forum=Forum.objects.filter(title='test1')[0], creator=User.objects.filter(username='test')[0])

        response = self.client.put('/api/topics/test1-test/', {'title': 'test1-test-changed'})

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['title'], 'test1-test-changed')
        self.assertEqual(response_jsonified['slug'], 'test1-test-changed')
        self.assertEqual(response_jsonified['creator'], 'test@test.com')
        self.assertEqual(response_jsonified['forum'], 'test1')

    def test_update_other_user_topic(self):
        other_user = User.objects.create_user(username='test2', email='test2@test.com', password='testtest')
        Topic.objects.create(title='test1-test', forum=Forum.objects.filter(title='test1')[0], creator=other_user)

        response = self.client.put('/api/topics/test1-test/', {'title': 'test1-test-changed'})
        self.assertEqual(response.status_code, 200)

    def test_update_change_forum_topic(self):
        Topic.objects.create(title='test1-test', forum=Forum.objects.filter(title='test1')[0], creator=User.objects.filter(username='test')[0])

        response = self.client.put('/api/topics/test1-test/', {'title': 'test1-test-changed', 'forum': 'test2'})

        self.assertEqual(response.status_code, 403)

    def test_delete_topic(self):
        Topic.objects.create(title='test1-test', forum=Forum.objects.filter(title='test1')[0], creator=User.objects.filter(username='test')[0])

        response = self.client.delete('/api/topics/test1-test/')

        self.assertEqual(response.status_code, 204)

    def test_delete_other_user_topic(self):
        other_user = User.objects.create_user(username='test2', email='test2@test.com', password='testtest')
        Topic.objects.create(title='test1-test', forum=Forum.objects.filter(title='test1')[0], creator=other_user)

        response = self.client.delete('/api/topics/test1-test/')
        self.assertEqual(response.status_code, 204)

class CommentsNotLoginedTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='test', email='test@test.com', password='testtest')

        forum = Forum.objects.create(title='test')
        for i in range(3):
            topic = Topic.objects.create(title='test-test' + str(i+1), forum=forum, creator=user)
            for j in range(10):
                Comment.objects.create(text='test-test' + str(i+1) + '-test' + str(j+1), topic=topic, author=user)

    def test_get_comments_list(self):
        response = self.client.get('/api/comments/')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 30)
        self.assertEqual(response_jsonified['results'][0]['author'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][0]['text'], 'test-test1-test1')
        self.assertEqual(response_jsonified['results'][0]['topic'], 'test-test1')
        self.assertEqual(response_jsonified['results'][29]['author'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][29]['text'], 'test-test3-test10')
        self.assertEqual(response_jsonified['results'][29]['topic'], 'test-test3')
    
    def test_get_comments_list_search(self):
        response = self.client.get('/api/comments/?search=1')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 14)

    def test_get_comments_list_filter(self):
        response = self.client.get('/api/comments/?author=test')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 30)
        self.assertEqual(response_jsonified['results'][0]['author'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][0]['text'], 'test-test1-test1')
        self.assertEqual(response_jsonified['results'][0]['topic'], 'test-test1')
        self.assertEqual(response_jsonified['results'][29]['author'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][29]['text'], 'test-test3-test10')
        self.assertEqual(response_jsonified['results'][29]['topic'], 'test-test3')
        
        response = self.client.get('/api/comments/?topic=test-test1')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 10)
        self.assertEqual(response_jsonified['results'][0]['author'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][0]['text'], 'test-test1-test1')
        self.assertEqual(response_jsonified['results'][0]['topic'], 'test-test1')
        self.assertEqual(response_jsonified['results'][9]['author'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][9]['text'], 'test-test1-test10')
        self.assertEqual(response_jsonified['results'][9]['topic'], 'test-test1')

    def test_get_comments_list_filter_search(self):
        response = self.client.get('/api/comments/?topic=test-test1&search=10')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 1)

    def test_get_comment(self):
        response = self.client.get('/api/comments/1/')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['author'], 'test@test.com')
        self.assertEqual(response_jsonified['text'], 'test-test1-test1')
        self.assertEqual(response_jsonified['topic'], 'test-test1')

    def test_create_comment(self):
        response = self.client.post('/api/comments/', {'topic': 'test-test1', 'text': 'test-test1-test-test'})

        self.assertEqual(response.status_code, 401)

    def test_update_comment(self):
        response = self.client.put('/api/comments/1/', {'text': 'test-test1-test-test'})

        self.assertEqual(response.status_code, 401)

    def test_delete_comment(self):
        response = self.client.delete('/api/comments/1/')

        self.assertEqual(response.status_code, 401)

class CommentsLoginedTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', email='test@test.com', password='testtest')

        login = self.client.post('/api/token', {'email': 'test@test.com', 'password': 'testtest'})
        token = 'Bearer ' + json.loads(login.content)['access']
        self.client = APIClient(HTTP_AUTHORIZATION=token)

        self.forum = Forum.objects.create(title='test')
        for i in range(3):
            topic = Topic.objects.create(title='test-test' + str(i+1), forum=self.forum, creator=self.user)
            for j in range(10):
                Comment.objects.create(text='test-test' + str(i+1) + '-test' + str(j+1), topic=topic, author=self.user)

    def test_get_comments_list(self):
        response = self.client.get('/api/comments/')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 30)
        self.assertEqual(response_jsonified['results'][0]['author'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][0]['text'], 'test-test1-test1')
        self.assertEqual(response_jsonified['results'][0]['topic'], 'test-test1')
        self.assertEqual(response_jsonified['results'][29]['author'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][29]['text'], 'test-test3-test10')
        self.assertEqual(response_jsonified['results'][29]['topic'], 'test-test3')
    
    def test_get_comments_list_search(self):
        response = self.client.get('/api/comments/?search=1')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 14)

    def test_get_comments_list_filter(self):
        response = self.client.get('/api/comments/?author=test')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 30)
        self.assertEqual(response_jsonified['results'][0]['author'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][0]['text'], 'test-test1-test1')
        self.assertEqual(response_jsonified['results'][0]['topic'], 'test-test1')
        self.assertEqual(response_jsonified['results'][29]['author'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][29]['text'], 'test-test3-test10')
        self.assertEqual(response_jsonified['results'][29]['topic'], 'test-test3')

        response = self.client.get('/api/comments/?topic=test-test1')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 10)
        self.assertEqual(response_jsonified['results'][0]['author'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][0]['text'], 'test-test1-test1')
        self.assertEqual(response_jsonified['results'][0]['topic'], 'test-test1')
        self.assertEqual(response_jsonified['results'][9]['author'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][9]['text'], 'test-test1-test10')
        self.assertEqual(response_jsonified['results'][9]['topic'], 'test-test1')

    def test_get_comments_list_filter_search(self):
        response = self.client.get('/api/comments/?topic=test-test1&search=10')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 1)

    def test_get_comment(self):
        response = self.client.get('/api/comments/1/')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['author'], 'test@test.com')
        self.assertEqual(response_jsonified['text'], 'test-test1-test1')
        self.assertEqual(response_jsonified['topic'], 'test-test1')

    def test_create_comment(self):
        response = self.client.post('/api/comments/', {'topic': 'test-test1', 'text': 'test-test1-test-test'})

        self.assertEqual(response.status_code, 201)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['author'], 'test@test.com')
        self.assertEqual(response_jsonified['text'], 'test-test1-test-test')
        self.assertEqual(response_jsonified['topic'], 'test-test1')

    def test_update_comment(self):
        topic = Topic.objects.filter(title='test-test1')[0]
        comment = Comment.objects.create(text='test-test1-test-test', topic=topic, author=self.user)

        response = self.client.put('/api/comments/' + str(comment.id) + '/', {'text': 'test-test1-test-test-changed'})

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['author'], 'test@test.com')
        self.assertEqual(response_jsonified['text'], 'test-test1-test-test-changed')
        self.assertEqual(response_jsonified['topic'], 'test-test1')

    def test_update_other_user_comment(self):
        other_user = User.objects.create_user(username='test2', email='test2@test.com', password='testtest')
        topic = Topic.objects.filter(title='test-test1')[0]
        comment = Comment.objects.create(text='test-test1-test-test', topic=topic, author=other_user)

        response = self.client.put('/api/comments/' + str(comment.id) + '/', {'text': 'test-test1-test-test-changed'})

        self.assertEqual(response.status_code, 403)

    def test_update_change_topic_comment(self):
        topic = Topic.objects.filter(title='test-test1')[0]
        comment = Comment.objects.create(text='test-test1-test-test', topic=topic, author=self.user)

        response = self.client.put('/api/comments/' + str(comment.id) + '/', {'test-test2-test-test-changed': 'test1-test-changed', 'topic': 'test2'})

        self.assertEqual(response.status_code, 403)

    def test_delete_comment(self):
        topic = Topic.objects.filter(title='test-test1')[0]
        comment = Comment.objects.create(text='test-test1-test-test', topic=topic, author=self.user)

        response = self.client.delete('/api/comments/' + str(comment.id) + '/')

        self.assertEqual(response.status_code, 204)

    def test_delete_other_user_comment(self):
        other_user = User.objects.create_user(username='test2', email='test2@test.com', password='testtest')
        topic = Topic.objects.filter(title='test-test1')[0]
        comment = Comment.objects.create(text='test-test1-test-test', topic=topic, author=other_user)

        response = self.client.delete('/api/comments/' + str(comment.id) + '/')

        self.assertEqual(response.status_code, 403)

class CommentsLoginedSuperuserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='test', email='test@test.com', password='testtest')

        login = self.client.post('/api/token', {'email': 'test@test.com', 'password': 'testtest'})
        token = 'Bearer ' + json.loads(login.content)['access']
        self.client = APIClient(HTTP_AUTHORIZATION=token)

        self.forum = Forum.objects.create(title='test')
        for i in range(3):
            topic = Topic.objects.create(title='test-test' + str(i+1), forum=self.forum, creator=self.user)
            for j in range(10):
                Comment.objects.create(text='test-test' + str(i+1) + '-test' + str(j+1), topic=topic, author=self.user)

    def test_get_comments_list(self):
        response = self.client.get('/api/comments/')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 30)
        self.assertEqual(response_jsonified['results'][0]['author'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][0]['text'], 'test-test1-test1')
        self.assertEqual(response_jsonified['results'][0]['topic'], 'test-test1')
        self.assertEqual(response_jsonified['results'][29]['author'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][29]['text'], 'test-test3-test10')
        self.assertEqual(response_jsonified['results'][29]['topic'], 'test-test3')

    def test_get_comments_list_search(self):
        response = self.client.get('/api/comments/?search=1')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 14)

    def test_get_comments_list_filter(self):
        response = self.client.get('/api/comments/?author=test')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 30)
        self.assertEqual(response_jsonified['results'][0]['author'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][0]['text'], 'test-test1-test1')
        self.assertEqual(response_jsonified['results'][0]['topic'], 'test-test1')
        self.assertEqual(response_jsonified['results'][29]['author'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][29]['text'], 'test-test3-test10')
        self.assertEqual(response_jsonified['results'][29]['topic'], 'test-test3')

        response = self.client.get('/api/comments/?topic=test-test1')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 10)
        self.assertEqual(response_jsonified['results'][0]['author'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][0]['text'], 'test-test1-test1')
        self.assertEqual(response_jsonified['results'][0]['topic'], 'test-test1')
        self.assertEqual(response_jsonified['results'][9]['author'], 'test@test.com')
        self.assertEqual(response_jsonified['results'][9]['text'], 'test-test1-test10')
        self.assertEqual(response_jsonified['results'][9]['topic'], 'test-test1')

    def test_get_comments_list_filter_search(self):
        response = self.client.get('/api/comments/?topic=test-test1&search=10')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['count'], 1)

    def test_get_comment(self):
        response = self.client.get('/api/comments/1/')

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['author'], 'test@test.com')
        self.assertEqual(response_jsonified['text'], 'test-test1-test1')
        self.assertEqual(response_jsonified['topic'], 'test-test1')

    def test_create_comment(self):
        response = self.client.post('/api/comments/', {'topic': 'test-test1', 'text': 'test-test1-test-test'})

        self.assertEqual(response.status_code, 201)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['author'], 'test@test.com')
        self.assertEqual(response_jsonified['text'], 'test-test1-test-test')
        self.assertEqual(response_jsonified['topic'], 'test-test1')

    def test_update_comment(self):
        topic = Topic.objects.filter(title='test-test1')[0]
        comment = Comment.objects.create(text='test-test1-test-test', topic=topic, author=self.user)

        response = self.client.put('/api/comments/' + str(comment.id) + '/', {'text': 'test-test1-test-test-changed'})

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['author'], 'test@test.com')
        self.assertEqual(response_jsonified['text'], 'test-test1-test-test-changed')
        self.assertEqual(response_jsonified['topic'], 'test-test1')

    def test_update_other_user_comment(self):
        other_user = User.objects.create_user(username='test2', email='test2@test.com', password='testtest')
        topic = Topic.objects.filter(title='test-test1')[0]
        comment = Comment.objects.create(text='test-test1-test-test', topic=topic, author=other_user)

        response = self.client.put('/api/comments/' + str(comment.id) + '/', {'text': 'test-test1-test-test-changed'})

        self.assertEqual(response.status_code, 200)
        response_jsonified = json.loads(response.content)
        self.assertEqual(response_jsonified['author'], 'test2@test.com')
        self.assertEqual(response_jsonified['text'], 'test-test1-test-test-changed')
        self.assertEqual(response_jsonified['topic'], 'test-test1')

    def test_update_change_topic_comment(self):
        topic = Topic.objects.filter(title='test-test1')[0]
        comment = Comment.objects.create(text='test-test1-test-test', topic=topic, author=self.user)

        response = self.client.put('/api/comments/' + str(comment.id) + '/', {'test-test2-test-test-changed': 'test1-test-changed', 'topic': 'test2'})

        self.assertEqual(response.status_code, 403)

    def test_delete_comment(self):
        topic = Topic.objects.filter(title='test-test1')[0]
        comment = Comment.objects.create(text='test-test1-test-test', topic=topic, author=self.user)

        response = self.client.delete('/api/comments/' + str(comment.id) + '/')

        self.assertEqual(response.status_code, 204)

    def test_delete_other_user_comment(self):
        other_user = User.objects.create_user(username='test2', email='test2@test.com', password='testtest')
        topic = Topic.objects.filter(title='test-test1')[0]
        comment = Comment.objects.create(text='test-test1-test-test', topic=topic, author=other_user)

        response = self.client.delete('/api/comments/' + str(comment.id) + '/')

        self.assertEqual(response.status_code, 204)
