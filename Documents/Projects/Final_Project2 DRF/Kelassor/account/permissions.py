from rest_framework.permissions import BasePermission




def GroupPermission(*group_names):
    class _DynamicGroupPermission(BasePermission):
        def has_permission(self, request, view):
            if not request.user or not request.user.is_authenticated:
                return False

            return request.user.groups.filter(name__in=group_names).exists()
    return _DynamicGroupPermission



def is_supportpanel_user(user):
    return user.groups.filter(name="SupportPanel").exists()





class GroupHasDynamicPermission(BasePermission):
    required_perms = []
    always_allowed = ["SuperUser", "SupportPanel"]

    def __init__(self):
        if not hasattr(self, 'required_perms'):
            self.required_perms = []

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        user_groups = user.groups.all()
        if user_groups.filter(name__in=self.always_allowed).exists():
            return True

        for group in user_groups:
            perms = group.permissions.values_list("content_type__app_label", "codename")
            full_perms = [f"{app}.{code}" for app, code in perms]
            if all(p in full_perms for p in self.required_perms):
                return True

        return False



def create_permission_class(required_perms_list):
    class CustomPermission(GroupHasDynamicPermission):
        def __init__(self):
            super().__init__()
            self.required_perms = required_perms_list

    return CustomPermission
