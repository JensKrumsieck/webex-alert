from configparser import ConfigParser
from typing import Any
from util import root_dir

default_section = "webex"
mod_section = "moderators"

class Config():
    def __init__(self):
        self.config = ConfigParser()
        self.config.read(root_dir + "/config.ini")
        if not self.config.has_section(default_section):
            self.config.add_section(default_section)

    def get_room_id(self):
        try:
            room_id = self.config.get(default_section, "room_id")
        except:
            room_id = ""
        return room_id

    def get_room_options(self):
        try:
            room_title = self.config.get(default_section, "room_title")
        except:
            room_title = "❗ [Test] IT Security Alerts ❗" # default room title
        
        try:
            isLocked = self.config.getboolean(default_section, "isLocked")
        except:
            isLocked = True

        try:
            isPublic = self.config.getboolean(default_section, "isPublic")
        except:
            isPublic = False

        try:
            isAnnouncementOnly = self.config.getboolean(default_section, "isAnnouncementOnly")
        except:
            isAnnouncementOnly = True

        return {"title": room_title, "isLocked": isLocked, "isPublic": isPublic, "isAnnouncementOnly": isAnnouncementOnly}
    
    def get_moderators(self):
        try:
            raw = self.config.get(mod_section, "moderators")
            moderators = raw.split(",")
        except:
            moderators = []
        return moderators
    
    def set_room_options(self, room):
        self.config.set(default_section, "room_id", room['id'])
        self.config.set(default_section, "title", room["title"])
        self.config.set(default_section, "isAnnouncementOnly", str(room["isAnnouncementOnly"]))
        self.config.set(default_section, "isLocked", str(room["isLocked"]))
        self.config.set(default_section, "isPublic", str(room["isPublic"]))
        self.save()


    def save(self):
        with open(root_dir + "/config.ini", "w") as f:
            self.config.write(f)