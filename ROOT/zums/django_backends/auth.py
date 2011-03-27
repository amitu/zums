import msgpack
from django.contrib.auth.models import User
from zums.zumsd import query

class ZUMSBackend:
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def update_user_if_required(self, user, user_info):
        save = False
        def check_attr(name, default=""):
            if getattr(user, name) != user_info.get(name, default):
                setattr(user, name, user_info.get(name, default))
                save = True
        check_attr("email")
        check_attr("first_name")
        check_attr("last_name")
        check_attr("is_superuser", False)
        check_attr("is_staff", False)
        if not user.id: save = True
        if save: user.save()

    def authenticate(self, username=None, password=None):
        user_info = query(str("user_authenticate:%s:%s" % (username, password)))
        if user_info:
            user_info = msgpack.loads(user_info)
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=user_info["username"], password='get from zums')
            self.update_user_if_required(user, user_info)
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
