from csv import reader
from optparse import make_option

from django.core.management.base import BaseCommand
from f2fsignup.models import Group


class Command(BaseCommand):
    help = 'Imports groups from csv.'
    option_list = BaseCommand.option_list + (
        make_option('--file',
                    dest='import_file',
                    help='File name of import file'),
    )

    def handle(self, *args, **options):
        import_count = 0
        with open(options['import_file'], 'rU') as acs_file:
            acs_reader = reader(acs_file)
            for row in acs_reader:
                group = Group()
                group.hosts = row[1].strip()
                group.leaders = row[0].strip()
                group.leader_email = row[3].strip()
                group.leader_phone = row[2].strip()
                group.location = row[4].strip()
                group.address = '%s in %s' % (row[5].strip(), row[6])
                group.day_of_week = row[7].strip()
                group.name = row[8].strip()
                group.save()
                import_count += 1
        self.stdout.write('Successfully imported %s groups' % import_count)
