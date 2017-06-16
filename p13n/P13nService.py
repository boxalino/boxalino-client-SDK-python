#
# Autogenerated by Thrift Compiler (0.10.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
import sys
import logging
from .ttypes import *
from thrift.Thrift import TProcessor
from thrift.transport import TTransport


class Iface(object):
    def choose(self, choiceRequest):
        """
        <dl>
        <dt>@param choiceRequest</dt>
        <dd>the ChoiceRequest object containing your request</dd>

        <dt>@return</dt>
        <dd>a ChoiceResponse object containing the list of variants</dd>

        <dt>@throws P13nServiceException</dt>
        <dd>an exception containing an error message</dd>
        </dl>

        Parameters:
         - choiceRequest
        """
        pass

    def batchChoose(self, batchChoiceRequest):
        """
        <dl>
        <dt>@param batchChoiceRequest</dt>
        <dd>the BatchChoiceRequest object containing your requests</dd>

        <dt>@return</dt>
        <dd>a BatchChoiceResponse object containing the list of variants for each request</dd>

        <dt>@throws P13nServiceException</dt>
        <dd>an exception containing an error message</dd>
        </dl>

        Parameters:
         - batchChoiceRequest
        """
        pass

    def autocomplete(self, request):
        """
        <dl>
        <dt>@param request</dt>
        <dd>the AutocompleteRequest object containing your request</dd>

        <dt>@return</dt>
        <dd>a AutocompleteResponse object containing the list of hits</dd>

        <dt>@throws P13nServiceException</dt>
        <dd>an exception containing an error message</dd>
        </dl>

        Parameters:
         - request
        """
        pass

    def autocompleteAll(self, bundle):
        """
        Parameters:
         - bundle
        """
        pass

    def updateChoice(self, choiceUpdateRequest):
        """
        Updating a choice or creating a new choice if choiceId is not given in choiceUpdateRequest.

        Parameters:
         - choiceUpdateRequest
        """
        pass


