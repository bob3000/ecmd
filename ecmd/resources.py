import abc.ABC


class Resource(abc.ABC):

    def __init__(self, api, res_type, uid):
        self.api = api
        self.res_type = res_type
        self.uid = uid

    def __getattr__(self, name):
        """
        Attributes are fetched lazily
        """
        if name not in locals():
            try:
                res = self.api.call("/{}s/info".format(self.res_type))
                if "200" not in res.code:
                    raise ResourceException("API returned {}".format(res.code))
                self.__dict__.update(res.payload)
            except ecmd.lib.api.ApiException as e:
                raise ResourceException(str(e))
        return locals()[name]


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
