from email.policy import default
import uuid
import base64
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
# from userena.models import UserenaLanguageBaseProfile
# from userena.utils import user_model_label 

# Create your models here.


class Profile(models.Model):
    """ Default profile """

    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='profile',on_delete=models.CASCADE)

    referral_code = models.CharField(max_length=300, blank=True, null=True)
    count1= models.IntegerField(default=0)


    def get_absolute_url(self):
        print(u'/profile/show/%d' % self.id)
        return u'/profile/show/%d' % self.id
    def generate_verification_code(self):
        # Generate user's verification code
        # TODO: Move this to the model
        return base64.urlsafe_b64encode(uuid.uuid1().bytes.encode("base64").rstrip())[:25]

    def save(self, *args, **kwargs):
        """
        If this is a new user, generate code.
        Otherwise leave as is
        """
        referrals= Profile.objects.all()
        print("jhjhbhjbj")

        return super(Profile, self).save(*args, **kwargs)


