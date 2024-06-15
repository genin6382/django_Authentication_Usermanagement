from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from myapp.models import Post
class Command(BaseCommand):
    help = 'Setup mods and superusers and assign them to the appropriate groups'

    def handle(self, *args, **kwargs):
        # Create groups
        default, created = Group.objects.get_or_create(name='default')
        mods, created = Group.objects.get_or_create(name='mods')
        superusers, created = Group.objects.get_or_create(name='superusers')
        banned, created = Group.objects.get_or_create(name='banned')

        # Define content type for your custom model (e.g., 'Post' model)
        content_type = ContentType.objects.get_for_model(Post)  
        content_type2 = ContentType.objects.get_for_model(User)  # This is wrong pls define content type for the model and not user model
        # Define permissions
        permissions = [
            {'codename': 'add_post', 'name': 'Can add post', 'content_type': content_type},
            {'codename': 'change_post', 'name': 'Can change post', 'content_type': content_type},
            {'codename': 'view_post', 'name': 'Can view post', 'content_type': content_type},
            {'codename': 'delete_post', 'name': 'Can delete post', 'content_type': content_type},
            {'codename': 'can_ban_user', 'name': 'Can ban user', 'content_type': content_type2},  # Assuming 'auth' app
        ]

        # Create or fetch permissions
        for perm_data in permissions:
            Permission.objects.get_or_create(**perm_data)

        # Assign permissions to the groups
        default.permissions.set([
            Permission.objects.get(codename='add_post', content_type=content_type),
            Permission.objects.get(codename='change_post', content_type=content_type),
            Permission.objects.get(codename='view_post', content_type=content_type),
        ])

        mods.permissions.set([
            Permission.objects.get(codename='add_post', content_type=content_type),
            Permission.objects.get(codename='change_post', content_type=content_type),
            Permission.objects.get(codename='view_post', content_type=content_type),
            Permission.objects.get(codename='delete_post', content_type=content_type),
        ])

        superusers.permissions.set([
            Permission.objects.get(codename='add_post', content_type=content_type),
            Permission.objects.get(codename='change_post', content_type=content_type),
            Permission.objects.get(codename='view_post', content_type=content_type),
            Permission.objects.get(codename='delete_post', content_type=content_type),
            Permission.objects.get(codename='can_ban_user', content_type=content_type2),
        ])

        banned.permissions.set([])

        # Create a superuser
        superuser = User.objects.create_superuser(username="VIDHU", password="VIDHU$12")
        superuser.groups.add(superusers)

        # Create a mod
        mod = User.objects.create_user(username="mod", password="mod$12")
        mod.groups.add(mods)

        # Print groups and their permissions
        self.print_groups()

    def print_groups(self):
        all_groups = Group.objects.all()
        for group in all_groups:
            self.stdout.write(f"Group: {group.name}")
            group_permissions = group.permissions.all()
            for perm in group_permissions:
                self.stdout.write(f" - Permission: {perm.codename}, {perm.name}, {perm.content_type.app_label}")

# Define permissions 
        #This is wrong pls define content type for the model and not user model
        # content_type = ContentType.objects.get_for_model(User)
        
