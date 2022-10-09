from watcher.dummy.domain.ports.dummy_ports import ListUser


class ListDummyUsers(ListUser):
    def __init__(self, sth):
        self.sth = sth

    def all(self):
        return {"sth": 'all users' + self.sth}
