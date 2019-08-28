import datetime
import random
import re

import faker
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from portailva.association.models import Category, Association
import logging

from portailva.directory.models import DirectoryEntry
from portailva.event.models import Event

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Generates sample data'

    def add_arguments(self, parser):
        parser.add_argument('--categories', help="Number of categories to create", default=0, type=int)
        parser.add_argument('--associations', help="Number of associations to create", default=0, type=int)
        parser.add_argument('--users', help="Number of users to create", default=0, type=int)
        parser.add_argument('--directory_entries', help="Number of directory entries to create", default=0, type=int)
        parser.add_argument('--events', help="Number of events entries to create", default=0, type=int)

    def handle(self, *args, **options):
        fake = faker.Faker('fr_FR')
        user_counter = 0
        while user_counter < options['users']:
            try:
                User.objects.create(
                    username=fake.user_name(),
                    email=fake.email(),
                    password=fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True),
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                )
            except IntegrityError:
                pass
            else:
                user_counter += 1
        users = User.objects.all()
        logger.info(f"Created {options['users']} users")

        for i in range(options['categories']):
            Category.objects.create(
                name=fake.sentence(nb_words=2, ext_word_list=None),
                position=random.randint(-options['categories'], options['categories']),
                latex_color_name=fake.word(ext_word_list=None)
            )
        categories = Category.objects.all()
        logger.info(f"Created {options['categories']} categories")

        not_caps = re.compile('[^A-Z]')
        for i in range(options['associations']):
            name = fake.company()
            asso = Association.objects.create(
                name=name,
                acronym=re.sub(not_caps, '', name),
                description=fake.text(max_nb_chars=200, ext_word_list=None),
                active_members_number=random.randint(0, 200),
                is_active=fake.boolean(chance_of_getting_true=85),
                is_validated=fake.boolean(chance_of_getting_true=90),
                has_place=fake.boolean(chance_of_getting_true=60),
                category=random.choice(categories),
                logo_url=fake.image_url(width=None, height=None),
                iban=fake.iban(),
                bic=fake.password(length=11, special_chars=False, digits=True, upper_case=True, lower_case=False),
            )
            number_of_users = random.randint(0, 4)
            asso.users.set(random.choices(users, k=number_of_users))
        logger.info(f"Created {options['associations']} associations")
        assos = Association.objects.all()

        for i in range(options['directory_entries']):
            asso = random.choice(assos)
            DirectoryEntry.objects.create(
                association=asso,
                description=asso.description[:800],
                contact_address=fake.email(),
                is_online=fake.boolean(chance_of_getting_true=80),
            )
        logger.info(f"Created {options['directory_entries']} directory entries")

        for i in range(options['events']):
            asso = random.choice(assos)
            start_date = fake.date_time_this_decade(before_now=True, after_now=True)
            duration = datetime.timedelta(hours=random.randint(1, 5))
            end_date = start_date + duration
            Event.objects.create(
                association=asso,
                short_description=fake.text(max_nb_chars=150, ext_word_list=None),
                description=fake.text(max_nb_chars=300, ext_word_list=None),
                is_online=fake.boolean(chance_of_getting_true=80),
                begins_at=start_date,
                ends_at=end_date,
            )
        logger.info(f"Created {options['events']} events")
