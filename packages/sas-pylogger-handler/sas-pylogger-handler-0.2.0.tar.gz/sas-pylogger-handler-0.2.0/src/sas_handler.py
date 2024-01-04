import logging
from logging import Handler


class SASHandler(logging.Handler):
    """
    A handler class which writes formatted logging records to the SAS log.
    """

    def __init__(self, sas):
        """
        Connects to the specified SAS Session and use it for logging.
        """

        self._sas = sas
        if self._sas is None:
            raise Exception("The SASsession object cant not be empty")

        Handler.__init__(self)

    def sasLogMessage(self, message, messageType='NOTE'):
        """Writes a well formed message to the SAS Log

        	message {String} - Message that should be written to the SAS log
        	messageType {String - default: NOTE} - NOTE, writes a Note to the SAS log
        									- WARNING, writes a Warning to the SAS log
        									- ERROR, writes an Error to the SAS log
        """
        self._sas.submit(f"%put {messageType.upper()}: Python-Subprocess - {message};")

    def emit(self, record):
        """
        Emit a record to the SAS logger, because the SAS logger only have 3 levels it will match the standard levels to
        the SAS levels.
        """
        try:
            msg = self.format(record)
            level_name = logging.getLevelName(self.level)

            if level_name in ["CRITICAL", "FATAL", "ERROR"]:
                sas_message_type = "ERROR"
            elif level_name in ["WARNING", "WARN"]:
                sas_message_type = "WARNING"
            elif level_name in ["INFO", "DEBUG"]:
                sas_message_type = "NOTE"
            else:
                sas_message_type = None

            if sas_message_type is not None:
                self.sasLogMessage(msg, sas_message_type)
        except Exception:
            self.handleError(record)
