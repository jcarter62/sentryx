from django.db import models

# Create your models here.


class SessionData(models.Model):
    id = models.AutoField(primary_key=True)
    session = models.CharField(max_length=50, null=True, blank=True)
    key_name = models.CharField(max_length=50, null=True, blank=True)
    key_text = models.CharField(max_length=2048, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.session + ': ' + self.key_name + ' = ' + self.key_text

    class Meta:
        ordering = ['session', 'key_name']


class SessionInfo(models.Model):
    record_id = models.IntegerField(default=0, blank=True, null=True)
    session_id = models.CharField(max_length=50, null=True, blank=True)
    key_name = models.CharField(max_length=50, null=True, blank=True)
    key_text = models.CharField(max_length=2048, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.session_id + ': ' + self.key_name + ' = ' + self.key_text

    class Meta:
        ordering = ['session_id', 'key_name']


class Session_Info_Data:
    session_id = ''
    session_data = {}

    def __init__(self, session_id):
        self.session_id = session_id
        self.session_info = SessionInfo.objects.filter(session_id=self.session_id)
        self.session_data = {}
        for session in self.session_info:
            self.session_data[session.key_name] = session.key_text

    def get_session_data(self, key):
        if key in self.session_data:
            return self.session_data[key]
        else:
            return ''

    def set_session_data(self, key, value):
        self.session_data[key] = value
        self.save_session_data()

    def remove_session_data(self, key):
        if key in self.session_data:
            del self.session_data[key]
            self.save_session_data()

    def save_session_data(self):
        for key in self.session_data:
            session = SessionInfo.objects.filter(session_id=self.session_id, key_name=key)
            if session:
                session = session[0]
                session.key_text = self.session_data[key]
                session.save()
            else:
                session = SessionInfo(session_id=self.session_id, key_name=key, key_text=self.session_data[key])
                session.save()

