.. _upstream-differences:

Changes With Respect To Upstream
================================

Evernote's needs differ from the Pootle-as-a-product perspective, and we
have seen the need to `fork the upstream product
<https://github.com/evernote/pootle/commit/8140ff1706>`_ to adapt it to
our specific needs. This involves adding new features and customizing the
existing product. We have also ripped out unneeded stuff and cleaned up
code to make it easier for us to work with no distractions.


Feature Differences
-------------------

Added Features
^^^^^^^^^^^^^^

- Commands and store action logging.

- General *system* user which is the author of the batch actions performed
  via management commands.

- Timeline tracks all changes done to units.

- Whole new set of quality checks (plus the related ``test_checks``
  management command).

- Project-specific announcements in a sidebar.

- Maintenance mode middleware. It can be enabled in the settings before
  performing any app upgrades.

- Screenshot prefix URL to allow integrating screenshots for units.

- Evernote-specific apps: reports and stats.


Changed Features
^^^^^^^^^^^^^^^^

- Richer and more responsive statistics. *Last Updated* dates for stores
  and projects are tracked, for instance. These statistics are also
  available for the *All Projects* view.

- ``refresh_stats`` has been refined to be faster, and allows extra
  options.

- Quality checks. A custom set of quality checks has been incorporated.

- Report target field has been removed. This functionality has been
  integrated into a new contact form.

- Table sorting is remembered across overview pages.

- Captcha implementation details have been refined.

- Authentication is handled via Evernote (*evernote_auth* app).

- Word count function can be customized in the settings, and a new method
  has been incorporated (omits placeholders and words that shouldn't be
  translated). Non-empty units with 0 words are immediately translated and
  marked as fuzzy.


Removed Features
^^^^^^^^^^^^^^^^

- SQLite support.

- LDAP support.

- Monolingual file format support.

- Support for Version Control Systems.

- News, notifications and RSS feeds.

- Live Translation.

- Lookup backends.

- Offline translation, file uploads.

- Update against templates. (Basically templates aren't needed)

- User registration. *django-registration* has been removed and new users
  need to use their Evernote accounts.

- Public API.

- Project/Language/Translation Project descriptions.


Unmerged Features
^^^^^^^^^^^^^^^^^

These features appeared upstream since we forked, but haven't been
incorporated.

- Extension actions.

- Tags and Goals.

- Local Translation Memory.

- ``assign_permissions`` management command (688b8482)


Editor Differences
------------------

- If the currently-submitted unit has pending checks, the editor won't
  advance to the next unit and it will be updated displaying the
  unresolved checks.

- Quality checks can be individually muted/unmuted.

- The *Submit*/*Suggest* button is not enabled until a change over the
  initial state of the unit is detected.

- When going through all units in the translation editor, users will be
  automatically redirected back to overview.

- The Wikipedia lookup backend has been removed.


Layout Differences
------------------

- Highly customized layout and look & feel.

- Redesigned navigation scheme, including fast, easy and practical
  navigation via breadcrumb drop-downs.

- Tabs have been replaced in favor of drop-down menus.

- Critical errors are prominently displayed.

- No *Top Contributors* tables.

- No home page. Users are redirected to their preferred language pages
  instead, falling back to the project listings page.

- Single-column and wide browsing table.

- All templates are gathered in a single location (*pootle/templates*),
  and have been reorganized and sorted.

- `Modern browser support <browsers>`_. This includes latest stable
  versions of major browsers, and therefore some JavaScript libraries
  that don't rely on old browsers can be used (namely jQuery 2.x). Some
  CSS prefixes have been removed too.


Other Notable Differences
-------------------------

- Hard dependency differences. Check the *requirements/* directory for
  details.

- URLs have been unified and all follow the same scheme. URLs ending in
  *.html* have been removed altogether. ``reverse()`` and ``{% url %}``
  are used almost everywhere.