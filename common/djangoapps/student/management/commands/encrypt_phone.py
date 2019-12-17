from __future__ import print_function
import re

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from six import text_type
from django.db import connection
from student.hasher import AESCipher


class Command(BaseCommand):

    help = """
    This command will encrypt user's phone.
    """

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, phone FROM auth_userprofile")
            row = cursor.fetchall()
            update_values = [(int(profile[0]), AESCipher.encrypt(profile[-1])) for profile in row]
            sql = """INSERT INTO auth_userprofile (id, phone) VALUES {} ON DUPLICATE KEY UPDATE id=VALUES(id), phone=VALUES(phone);""".format(str(update_values)[1:-1])
            cursor.execute(sql)
            print('Complete!')
