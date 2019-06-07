def get_output_handler(logger=None, severity=None):
    """
    Helper function to define a how to handle output. If a logger is provided, along with the corresponding severity,
    the logger will be used. Otherwise, will print to console.

    :param logger: logger object, from the 'logging' module
    :param severity: string definining severity og the logs. One of 'critical', 'error', 'warning', 'info', 'debug'
    :return: function object, either the logger method corresponding to the severity, or the print method
    """
    if logger is not None:
        if severity.lower() not in ['critical', 'error', 'warning', 'info', 'debug']:
            raise ValueError("severity must be one of 'critical', 'error', 'warning', 'info', 'debug'. "
                             "Value provided instead: {}".format(str(severity)))
        return getattr(logger, severity.lower())
    else:
        return print