class Client(Iface):
    def __init__(self, iprot, oprot=None):
        self._iprot = self._oprot = iprot
        if oprot is not None:
            self._oprot = oprot
        self._seqid = 0

    def choose(self, choiceRequest):
        """
        <dl>
        <dt>@param choiceRequest</dt>
        <dd>the ChoiceRequest object containing your request</dd>

        <dt>@return</dt>
        <dd>a ChoiceResponse object containing the list of variants</dd>

        <dt>@throws P13nServiceException</dt>
        <dd>an exception containing an error message</dd>
        </dl>

        Parameters:
         - choiceRequest
        """
        self.send_choose(choiceRequest)
        return self.recv_choose()

    def send_choose(self, choiceRequest):
        self._oprot.writeMessageBegin('choose', TMessageType.CALL, self._seqid)
        args = choose_args()
        args.choiceRequest = choiceRequest
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_choose(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = choose_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.p13nServiceException is not None:
            raise result.p13nServiceException
        raise TApplicationException(TApplicationException.MISSING_RESULT, "choose failed: unknown result")

    def batchChoose(self, batchChoiceRequest):
        """
        <dl>
        <dt>@param batchChoiceRequest</dt>
        <dd>the BatchChoiceRequest object containing your requests</dd>

        <dt>@return</dt>
        <dd>a BatchChoiceResponse object containing the list of variants for each request</dd>

        <dt>@throws P13nServiceException</dt>
        <dd>an exception containing an error message</dd>
        </dl>

        Parameters:
         - batchChoiceRequest
        """
        self.send_batchChoose(batchChoiceRequest)
        return self.recv_batchChoose()

    def send_batchChoose(self, batchChoiceRequest):
        self._oprot.writeMessageBegin('batchChoose', TMessageType.CALL, self._seqid)
        args = batchChoose_args()
        args.batchChoiceRequest = batchChoiceRequest
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_batchChoose(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = batchChoose_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.p13nServiceException is not None:
            raise result.p13nServiceException
        raise TApplicationException(TApplicationException.MISSING_RESULT, "batchChoose failed: unknown result")

    def autocomplete(self, request):
        """
        <dl>
        <dt>@param request</dt>
        <dd>the AutocompleteRequest object containing your request</dd>

        <dt>@return</dt>
        <dd>a AutocompleteResponse object containing the list of hits</dd>

        <dt>@throws P13nServiceException</dt>
        <dd>an exception containing an error message</dd>
        </dl>

        Parameters:
         - request
        """
        self.send_autocomplete(request)
        return self.recv_autocomplete()

    def send_autocomplete(self, request):
        self._oprot.writeMessageBegin('autocomplete', TMessageType.CALL, self._seqid)
        args = autocomplete_args()
        args.request = request
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_autocomplete(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = autocomplete_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.p13nServiceException is not None:
            raise result.p13nServiceException
        raise TApplicationException(TApplicationException.MISSING_RESULT, "autocomplete failed: unknown result")

    def autocompleteAll(self, bundle):
        """
        Parameters:
         - bundle
        """
        self.send_autocompleteAll(bundle)
        return self.recv_autocompleteAll()

    def send_autocompleteAll(self, bundle):
        self._oprot.writeMessageBegin('autocompleteAll', TMessageType.CALL, self._seqid)
        args = autocompleteAll_args()
        args.bundle = bundle
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_autocompleteAll(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = autocompleteAll_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.p13nServiceException is not None:
            raise result.p13nServiceException
        raise TApplicationException(TApplicationException.MISSING_RESULT, "autocompleteAll failed: unknown result")

    def updateChoice(self, choiceUpdateRequest):
        """
        Updating a choice or creating a new choice if choiceId is not given in choiceUpdateRequest.

        Parameters:
         - choiceUpdateRequest
        """
        self.send_updateChoice(choiceUpdateRequest)
        return self.recv_updateChoice()

    def send_updateChoice(self, choiceUpdateRequest):
        self._oprot.writeMessageBegin('updateChoice', TMessageType.CALL, self._seqid)
        args = updateChoice_args()
        args.choiceUpdateRequest = choiceUpdateRequest
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_updateChoice(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = updateChoice_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.p13nServiceException is not None:
            raise result.p13nServiceException
        raise TApplicationException(TApplicationException.MISSING_RESULT, "updateChoice failed: unknown result")


class Processor(Iface, TProcessor):
    def __init__(self, handler):
        self._handler = handler
        self._processMap = {}
        self._processMap["choose"] = Processor.process_choose
        self._processMap["batchChoose"] = Processor.process_batchChoose
        self._processMap["autocomplete"] = Processor.process_autocomplete
        self._processMap["autocompleteAll"] = Processor.process_autocompleteAll
        self._processMap["updateChoice"] = Processor.process_updateChoice

    def process(self, iprot, oprot):
        (name, type, seqid) = iprot.readMessageBegin()
        if name not in self._processMap:
            iprot.skip(TType.STRUCT)
            iprot.readMessageEnd()
            x = TApplicationException(TApplicationException.UNKNOWN_METHOD, 'Unknown function %s' % (name))
            oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
            x.write(oprot)
            oprot.writeMessageEnd()
            oprot.trans.flush()
            return
        else:
            self._processMap[name](self, seqid, iprot, oprot)
        return True

    def process_choose(self, seqid, iprot, oprot):
        args = choose_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = choose_result()
        try:
            result.success = self._handler.choose(args.choiceRequest)
            msg_type = TMessageType.REPLY
        except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
            raise
        except P13nServiceException as p13nServiceException:
            msg_type = TMessageType.REPLY
            result.p13nServiceException = p13nServiceException
        except Exception as ex:
            msg_type = TMessageType.EXCEPTION
            logging.exception(ex)
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')
        oprot.writeMessageBegin("choose", msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_batchChoose(self, seqid, iprot, oprot):
        args = batchChoose_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = batchChoose_result()
        try:
            result.success = self._handler.batchChoose(args.batchChoiceRequest)
            msg_type = TMessageType.REPLY
        except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
            raise
        except P13nServiceException as p13nServiceException:
            msg_type = TMessageType.REPLY
            result.p13nServiceException = p13nServiceException
        except Exception as ex:
            msg_type = TMessageType.EXCEPTION
            logging.exception(ex)
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')
        oprot.writeMessageBegin("batchChoose", msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_autocomplete(self, seqid, iprot, oprot):
        args = autocomplete_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = autocomplete_result()
        try:
            result.success = self._handler.autocomplete(args.request)
            msg_type = TMessageType.REPLY
        except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
            raise
        except P13nServiceException as p13nServiceException:
            msg_type = TMessageType.REPLY
            result.p13nServiceException = p13nServiceException
        except Exception as ex:
            msg_type = TMessageType.EXCEPTION
            logging.exception(ex)
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')
        oprot.writeMessageBegin("autocomplete", msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_autocompleteAll(self, seqid, iprot, oprot):
        args = autocompleteAll_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = autocompleteAll_result()
        try:
            result.success = self._handler.autocompleteAll(args.bundle)
            msg_type = TMessageType.REPLY
        except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
            raise
        except P13nServiceException as p13nServiceException:
            msg_type = TMessageType.REPLY
            result.p13nServiceException = p13nServiceException
        except Exception as ex:
            msg_type = TMessageType.EXCEPTION
            logging.exception(ex)
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')
        oprot.writeMessageBegin("autocompleteAll", msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_updateChoice(self, seqid, iprot, oprot):
        args = updateChoice_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = updateChoice_result()
        try:
            result.success = self._handler.updateChoice(args.choiceUpdateRequest)
            msg_type = TMessageType.REPLY
        except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
            raise
        except P13nServiceException as p13nServiceException:
            msg_type = TMessageType.REPLY
            result.p13nServiceException = p13nServiceException
        except Exception as ex:
            msg_type = TMessageType.EXCEPTION
            logging.exception(ex)
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')
        oprot.writeMessageBegin("updateChoice", msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

# HELPER FUNCTIONS AND STRUCTURES


class choose_args(object):
    """
    Attributes:
     - choiceRequest
    """

    thrift_spec = None

    def __init__(self, choiceRequest=None,):
        self.choiceRequest = choiceRequest

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == -1:
                if ftype == TType.STRUCT:
                    self.choiceRequest = ChoiceRequest()
                    self.choiceRequest.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('choose_args')
        if self.choiceRequest is not None:
            oprot.writeFieldBegin('choiceRequest', TType.STRUCT, -1)
            self.choiceRequest.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class choose_result(object):
    """
    Attributes:
     - success
     - p13nServiceException
    """

    thrift_spec = (
        (0, TType.STRUCT, 'success', (ChoiceResponse, ChoiceResponse.thrift_spec), None, ),  # 0
        (1, TType.STRUCT, 'p13nServiceException', (P13nServiceException, P13nServiceException.thrift_spec), None, ),  # 1
    )

    def __init__(self, success=None, p13nServiceException=None,):
        self.success = success
        self.p13nServiceException = p13nServiceException

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.STRUCT:
                    self.success = ChoiceResponse()
                    self.success.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.p13nServiceException = P13nServiceException()
                    self.p13nServiceException.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('choose_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRUCT, 0)
            self.success.write(oprot)
            oprot.writeFieldEnd()
        if self.p13nServiceException is not None:
            oprot.writeFieldBegin('p13nServiceException', TType.STRUCT, 1)
            self.p13nServiceException.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class batchChoose_args(object):
    """
    Attributes:
     - batchChoiceRequest
    """

    thrift_spec = None

    def __init__(self, batchChoiceRequest=None,):
        self.batchChoiceRequest = batchChoiceRequest

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == -1:
                if ftype == TType.STRUCT:
                    self.batchChoiceRequest = BatchChoiceRequest()
                    self.batchChoiceRequest.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('batchChoose_args')
        if self.batchChoiceRequest is not None:
            oprot.writeFieldBegin('batchChoiceRequest', TType.STRUCT, -1)
            self.batchChoiceRequest.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class batchChoose_result(object):
    """
    Attributes:
     - success
     - p13nServiceException
    """

    thrift_spec = (
        (0, TType.STRUCT, 'success', (BatchChoiceResponse, BatchChoiceResponse.thrift_spec), None, ),  # 0
        (1, TType.STRUCT, 'p13nServiceException', (P13nServiceException, P13nServiceException.thrift_spec), None, ),  # 1
    )

    def __init__(self, success=None, p13nServiceException=None,):
        self.success = success
        self.p13nServiceException = p13nServiceException

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.STRUCT:
                    self.success = BatchChoiceResponse()
                    self.success.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.p13nServiceException = P13nServiceException()
                    self.p13nServiceException.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('batchChoose_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRUCT, 0)
            self.success.write(oprot)
            oprot.writeFieldEnd()
        if self.p13nServiceException is not None:
            oprot.writeFieldBegin('p13nServiceException', TType.STRUCT, 1)
            self.p13nServiceException.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class autocomplete_args(object):
    """
    Attributes:
     - request
    """

    thrift_spec = None

    def __init__(self, request=None,):
        self.request = request

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == -1:
                if ftype == TType.STRUCT:
                    self.request = AutocompleteRequest()
                    self.request.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('autocomplete_args')
        if self.request is not None:
            oprot.writeFieldBegin('request', TType.STRUCT, -1)
            self.request.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class autocomplete_result(object):
    """
    Attributes:
     - success
     - p13nServiceException
    """

    thrift_spec = (
        (0, TType.STRUCT, 'success', (AutocompleteResponse, AutocompleteResponse.thrift_spec), None, ),  # 0
        (1, TType.STRUCT, 'p13nServiceException', (P13nServiceException, P13nServiceException.thrift_spec), None, ),  # 1
    )

    def __init__(self, success=None, p13nServiceException=None,):
        self.success = success
        self.p13nServiceException = p13nServiceException

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.STRUCT:
                    self.success = AutocompleteResponse()
                    self.success.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.p13nServiceException = P13nServiceException()
                    self.p13nServiceException.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('autocomplete_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRUCT, 0)
            self.success.write(oprot)
            oprot.writeFieldEnd()
        if self.p13nServiceException is not None:
            oprot.writeFieldBegin('p13nServiceException', TType.STRUCT, 1)
            self.p13nServiceException.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class autocompleteAll_args(object):
    """
    Attributes:
     - bundle
    """

    thrift_spec = None

    def __init__(self, bundle=None,):
        self.bundle = bundle

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == -1:
                if ftype == TType.STRUCT:
                    self.bundle = AutocompleteRequestBundle()
                    self.bundle.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('autocompleteAll_args')
        if self.bundle is not None:
            oprot.writeFieldBegin('bundle', TType.STRUCT, -1)
            self.bundle.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class autocompleteAll_result(object):
    """
    Attributes:
     - success
     - p13nServiceException
    """

    thrift_spec = (
        (0, TType.STRUCT, 'success', (AutocompleteResponseBundle, AutocompleteResponseBundle.thrift_spec), None, ),  # 0
        (1, TType.STRUCT, 'p13nServiceException', (P13nServiceException, P13nServiceException.thrift_spec), None, ),  # 1
    )

    def __init__(self, success=None, p13nServiceException=None,):
        self.success = success
        self.p13nServiceException = p13nServiceException

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.STRUCT:
                    self.success = AutocompleteResponseBundle()
                    self.success.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.p13nServiceException = P13nServiceException()
                    self.p13nServiceException.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('autocompleteAll_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRUCT, 0)
            self.success.write(oprot)
            oprot.writeFieldEnd()
        if self.p13nServiceException is not None:
            oprot.writeFieldBegin('p13nServiceException', TType.STRUCT, 1)
            self.p13nServiceException.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class updateChoice_args(object):
    """
    Attributes:
     - choiceUpdateRequest
    """

    thrift_spec = None

    def __init__(self, choiceUpdateRequest=None,):
        self.choiceUpdateRequest = choiceUpdateRequest

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == -1:
                if ftype == TType.STRUCT:
                    self.choiceUpdateRequest = ChoiceUpdateRequest()
                    self.choiceUpdateRequest.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('updateChoice_args')
        if self.choiceUpdateRequest is not None:
            oprot.writeFieldBegin('choiceUpdateRequest', TType.STRUCT, -1)
            self.choiceUpdateRequest.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class updateChoice_result(object):
    """
    Attributes:
     - success
     - p13nServiceException
    """

    thrift_spec = (
        (0, TType.STRUCT, 'success', (ChoiceUpdateResponse, ChoiceUpdateResponse.thrift_spec), None, ),  # 0
        (1, TType.STRUCT, 'p13nServiceException', (P13nServiceException, P13nServiceException.thrift_spec), None, ),  # 1
    )

    def __init__(self, success=None, p13nServiceException=None,):
        self.success = success
        self.p13nServiceException = p13nServiceException

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.STRUCT:
                    self.success = ChoiceUpdateResponse()
                    self.success.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.p13nServiceException = P13nServiceException()
                    self.p13nServiceException.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('updateChoice_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRUCT, 0)
            self.success.write(oprot)
            oprot.writeFieldEnd()
        if self.p13nServiceException is not None:
            oprot.writeFieldBegin('p13nServiceException', TType.STRUCT, 1)
            self.p13nServiceException.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)