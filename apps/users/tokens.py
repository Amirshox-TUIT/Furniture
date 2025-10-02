from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        """
        is_active ni hash qilishdan oldin hisoblaydi
        """
        return f"{user.pk}{timestamp}{user.is_active}"


email_verification_token = EmailVerificationTokenGenerator()