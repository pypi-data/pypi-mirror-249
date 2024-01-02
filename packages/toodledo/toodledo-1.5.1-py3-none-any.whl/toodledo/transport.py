"""Implementation"""

from contextlib import contextmanager
import datetime
from itertools import islice
from json import dumps
import logging

from requests_oauthlib import OAuth2Session

from .account import _AccountSchema
from .context import _ContextSchema
from .errors import ToodledoError
from .folder import _FolderSchema
from .task import _DumpTaskList, _TaskSchema
from .deleted_task import _DeletedTaskSchema


class AuthorizationNeeded(Exception):
    """Thrown when the token storage doesn't contain a token"""


class ToodledoSession(OAuth2Session):
    """Refresh token when we get a 429 error"""
    def __init__(self, *args, **kwargs):
        self.toodledo_logger = logging.getLogger(__name__)
        self.toodledo_refreshing = False
        self.toodledo_history_count = kwargs.pop('history_count', None)
        self.toodledo_history = []
        super().__init__(*args, **kwargs)

    def toodledo_save(self, response, method, url, data=None, headers=None,
                      **kwargs):
        if not self.toodledo_history_count:
            return
        self.toodledo_history.insert(0, (method, url, data, headers, response))
        self.toodledo_history[self.toodledo_history_count:] = []

    def request(self, *args, **kwargs):  # pylint: disable=too-many-arguments
        response = super().request(*args, **kwargs)
        if response.status_code != 429:
            self.toodledo_refreshing = False
            self.toodledo_save(response, *args, **kwargs)
            return response
        if self.toodledo_refreshing:
            response.raise_for_status()
        self.toodledo_refreshing = True
        self.toodledo_logger.warning(
            "Received 429 error - refreshing token and retrying")
        token = self.refresh_token(
            Toodledo.tokenUrl, **self.auto_refresh_kwargs)
        self.token_updater(token)
        response = super().request(*args, **kwargs)
        self.toodledo_save(response, *args, **kwargs)
        return response


