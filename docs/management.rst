*******************
Management commands
*******************

.. highlight:: python

.. _thumbnail-cleanup:

thumbnail cleanup
=================
``python manage.py thumbnail cleanup``

This cleans up the Key Value Store from stale cache. It removes references to
images that do not exist and thumbnail references and their actual files for
images that do not exist. It removes thumbnails for unknown images.


.. _thumbnail-clear:

thumbnail clear
===============
``python manage.py thumbnail clear [--leave-orphans] [--delete-referenced] [--delete-all]``

This totally empties the Key Value Store from all keys that start with the
``settings.THUMBNAIL_KEY_PREFIX``.

With ``--leave-orphans`` or ``-o`` it does not delete any files. The Key Value
store will update when you hit the template tags, and if the thumbnails files
still exist they will be used and not overwritten. This can be useful if your
Key Value Store has garbage data not dealt with by cleanup or you're switching
Key Value Store backend.

With ``--delete-referenced`` or ``-r`` it will delete all thumbnail files
referenced by the Key Value Store. It is generally safe to run this if you do
not reference the generated thumbnails by name somewhere else in your code. As
long as all the original images still exist this will trigger a regeneration of
all the thumbnails the Key Value Store knows about thumbnails.

With ``--delete-all`` or ``-a`` this will also delete any orphans not in the
Key Value Store. Caution should be exercised with this command if multiple
Django sites (as in SITE_ID) or projects are using the same MEDIA_ROOT since
this will clear out absolutely everything in the thumbnail cache directory. It
is equivalent to rm -rf MEDIA_ROOT + THUMBNAIL_PREFIX
