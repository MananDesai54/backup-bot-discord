#!/usr/bin/env python3

# if __name__ == '__main__':
import mongoengine as db
import os


def connectMongoDB():
    conn = db.connect(host=os.getenv('MONGO_URI'), alias='botDB')
    print(f"Connected to the Database: {conn}")


class Channel(db.EmbeddedDocument):
    id = db.StringField(required=True)
    name = db.StringField(required=True)
    category = db.StringField(required=True)


class Role(db.EmbeddedDocument):
    id = db.StringField(required=True)
    name = db.StringField(required=True)
    permissions = db.ListField(db.StringField())


class Backup(db.Document):
    backupName = db.StringField()
    textChannels = db.ListField(db.EmbeddedDocumentField(Channel))
    voiceChannels = db.ListField(db.EmbeddedDocumentField(Channel))
    categories = db.ListField(db.StringField())
    roles = db.ListField(db.EmbeddedDocumentField(Role))

    def to_json(self):
        return {
            "backupName": self.backupName,
            "textChannels": self.textChannels,
            "voiceChannels": self.voiceChannels,
            "categories": self.categories,
            "roles": self.roles,
        }

    def create(name, textChannels, voiceChannels, categories, roles):
        backup = Backup(backupName=name,
                        textChannels=textChannels,
                        voiceChannels=voiceChannels,
                        categories=categories,
                        roles=roles)
        backup.save()
        return backup


class TextMessages(db.Document):
    channelId = db.StringField(required=True)
    messages = db.ListField(db.StringField())

    def to_json(self):
        return {
            "channelId": self.channelId,
            "messages": self.messages,
        }

    def create(channelId, messages):
        textMessages = TextMessages(channelId=channelId, messages=messages)
        textMessages.save()
        return textMessages