class Toodledo:
    """Wrapper for the Toodledo v3 API"""
    baseUrl = "https://api.toodledo.com/3/"
    tokenUrl = baseUrl + "account/token.php"
    getAccountUrl = baseUrl + "account/get.php"
    getTasksUrl = baseUrl + "tasks/get.php"
    deleteTasksUrl = baseUrl + "tasks/delete.php"
    getDeletedTasksUrl = baseUrl + "tasks/deleted.php"
    addTasksUrl = baseUrl + "tasks/add.php"
    editTasksUrl = baseUrl + "tasks/edit.php"
    getFoldersUrl = baseUrl + "folders/get.php"
    addFolderUrl = baseUrl + "folders/add.php"
    deleteFolderUrl = baseUrl + "folders/delete.php"
    editFolderUrl = baseUrl + "folders/edit.php"
    getContextsUrl = baseUrl + "contexts/get.php"
    addContextUrl = baseUrl + "contexts/add.php"
    editContextUrl = baseUrl + "contexts/edit.php"
    deleteContextUrl = baseUrl + "contexts/delete.php"

    def __init__(self, clientId, clientSecret, tokenStorage, scope):
        self.logger = logging.getLogger(__name__)
        self.tokenStorage = tokenStorage
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.scope = scope
        self.__session = None

    @property
    def _session(self):
        if self.__session:
            return self.__session
        self.__session = self._Session()
        return self.__session

    def _Session(self):
        token = self.tokenStorage.Load()
        if token is None:
            raise AuthorizationNeeded("No token in storage")

        return ToodledoSession(
            client_id=self.clientId,
            token=token,
            auto_refresh_kwargs={
                "client_id": self.clientId,
                "client_secret": self.clientSecret
            },
            auto_refresh_url=Toodledo.tokenUrl,
            token_updater=self.tokenStorage.Save)

    @property
    def _history(self):
        return self._session.toodledo_history

    def GetFolders(self):
        """Get all the folders as folder objects"""
        folders = self._session.get(Toodledo.getFoldersUrl)
        folders.raise_for_status()
        schema = _FolderSchema()
        return [schema.load(x) for x in folders.json()]

    def AddFolder(self, folder):
        """Add folder, return the created folder"""
        response = self._session.post(
            Toodledo.addFolderUrl,
            data={
                "name": folder.name,
                "private": 1 if folder.private else 0
            })
        response.raise_for_status()
        if "errorCode" in response.json():
            self.logger.error("Toodledo error: %s", response.json())
            raise ToodledoError(response.json()["errorCode"])
        return _FolderSchema().load(response.json()[0])

    def DeleteFolder(self, folder):
        """Delete folder"""
        response = self._session.post(Toodledo.deleteFolderUrl,
                                      data={"id": folder.id_})
        response.raise_for_status()
        jsonResponse = response.json()
        if "errorCode" in jsonResponse:
            self.logger.error("Toodledo error: %s", jsonResponse)
            raise ToodledoError(jsonResponse["errorCode"])
        assert jsonResponse == {"deleted": folder.id_}, dumps(jsonResponse)

    def EditFolder(self, folder):
        """Edits the given folder to have the given properties"""
        folderData = _FolderSchema().dump(folder)
        response = self._session.post(Toodledo.editFolderUrl,
                                      data=folderData)
        response.raise_for_status()
        responseAsDict = response.json()
        if "errorCode" in responseAsDict:
            self.logger.error("Toodledo error: %s", responseAsDict)
            raise ToodledoError(responseAsDict["errorCode"])
        return _FolderSchema().load(responseAsDict[0])

    def GetContexts(self):
        """Get all the contexts as context objects"""
        contexts = self._session.get(Toodledo.getContextsUrl)
        contexts.raise_for_status()
        schema = _ContextSchema()
        return [schema.load(x) for x in contexts.json()]

    def AddContext(self, context):
        """Add context, return the created context"""
        response = self._session.post(
            Toodledo.addContextUrl,
            data={
                "name": context.name,
                "private": 1 if context.private else 0
            })
        response.raise_for_status()
        if "errorCode" in response.json():
            self.logger.error("Toodledo error: %s", response.json())
            raise ToodledoError(response.json()["errorCode"])
        return _ContextSchema().load(response.json()[0])

    def DeleteContext(self, context):
        """Delete context"""
        response = self._session.post(
            Toodledo.deleteContextUrl, data={"id": context.id_})
        response.raise_for_status()
        jsonResponse = response.json()
        if "errorCode" in jsonResponse:
            self.logger.error("Toodledo error: %s", jsonResponse)
            raise ToodledoError(jsonResponse["errorCode"])
        assert jsonResponse == {"deleted": context.id_}, dumps(jsonResponse)

    def EditContext(self, context):
        """Edits the given folder to have the given properties"""
        contextData = _ContextSchema().dump(context)
        response = self._session.post(
            Toodledo.editContextUrl, data=contextData)
        response.raise_for_status()
        responseAsDict = response.json()
        if "errorCode" in responseAsDict:
            self.logger.error("Toodledo error: %s", responseAsDict)
            raise ToodledoError(responseAsDict["errorCode"])
        return _ContextSchema().load(responseAsDict[0])

    def GetAccount(self):
        """Get the Toodledo account"""
        accountInfo = self._session.get(Toodledo.getAccountUrl)
        accountInfo.raise_for_status()
        return _AccountSchema().load(accountInfo.json())

    def GetTasks(self, params=None, before=None, after=None, comp=None,
                 id_=None, fields=None):
        """Get the tasks filtered by the given params.

        You can params in the params array as for the raw API, or in the
        `before`, `after`, `comp`, `id_`, and `fields` keywords arguments."""
        if params is None:
            params = {}
        if before:
            params['before'] = before
        if after:
            params['after'] = after
        if comp is not None:
            params['comp'] = comp
        if id_:
            params['id'] = id_
        if fields:
            params['fields'] = fields

        allTasks = []
        limit = 1000  # single request limit
        start = 0
        params = params.copy()
        if 'before' in params and isinstance(params['before'],
                                             datetime.datetime):
            params['before'] = params['before'].timestamp()
        if 'after' in params and isinstance(params['after'],
                                            datetime.datetime):
            params['after'] = params['after'].timestamp()
        while True:
            self.logger.debug("Start: %d", start)
            params["start"] = start
            params["num"] = limit
            response = self._session.get(Toodledo.getTasksUrl, params=params)
            response.raise_for_status()
            tasks = response.json()
            if "errorCode" in tasks:
                self.logger.error("Toodledo error: %s", tasks)
                raise ToodledoError(tasks["errorCode"])
            # the first field contains the count or the error code
            allTasks.extend(tasks[1:])
            self.logger.debug("Retrieved %d tasks", len(tasks) - 1)
            if len(tasks) - 1 < limit:
                break
            start += limit
        schema = _TaskSchema()
        for x in allTasks:
            # This field is sometimes being leaked by the API and should be
            # ignored.
            x.pop('repeatfrom', None)
        return [schema.load(x) for x in allTasks]

    def GetDeletedTasks(self, after):
        """Get a list of deleted tasks.

        Required arguments:
        after -- Return tasks deleted after this UNIX timestamp
        """
        if isinstance(after, datetime.datetime):
            after = after.timestamp()
        response = self._session.get(Toodledo.getDeletedTasksUrl,
                                     params={'after': after})
        response.raise_for_status()
        deleted = response.json()
        if "errorCode" in deleted:
            self.logger.error("Toodledo error: %s", deleted)
            raise ToodledoError(deleted["errorCode"])
        # the first field contains the count or the error code
        self.logger.debug("Retrieved %d deleted tasks", len(deleted) - 1)
        schema = _DeletedTaskSchema()
        return [schema.load(x) for x in deleted[1:]]

    def EditTasks(self, taskList):
        """Edit existing tasks as indicated in the specified task objects.

        Only specify fields that need to be changed, except for the id_ field,
        which must always be specified. In particular, note that if you specify
        `None` for a field, that means to erase it, not to ignore it!"""
        # Any iterator can be passed in, not just a list.
        # The iterator we create here remembers our place in the input as we
        # step through it in chunks using islice.
        taskList = iter(taskList)
        limit = 50  # single request limit
        responses = []
        while True:
            listDump = _DumpTaskList(list(islice(taskList, limit)))
            if not listDump:
                break
            response = self._session.post(
                Toodledo.editTasksUrl, data={"tasks": dumps(listDump)})
            response.raise_for_status()
            self.logger.debug("Response: %s,%s", response, response.text)
            taskResponse = response.json()
            errors = []
            if isinstance(taskResponse, list):
                for response in taskResponse:
                    if "errorCode" in response:
                        errors.append(ToodledoError(response["errorCode"]))
            elif "errorCode" in taskResponse:
                errors.append(ToodledoError(taskResponse["errorCode"]))
            if len(errors) == 1:
                raise errors[0]
            if errors:
                # pylint: disable=broad-exception-raised
                raise Exception(str(errors))
                # pylint: enable=broad-exception-raised
            responses.extend(taskResponse)
        schema = _TaskSchema()
        return [schema.load(t) for t in responses]

    def AddTasks(self, taskList):
        """Add the given tasks"""
        taskList = iter(taskList)  # See EditTasks
        limit = 50  # single request limit
        responses = []
        while True:
            listDump = _DumpTaskList(list(islice(taskList, limit)))
            if not listDump:
                break
            response = self._session.post(
                Toodledo.addTasksUrl, data={"tasks": dumps(listDump)})
            response.raise_for_status()
            taskResponse = response.json()
            errors = []
            if isinstance(taskResponse, list):
                for response in taskResponse:
                    if "errorCode" in response:
                        errors.append(ToodledoError(response["errorCode"]))
            elif "errorCode" in taskResponse:
                errors.append(ToodledoError(taskResponse["errorCode"]))
            if len(errors) == 1:
                raise errors[0]
            if errors:
                # pylint: disable=broad-exception-raised
                raise Exception(str(errors))
                # pylint: enable=broad-exception-raised
            responses.extend(taskResponse)
        schema = _TaskSchema()
        return [schema.load(t) for t in responses]

    def DeleteTasks(self, taskList):
        """Delete the given tasks"""
        if len(taskList) == 0:
            return
        taskIdList = [task.id_ for task in taskList]
        limit = 50  # single request limit
        start = 0
        while True:
            self.logger.debug("Start: %d", start)
            response = self._session.post(
                Toodledo.deleteTasksUrl,
                data={
                    "tasks": dumps(taskIdList[start:start + limit])
                })
            response.raise_for_status()
            if "errorCode" in response.json():
                raise ToodledoError(response.json()["errorCode"])
            if len(taskIdList[start:start + limit]) < limit:
                break
            start += limit

    def save(self):
        """No-op for drop-in compatibility with TaskCache"""

    def load_from_path(self, path=None):
        """No-op for drop-in compatibility with TaskCache"""

    def dump_to_path(self, path=None):
        """No-op for drop-in compatibility with TaskCache"""

    @contextmanager
    def caching_everything(self):
        yield

    def update(self):
        """No-op for drop-in compatibility with TaskCache"""
