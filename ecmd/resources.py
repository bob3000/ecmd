import abc
import ecmd.api


class Resource(abc.ABC):

    def __init__(self, api, res_type, uid):
        self.api = api
        self.res_type = res_type
        self.uid = uid

    def __getattr__(self, name):
        """
        Attributes are fetched lazily
        """
        if name not in self.__dict__:
            self.load()
        return self.__dict__[name]

    def load(self):
        try:
            res = self.api.call(
                "/{}s/{}/info".format(self.res_type, self.uid))
            if 200 != res.code:
                raise ResourceException("API returned {}".format(res.code))
            attributes = {k.replace(":", "_"): v
                          for k, v in res.payload.items()}
            self.__dict__.update(attributes)
        except ecmd.api.ApiException as e:
            raise ResourceException(str(e))


class Drive(Resource):

    def __init__(self, api, uid=None):
        res_type = self.__class__.__name__.lower()
        super().__init__(api, res_type, uid)


class Server(Resource):

    def __init__(self, api, uid=None):
        res_type = self.__class__.__name__.lower()
        super().__init__(api, res_type, uid)


class ResourceException(Exception):
    pass
