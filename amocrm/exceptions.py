class AmocrmError(Exception): pass
class MissingValue(AmocrmError): pass
class MissingArgument(AmocrmError): pass
class EmptyArgument(AmocrmError): pass
class WrongValueType(AmocrmError): pass
class ForbiddenValueKey(AmocrmError): pass
class NotAnEntity(AmocrmError): pass
