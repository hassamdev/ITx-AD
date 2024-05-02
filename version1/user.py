class Object:
    NAME = None
    DN = None
    OBJECT_CLASS= None
    def __init__(self,_dn,_name,_object_class) -> None:
        self.DN = _dn
        self.NAME = _name
        self.OBJECT_CLASS = _object_class

    def __str__(self) -> str:
        return self.DN