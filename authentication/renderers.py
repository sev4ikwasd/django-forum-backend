from core.renderers import CustomJSONRenderer

class UserJSONRenderer(CustomJSONRenderer):
    charset = 'utf-8'
    object_label = 'user'
    pagination_object_label = 'users'
    pagination_object_count = 'usersCount'

    def render(self, data, media_type=None, rederer_context=None):
        token = data.get('token', None)

        if token is not None and isinstance(token, bytes):
            data['token'] = token.decode('utf-8')

        return super(UserJSONRenderer, self).render(data)