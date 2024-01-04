

import typing

from .AbstractTimeStampFormatter import AbstractTimeStampFormatter
from .AbstractLogMessageFormatter import AbstractLogMessageFormatter
from .DefaultTimeStampFormatter import DefaultTimeStampFormatter
from ..EnumExtensitivity import EnumExtensitivity







#
# This is a default formatter for log messages. It produces human readable output for log messages.
#
class LogMessageFormatter(AbstractLogMessageFormatter):

	################################################################################################################################
	## Constants
	################################################################################################################################

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self,
			bIncludeIDs:bool = False,
			fillChar:str = "\t",
			timeStampFormatter = None,
			bLogLevelRightAligned:bool = True,
		):

		assert isinstance(bIncludeIDs, bool)
		self.__includeIDs = bIncludeIDs

		assert isinstance(fillChar, str)
		self.__fillChar = fillChar
		self.__indentBuffer = fillChar

		self.__outputMode = EnumExtensitivity.FULL

		if timeStampFormatter is None:
			timeStampFormatter = DefaultTimeStampFormatter()
		else:
			assert callable(timeStampFormatter)
		self.__timeStampFormatter = timeStampFormatter

		self.__logLevelToStrMap = AbstractLogMessageFormatter.LOG_LEVEL_TO_STR_MAP__RIGHT_ALIGNED if bLogLevelRightAligned \
			else AbstractLogMessageFormatter.LOG_LEVEL_TO_STR_MAP__LEFT_ALIGNED
	#

	################################################################################################################################
	## Properties
	################################################################################################################################

	@property
	def timeStampFormatter(self) -> typing.Union[AbstractTimeStampFormatter,None]:
		return self.__timeStampFormatter
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __formatException(self, prefix:str, sExClass:str, sLogMsg:typing.Union[str,None], listStackTraceEntries:typing.Union[list,tuple], nestedException:typing.Union[list,tuple,None], ret:typing.List[str]):
		if sLogMsg is None:
			sLogMsg = ""

		if sLogMsg:
			ret.append(prefix + sExClass + ": " + sLogMsg)
		else:
			ret.append(prefix + sExClass)

		if listStackTraceEntries:
			if self.__outputMode == EnumExtensitivity.FULL:
				for (stPath, stLineNo, stModuleName, stLine) in listStackTraceEntries:
					ret.append(prefix + "    | " + stPath + ":" + str(stLineNo) + " " + stModuleName + "    # " + stLine)
			elif self.__outputMode == EnumExtensitivity.SHORTED:
				stPath, stLineNo, stModuleName, stLine = listStackTraceEntries[-1]
				ret.append(prefix + "    | " + stPath + ":" + str(stLineNo) + " " + stModuleName + "    # " + stLine)

		if nestedException:
			self.__formatException(prefix + "    ", nestedException[0], nestedException[1], nestedException[2], nestedException[3], ret)
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	#
	# Create and return a string representation of the specified log entry.
	#
	# @param		list logEntryStruct			A log entry structure. See <c>AbstractLogger._logi()</c> for a detailed description.
	# @return		str|str[]					Returns the string representation of the log entry, either as a single string or a list of strings.
	#
	def format(self, logEntryStruct) -> typing.Union[str,typing.List[str]]:
		sStructType = logEntryStruct[0]

		sID = str(logEntryStruct[1]) if (logEntryStruct != None) else "-"

		indentationLevel = logEntryStruct[2]
		while indentationLevel > len(self.__indentBuffer):
			self.__indentBuffer += self.__fillChar
		sIndent = self.__indentBuffer[0:indentationLevel]

		sParentID = str(logEntryStruct[3]) if (logEntryStruct != None) else "-"

		sTimeStamp = self.__timeStampFormatter(logEntryStruct[4])

		sLogType = self.__logLevelToStrMap[logEntryStruct[5]]

		# ----

		s = sIndent
		if self.__includeIDs:
			s += "(" + sParentID + "|" + sID + ") "
		s += "[" + sTimeStamp + "] "

		if sStructType == "txt":
			sLogMsg = logEntryStruct[6]
			if sLogMsg is None:
				sLogMsg = ""
			return s + sLogType + ": " + sLogMsg

		elif sStructType == "ex":
			sExClass = logEntryStruct[6]
			sLogMsg = logEntryStruct[7]
			if sLogMsg is None:
				sLogMsg = ""
			listStackTraceEntries = logEntryStruct[8]
			nestedException = logEntryStruct[9]

			ret = []
			self.__formatException(s + " " + sLogType + ": ", sExClass, sLogMsg, listStackTraceEntries, nestedException, ret)

			return ret

		elif sStructType == "desc":
			sLogMsg = logEntryStruct[6]
			if sLogMsg is None:
				sLogMsg = ""
			return s + sLogType + ": " + sLogMsg

		else:
			raise Exception("Invalid structure type: " + repr(sStructType))
	#

#



DEFAULT_LOG_MESSAGE_FORMATTER = LogMessageFormatter()








