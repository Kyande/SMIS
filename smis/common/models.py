import uuid

from django.db import models


def user_name(user_id_field):

    @property
    def prop(self):
        from smis.users.models import User

        try:
            user = User.objects.get(
                id=getattr(self, user_id_field))
            return user.get_full_name()
        except User.DoesNotExist:
            return 'Unknown'

    return prop


class AbstractBase(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class OwnedAbstractBase(AbstractBase):
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.UUIDField()
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.UUIDField()

    # properties
    created_by_name = user_name('created_by')
    updated_by_name = user_name('updated_by')

    class Meta(AbstractBase.Meta):
        abstract = True
        ordering = ('-updated', '-created')

    def preserve_created_by(self):
        try:
            original = self.__class__.objects.get(pk=self.pk)
            self.created_by = original.created_by
        except self.__class__.DoesNotExist:
            pass

    def save(self, *args, **kwargs):
        self.preserve_created_by()
        self.full_clean(exclude=None)
        super().save(*args, **kwargs)
