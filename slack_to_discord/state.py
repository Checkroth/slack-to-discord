
"""
Module that takes the data processed by importer and dumps it in to a sqlite database.
This is to create a stronger separation of concerns between parsing and slack posting.
It unlocks the ability to more easily:

1. Multiprocess channels so the import goes faster
2. Maintain a repeatable state so that if the process fails,
    we can pick up where we left off instead of starting over
    or requiring someone to edit a big raw export file.
"""
import peewee

class Message(peewee.Model):
    pass

class User(peewee.Model):
    slack_id = peewee.CharField(unique=True)
    name = peewee.CharField()
    profile_image = peewee.CharField()


class Channel(peewee.Model):
    topic = peewee.CharField()
    is_private = peewee.BooleanField()

class SlackFile(peewee.Model):
    name = peewee.CharField()
    title = peewee.CharField()
    url = peewee.CharField()
    # thumbs = peewee.???

class Message(peewee.Model):
    SUBTYPES = {
        "channel_join",
        "channel_leave",
        "channel_archive",
        "channel_unarchive",
        "me_message",
        "reminder_add",
        "file_comment",
        "channel_topic"
    }
    channel = peewee.ForeignKeyField(Channel, backref="messages")
    user = peewee.ForeignKeyField(User, backref="messages")
    subtype = peewee.CharField()
    topic = peewee.CharField()
    is_pinned = peewee.BooleanField()
    attachment = peewee.ForeignKeyField(SlackFile, unique=True)
    timestamp = peewee.DateTimeField()
    text = peewee.TextField()
    reply_to = peewee.ForeignKeyField(Message, backref="replies")
    
    # For picking up where we left off -- this should ony be "TRUE"
    #     if we've actually posted it to discord already.
    synced_to_discord = peewee.BooleanField()

class Reaction(peewee.Model):
    user = peewee.ForeignKeyField(User)
    message = peewee.ForeignKeyField(Message, backref="reactions")

