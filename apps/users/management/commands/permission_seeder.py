from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from common_utils.users.constants.permissions_constants import PERMISSIONS
from django.db import transaction



@transaction.atomic
class Command(BaseCommand):
    help = 'Create custom permissions from PERMISSIONS constant'

    def handle(self, *args, **options):
        """
        Create custom permissions defined in the PERMISSIONS constant.
        These are not tied to any specific model but are global permissions.
        """
        try:
            print("Starting permission creation process...")

            created_count = 0
            updated_count = 0

            for perm_key, perm_codename in PERMISSIONS.items():
                # Create a readable name from the key
                perm_name = f"Can {perm_key.replace('_', ' ').lower()}"

                perm_model = perm_codename.split('_')[-1]


                content_type = ContentType.objects.filter(model=perm_model).first()

                
                permission, created = Permission.objects.get_or_create(
                                                                    codename=perm_codename,
                                                                    content_type=content_type,
                                                                    defaults={
                                                                        "name": perm_name
                                                                    }
                                                                )
                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Created permission: {perm_codename} ({perm_name})"
                        )
                    )
                else:
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"Permission already exists: {perm_codename}"
                        )
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f"\n=== Summary ===\n"
                    f"Created: {created_count}\n"
                    f"Already existed: {updated_count}\n"
                    f"Total: {len(PERMISSIONS)}"
                )
            )
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error: {str(e)}"))