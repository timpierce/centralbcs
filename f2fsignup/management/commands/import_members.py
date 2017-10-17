from csv import reader
from datetime import datetime

from django.core.management.base import BaseCommand
from f2fsignup.models import Member, Group


class Command(BaseCommand):
    help = 'Imports members from csv file.'

    def add_arguments(self, parser):
        parser.add_argument('import_file', type=str)

    def handle(self, *args, **options):
        import_count = 0
        with open(options['import_file'], 'rU') as acs_file:
            acs_reader = reader(acs_file)
            for row in acs_reader:
                member = Member()
                try:
                    member.group = Group.objects.get(name=row[0])
                    member.ministry = row[1]
                    member.first_name = row[2]
                    member.last_name = row[3]
                    member.gender = row[4][0]
                    member.dob = datetime.strptime(row[5], '%m/%d/%y')
                    member.phone = row[6]
                    member.email = row[7]
                    member.address = row[8]
                    member.city = row[9]
                    member.state = row[10]
                    member.postal_code = row[11]
                    member.comments = 'Imported from ACS'
                    member.save(send_email=False)
                    import_count += 1
                except Group.DoesNotExist:
                    self.stdout.write('Group %s does not exist. Skipping %s %s.' % (row[0], row[2], row[3]))
                except ValueError:
                    self.stdout.write("Problem dob for %s %s" % (row[2], row[3]))
                except Exception, e:
                    self.stdout.write("Problem with %s %s: %s" % (row[2], row[3], e.message))

        self.stdout.write(self.style.SUCCESS('Successfully imported %s members.' % import_count))
