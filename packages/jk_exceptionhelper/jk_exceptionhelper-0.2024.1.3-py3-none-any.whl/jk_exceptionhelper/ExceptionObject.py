

__all__ = (
	"ExceptionObject",
)

import typing
import traceback

from .StackTraceItem import StackTraceItem















ExceptionObject = typing.NewType("ExceptionObject", object)





# def _analyseNestedException(exception) -> ExceptionObject:
# 	print(">4>>", type(exception.__traceback__), exception.__traceback__)

# 	exceptionLines = []
# 	for line in str(exception).splitlines():
# 		line = line.strip()
# 		if len(line) > 0:
# 			exceptionLines.append(line)
# 	exceptionTextHR = " ".join(exceptionLines)
# 	if not exceptionTextHR:
# 		exceptionTextHR = None

# 	if exception.__context__:
# 		nestedException = _analyseNestedException(exception.__context__)
# 	else:
# 		nestedException = None

# 	return ExceptionObject(exception, exception.__class__.__name__, exceptionTextHR, None, nestedException)
# #





class ExceptionObject(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor.
	#
	def __init__(self, exceptionClass:type, exceptionClassName:str, exceptionTextHR:str, stackTrace:typing.List[StackTraceItem], nestedException):
		self.exceptionClass:type = exceptionClass

		self.exceptionClassName:str = exceptionClassName

		if exceptionTextHR is not None:
			assert isinstance(exceptionTextHR, str)
		self.exceptionTextHR:str = exceptionTextHR

		if stackTrace is not None:
			assert isinstance(stackTrace, (list, tuple))
			for item in stackTrace:
				assert isinstance(item, StackTraceItem)
			self.stackTrace:typing.List[StackTraceItem] = stackTrace
		else:
			self.stackTrace:typing.List[StackTraceItem] = None

		if nestedException is not None:
			assert isinstance(nestedException, ExceptionObject)
		self.nestedException:typing.Union[ExceptionObject,None] = nestedException
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def toStrList(self) -> typing.List[str]:
		outStrList = []

		e = self
		indent = ""
		while True:
			outStrList.append(indent + e.exceptionClassName)
			if e.exceptionTextHR is not None:
				outStrList.append(indent + ": exceptionTextHR:")
				outStrList.append(indent + ":\t" + e.exceptionTextHR)
			if e.stackTrace is not None:
				outStrList.append(indent + ": stackTrace:")
				for item in reversed(e.stackTrace):
					outStrList.append(indent + ":\t" + str(item))
			if e.nestedException:
				e = e.nestedException
				outStrList.append(indent + "\- nestedException:")
				indent += "\t"
			else:
				outStrList.append(indent + "\-")
				break

		return outStrList
	#

	def dump(self, prefix:str = "") -> None:
		e = self
		indent = prefix
		while True:
			print(indent + e.exceptionClassName)
			if e.exceptionTextHR is not None:
				print(indent + ": exceptionTextHR:")
				print(indent + ":\t" + e.exceptionTextHR)
			if e.stackTrace is not None:
				print(indent + ": stackTrace:")
				for item in reversed(e.stackTrace):
					print(indent + ":\t" + str(item))
			if e.nestedException:
				e = e.nestedException
				print(indent + "\- nestedException:")
				indent += "\t"
			else:
				print(indent + "\-")
				break
	#

	#
	# Convert this object to JSON (recursively).
	#
	# @param	bool bRecursive		If `True` (which is the default) nested exceptions are serialized as well. If `False` these get skipped.
	#
	def toJSON(self, bRecursive:bool = True) -> dict:
		ret = {
			"text": self.exceptionTextHR,
			"exception": self.exceptionClassName,
		}
		if self.stackTrace is not None:
			ret["stacktrace"] = [ x.toJSON() for x in self.stackTrace ]
		if bRecursive and self.nestedException:
			ret["nested"] = self.nestedException.toJSON()
		else:
			ret["nested"] = None
		return ret
	#

	#
	# Convert this object to JSON (only this level).
	#
	def toJSON_flat(self):
		ret = {
			"text": self.exceptionTextHR,
			"exception": self.exceptionClassName,
		}
		if self.stackTrace is not None:
			ret["stacktrace"] = [ x.toJSON() for x in self.stackTrace ]
		else:
			ret["stacktrace"] = None
		return ret
	#

	################################################################################################################################
	## Public Static Methods
	################################################################################################################################

	@staticmethod
	def fromJSON(data:dict):
		assert isinstance(data, dict)
		return ExceptionObject(
			None,
			data["exception"],
			data["text"],
			([ StackTraceItem.fromJSON(x) for x in data["stacktrace"] ]) if data.get("stacktrace") else None,
			ExceptionObject.fromJSON(data["nested"]) if data.get("nested") else None
		)
	#

	#
	# This method constructs an ExceptionObject instance from an existing exception.
	#
	@staticmethod
	def fromException(
			exception:BaseException,
			ignoreJKTypingCheckFunctionSignatureFrames:bool = False,
			ignoreJKTestingAssertFrames:bool = False,
			ignoreJKLoggingFrames:bool = False,
			_bWithFullStackTrace:bool = True
		) -> ExceptionObject:

		assert isinstance(exception, BaseException)
		assert isinstance(ignoreJKTypingCheckFunctionSignatureFrames, bool)
		assert isinstance(ignoreJKTestingAssertFrames, bool)
		assert isinstance(ignoreJKLoggingFrames, bool)

		# ----

		_args = exception.args
		nestedException = None
		if _args and isinstance(_args[-1], ExceptionObject):
			nestedException = _args[-1]
			_args = _args[:-1]

		if len(_args) == 0:
			sArgs = ""
		elif len(_args) == 1:
			sArgs = str(_args[0])
		else:
			sArgs = str(_args)

		exceptionLines = []
		for line in sArgs.splitlines():
			line = line.strip()
			if len(line) > 0:
				exceptionLines.append(line)
		exceptionTextHR = " ".join(exceptionLines)
		if not exceptionTextHR:
			exceptionTextHR = None

		stackTrace1 = []
		for stElement in traceback.extract_tb(exception.__traceback__):
			if ignoreJKTypingCheckFunctionSignatureFrames:
				if (
						(stElement.filename.find("jk_typing/checkFunctionSignature.py") >= 0) or
						(stElement.filename.find("jk_typing\\checkFunctionSignature.py") >= 0)
					):
					continue
			if ignoreJKTestingAssertFrames:
				if (
						(stElement.filename.find("jk_testing/Assert.py") >= 0) or
						(stElement.filename.find("jk_testing\\Assert.py") >= 0)
					):
					continue
			if ignoreJKLoggingFrames:
				if (
						(stElement.filename.find("jk_logging/") >= 0) or
						(stElement.filename.find("jk_logging\\") >= 0)
					):
					continue
			stackTrace1.append(StackTraceItem(
				stElement.filename,
				stElement.lineno,
				stElement.name,
				stElement.line
			))

		stackTrace2 = []
		if _bWithFullStackTrace:
			for stElement in traceback.extract_stack():
				if ignoreJKTypingCheckFunctionSignatureFrames:
					if (
							(stElement.filename.find("jk_typing/checkFunctionSignature.py") >= 0) or
							(stElement.filename.find("jk_typing\\checkFunctionSignature.py") >= 0)
						):
						continue
				if ignoreJKTestingAssertFrames:
					if (
							(stElement.filename.find("jk_testing/Assert.py") >= 0) or
							(stElement.filename.find("jk_testing\\Assert.py") >= 0)
						):
						continue
				if ignoreJKLoggingFrames:
					if (
							(stElement.filename.find("jk_logging/") >= 0) or
							(stElement.filename.find("jk_logging\\") >= 0)
						):
						continue
				stackTrace2.append(StackTraceItem(
					stElement.filename,
					stElement.lineno,
					stElement.name,
					stElement.line
				))

			# remove last stacktrace item as it represents a line in the current method
			del stackTrace2[-1]

		stackTrace = stackTrace2
		stackTrace.extend(stackTrace1)

		# if not nestedException:
		# 	if hasattr(exception, "cause"):
		# 		_n = exception.cause
		# 		if isinstance(_n, ExceptionObject):
		# 			nestedException = _n
		# 		else:
		# 			if exception.__context__:
		# 				nestedException = _analyseNestedException(exception.__context__)
		if not nestedException:
			if exception.__context__:
				nestedException = ExceptionObject.fromException(
					exception.__context__,
					ignoreJKTypingCheckFunctionSignatureFrames,
					ignoreJKTestingAssertFrames,
					ignoreJKLoggingFrames,
					False,
				)

		return ExceptionObject(exception, type(exception).__name__, exceptionTextHR, stackTrace, nestedException)
	#

#












