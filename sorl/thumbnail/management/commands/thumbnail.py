# -*- encoding: utf8 -*-

from __future__ import unicode_literals, print_function

import sys
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from sorl.thumbnail import default
from sorl.thumbnail.images import delete_all_thumbnails


class Command(BaseCommand):
    help = (
        'Handles thumbnails and key value store'
    )
    args = '[cleanup, clear [--leave-orphans] [--delete-referenced] [--delete-all]]'
    option_list = BaseCommand.option_list + (
        make_option('-l', '--leave-orphans',
                    action='store_true',
                    dest='leave_orphans',
                    default=True,
                    help='Only drop the Key Value Cache, without deleting any files'),
        make_option('-r', '--delete-referenced',
                    action='store_true',
                    dest='delete_referenced',
                    default=False,
                    help='Delete everything in the thumbnail cache, including orphans and files not put there by sorl-thumbnail'),
        make_option('-a', '--delete-all',
                    action='store_true',
                    dest='delete_all',
                    default=False,
                    help='Delete everything in the thumbnail cache, including orphans and files not put there by sorl-thumbnail'),
    )

    def handle(self, *labels, **options):
        verbosity = int(options.get('verbosity'))

        # Django 1.4 compatibility fix
        stdout = options.get('stdout', None)
        stdout = stdout if stdout else sys.stdout

        stderr = options.get('stderr', None)
        stderr = stderr if stderr else sys.stderr

        if not labels:
            print(self.print_help('thumbnail', ''), file=stderr)
            sys.exit(1)

        if len(labels) != 1:
            raise CommandError('`%s` is not a valid argument' % labels)

        label = labels[0]

        if label not in ['cleanup', 'clear']:
            raise CommandError('`%s` unknown action' % label)

        if label == 'cleanup':
            if verbosity >= 1:
                print("Cleanup thumbnails", end=' ... ', file=stdout)

            default.kvstore.cleanup()

            if verbosity >= 1:
                print("[Done]", file=stdout)

        elif label == 'clear':
            if verbosity >= 1:
                print("Clear the Key Value Store", end=' ... ', file=stdout)

            if options['delete_referenced']:
                default.kvstore.delete_all_thumbnail_files()

            default.kvstore.clear()

            if options['delete_all']:
                delete_all_thumbnails()

            if verbosity >= 1:
                print('[Done]', file=stdout)
