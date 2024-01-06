import os
import warnings
import sqlalchemy.exc as sqlerrors


def deprecate(new_refer, message=""):
    """
    python -W
    PYTHONWARNINGS=default  # Warn once per call location
    PYTHONWARNINGS=error    # Convert to exceptions
    PYTHONWARNINGS=always   # Warn every time
    PYTHONWARNINGS=module   # Warn once per calling module
    PYTHONWARNINGS=once     # Warn once per Python process
    PYTHONWARNINGS=ignore   # Never warn
    
    ##; 这个无效
    # print(os.environ.get("PYTHONWARNINGS"))
    # os.environ["PYTHONWARNINGS"] = "once"
    
    ##; 要查看 DeprecationWarning，你可以在程序开始时添加以下代码：
    warnings.simplefilter('default', DeprecationWarning)

    ##; 或者，你可以使用命令行运行 Python 程序时加上 -W default 参数来显示所有警告：
    python -W default your_script.py
    
    :param new_refer: 
    :param message: 
    :return: 
    """
    warnings.warn(message, DeprecationWarning, stacklevel=2)
    return new_refer


class PycoSqlError(Exception, sqlerrors.DontWrapMixin):
    msg = "PycoSqlError!"
    errno = 40070

    def __init__(self, msg="", errno=40070, _debug_info=None, **kwargs):
        self.msg = msg
        self.kwargs = kwargs
        self.description = f"<{self.__class__.__name__}>:{errno}, {msg}"
        self._debug_info = _debug_info

    def to_dict(self):
        return dict(
            errno=self.errno,
            error_msg=self.msg,
            error_kws=self.kwargs,
        )

    def __call__(self, msg="", **kwargs):
        ##; 兼容旧代码，减少异常类
        kwargs.setdefault("errno", self.errno)
        m = self.__class__(msg, **kwargs)
        return m

    def __str__(self):
        return self.description
