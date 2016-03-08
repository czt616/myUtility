"""
define Exceptions
"""

class ApiCallException(Exception):
        def __init__(self,url):
            self.url = url
        def __str__(self):
            error_message = "something went wrong when calling api\n"
            error_message += "error url:\n%s\n" %self.url
            print error_message
            return repr(error_message)

class ResultErrorException(Exception):
        def __init__(self,content, detail):
            self.content = content
            self.detail = detail
        def __str__(self):
            error_message = "unexpected result\n"
            error_message += self.detail
            error_message += "result is:\n%s\n" %self.content
            return error_message

class NoClassException(Exception):
        def __init__(self,content,entity):
            self.content = content
            self.entity = entity
        def __str__(self):
            error_message = "entity %s does not have class!\n" %self.entity
            error_message += "the returned result is:\n%s" %self.content
            return error_message