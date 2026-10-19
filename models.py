import abc
import datetime


class CustomMap:

    def __init__(self):
        self._pairs = []

    @property
    def pairs(self):
        return self._pairs

    @pairs.setter
    def pairs(self, v):
        self._pairs = v

    def set(self, k, v):
        for i, (kk, _) in enumerate(self._pairs):
            if kk == k:
                self._pairs[i] = (k, v)
                return
        self._pairs.append((k, v))

    def get(self, k, default=None):
        for kk, vv in self._pairs:
            if kk == k:
                return vv
        return default

    def __len__(self):
        return len(self._pairs)

    def __contains__(self, k):
        return any(kk == k for kk, _ in self._pairs)

    def __iter__(self):
        return iter(self._pairs)

    def __eq__(self, o):
        return isinstance(o, CustomMap) and self._pairs == o._pairs

    def __lt__(self, o):
        if not isinstance(o, CustomMap):
            return NotImplemented
        return len(self._pairs) < len(o._pairs)

    def __repr__(self):
        return f"CustomMap({self._pairs})"

    def __str__(self):
        return f"CustomMap<{len(self._pairs)} пар>"


class BaseEntity(abc.ABC):

    def __init__(self, eid=0):
        self._id = eid

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, v):
        self._id = v

    @abc.abstractmethod
    def describe(self):
        ...


class Task(BaseEntity):
    FIELDS = ["title", "description", "type", "project", "priority", "completed"]
    TYPES = ["рабочая", "учебная", "обычная"]

    def __init__(self, title="", description="", ttype="обычная",
                 project="", priority=2, completed=False, eid=0):
        super().__init__(eid)
        self._title = title
        self._description = description
        self._type = ttype
        self._project = project
        self._priority = priority
        self._completed = completed

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, v):
        self._title = v

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, v):
        self._description = v

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, v):
        self._type = v

    @property
    def project(self):
        return self._project

    @project.setter
    def project(self, v):
        self._project = v

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, v):
        self._priority = v

    @property
    def completed(self):
        return self._completed

    @completed.setter
    def completed(self, v):
        self._completed = v

    def describe(self):
        return f"{self.title} ({self.type}, P{self.priority})"

    def to_row(self):
        return [self.title, self.description, self.type, self.project,
                str(self.priority), str(self.completed)]

    @staticmethod
    def from_row(row, eid):
        return Task(row[0], row[1], row[2], row[3],
                    int(row[4]), row[5].lower() == "true", eid)

    def __eq__(self, o):
        return isinstance(o, Task) and self.id == o.id

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title!r})"

    def __str__(self):
        return self.title

    def __lt__(self, o):
        if not isinstance(o, Task):
            return NotImplemented
        return self.priority < o.priority

    def __hash__(self):
        return hash(self.id)

    def __len__(self):
        return len(self.title)


class Session(BaseEntity):
    def __init__(self, login, time_in=None, time_out=None, eid=0):
        super().__init__(eid)
        self._login = login
        self._time_in = time_in or datetime.datetime.now()
        self._time_out = time_out

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, v):
        self._login = v

    @property
    def time_in(self):
        return self._time_in

    @time_in.setter
    def time_in(self, v):
        self._time_in = v

    @property
    def time_out(self):
        return self._time_out

    @time_out.setter
    def time_out(self, v):
        self._time_out = v

    def describe(self):
        return f"{self.login}: {self.time_in:%d.%m.%Y %H:%M:%S}"

    def __eq__(self, o):
        return (isinstance(o, Session)
                and self.login == o.login
                and self.time_in == o.time_in)

    def __repr__(self):
        return f"Session({self.login!r})"

    def __str__(self):
        return self.login

    def __lt__(self, o):
        if not isinstance(o, Session):
            return NotImplemented
        return self.time_in < o.time_in

    def __hash__(self):
        return hash((self.login, self.time_in))

    def __len__(self):
        return len(self.login)