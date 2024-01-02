# Generated from ../flash_patcher/antlr_source/PatchfileParser.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,15,59,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,1,0,1,
        0,1,0,1,0,1,1,4,1,18,8,1,11,1,12,1,19,1,1,1,1,1,1,1,1,1,2,4,2,27,
        8,2,11,2,12,2,28,1,3,1,3,1,3,1,3,1,3,1,3,1,4,1,4,5,4,39,8,4,10,4,
        12,4,42,9,4,1,5,3,5,45,8,5,1,5,1,5,1,5,3,5,50,8,5,1,5,3,5,53,8,5,
        1,5,1,5,3,5,57,8,5,1,5,0,0,6,0,2,4,6,8,10,0,0,61,0,12,1,0,0,0,2,
        17,1,0,0,0,4,26,1,0,0,0,6,30,1,0,0,0,8,40,1,0,0,0,10,56,1,0,0,0,
        12,13,5,1,0,0,13,14,5,3,0,0,14,15,3,10,5,0,15,1,1,0,0,0,16,18,3,
        0,0,0,17,16,1,0,0,0,18,19,1,0,0,0,19,17,1,0,0,0,19,20,1,0,0,0,20,
        21,1,0,0,0,21,22,5,4,0,0,22,23,3,4,2,0,23,24,5,14,0,0,24,3,1,0,0,
        0,25,27,5,15,0,0,26,25,1,0,0,0,27,28,1,0,0,0,28,26,1,0,0,0,28,29,
        1,0,0,0,29,5,1,0,0,0,30,31,5,2,0,0,31,32,5,3,0,0,32,33,3,10,5,0,
        33,34,5,10,0,0,34,35,3,10,5,0,35,7,1,0,0,0,36,39,3,2,1,0,37,39,3,
        6,3,0,38,36,1,0,0,0,38,37,1,0,0,0,39,42,1,0,0,0,40,38,1,0,0,0,40,
        41,1,0,0,0,41,9,1,0,0,0,42,40,1,0,0,0,43,45,5,7,0,0,44,43,1,0,0,
        0,44,45,1,0,0,0,45,46,1,0,0,0,46,47,5,5,0,0,47,49,5,11,0,0,48,50,
        5,9,0,0,49,48,1,0,0,0,49,50,1,0,0,0,50,52,1,0,0,0,51,53,5,8,0,0,
        52,51,1,0,0,0,52,53,1,0,0,0,53,57,1,0,0,0,54,57,5,9,0,0,55,57,5,
        6,0,0,56,44,1,0,0,0,56,54,1,0,0,0,56,55,1,0,0,0,57,11,1,0,0,0,8,
        19,28,38,40,44,49,52,56
    ]

class PatchfileParser ( Parser ):

    grammarFileName = "PatchfileParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "'('", "')'", 
                     "<INVALID>", "'-'" ]

    symbolicNames = [ "<INVALID>", "ADD", "REMOVE", "FILENAME", "BEGIN_PATCH", 
                      "FUNCTION", "END", "OPEN_BLOCK", "CLOSE_BLOCK", "INTEGER", 
                      "DASH", "FUNCTION_NAME", "WHITESPACE", "COMMENT", 
                      "END_PATCH", "AS_TEXT" ]

    RULE_addBlockHeader = 0
    RULE_addBlock = 1
    RULE_addBlockText = 2
    RULE_removeBlock = 3
    RULE_root = 4
    RULE_locationToken = 5

    ruleNames =  [ "addBlockHeader", "addBlock", "addBlockText", "removeBlock", 
                   "root", "locationToken" ]

    EOF = Token.EOF
    ADD=1
    REMOVE=2
    FILENAME=3
    BEGIN_PATCH=4
    FUNCTION=5
    END=6
    OPEN_BLOCK=7
    CLOSE_BLOCK=8
    INTEGER=9
    DASH=10
    FUNCTION_NAME=11
    WHITESPACE=12
    COMMENT=13
    END_PATCH=14
    AS_TEXT=15

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class AddBlockHeaderContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ADD(self):
            return self.getToken(PatchfileParser.ADD, 0)

        def FILENAME(self):
            return self.getToken(PatchfileParser.FILENAME, 0)

        def locationToken(self):
            return self.getTypedRuleContext(PatchfileParser.LocationTokenContext,0)


        def getRuleIndex(self):
            return PatchfileParser.RULE_addBlockHeader

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddBlockHeader" ):
                listener.enterAddBlockHeader(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddBlockHeader" ):
                listener.exitAddBlockHeader(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddBlockHeader" ):
                return visitor.visitAddBlockHeader(self)
            else:
                return visitor.visitChildren(self)




    def addBlockHeader(self):

        localctx = PatchfileParser.AddBlockHeaderContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_addBlockHeader)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 12
            self.match(PatchfileParser.ADD)
            self.state = 13
            self.match(PatchfileParser.FILENAME)
            self.state = 14
            self.locationToken()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AddBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BEGIN_PATCH(self):
            return self.getToken(PatchfileParser.BEGIN_PATCH, 0)

        def addBlockText(self):
            return self.getTypedRuleContext(PatchfileParser.AddBlockTextContext,0)


        def END_PATCH(self):
            return self.getToken(PatchfileParser.END_PATCH, 0)

        def addBlockHeader(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.AddBlockHeaderContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.AddBlockHeaderContext,i)


        def getRuleIndex(self):
            return PatchfileParser.RULE_addBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddBlock" ):
                listener.enterAddBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddBlock" ):
                listener.exitAddBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddBlock" ):
                return visitor.visitAddBlock(self)
            else:
                return visitor.visitChildren(self)




    def addBlock(self):

        localctx = PatchfileParser.AddBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_addBlock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 17 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 16
                self.addBlockHeader()
                self.state = 19 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==1):
                    break

            self.state = 21
            self.match(PatchfileParser.BEGIN_PATCH)
            self.state = 22
            self.addBlockText()
            self.state = 23
            self.match(PatchfileParser.END_PATCH)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AddBlockTextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AS_TEXT(self, i:int=None):
            if i is None:
                return self.getTokens(PatchfileParser.AS_TEXT)
            else:
                return self.getToken(PatchfileParser.AS_TEXT, i)

        def getRuleIndex(self):
            return PatchfileParser.RULE_addBlockText

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddBlockText" ):
                listener.enterAddBlockText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddBlockText" ):
                listener.exitAddBlockText(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddBlockText" ):
                return visitor.visitAddBlockText(self)
            else:
                return visitor.visitChildren(self)




    def addBlockText(self):

        localctx = PatchfileParser.AddBlockTextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_addBlockText)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 26 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 25
                self.match(PatchfileParser.AS_TEXT)
                self.state = 28 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==15):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RemoveBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def REMOVE(self):
            return self.getToken(PatchfileParser.REMOVE, 0)

        def FILENAME(self):
            return self.getToken(PatchfileParser.FILENAME, 0)

        def locationToken(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.LocationTokenContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.LocationTokenContext,i)


        def DASH(self):
            return self.getToken(PatchfileParser.DASH, 0)

        def getRuleIndex(self):
            return PatchfileParser.RULE_removeBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRemoveBlock" ):
                listener.enterRemoveBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRemoveBlock" ):
                listener.exitRemoveBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRemoveBlock" ):
                return visitor.visitRemoveBlock(self)
            else:
                return visitor.visitChildren(self)




    def removeBlock(self):

        localctx = PatchfileParser.RemoveBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_removeBlock)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 30
            self.match(PatchfileParser.REMOVE)
            self.state = 31
            self.match(PatchfileParser.FILENAME)
            self.state = 32
            self.locationToken()
            self.state = 33
            self.match(PatchfileParser.DASH)
            self.state = 34
            self.locationToken()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RootContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def addBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.AddBlockContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.AddBlockContext,i)


        def removeBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.RemoveBlockContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.RemoveBlockContext,i)


        def getRuleIndex(self):
            return PatchfileParser.RULE_root

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRoot" ):
                listener.enterRoot(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRoot" ):
                listener.exitRoot(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRoot" ):
                return visitor.visitRoot(self)
            else:
                return visitor.visitChildren(self)




    def root(self):

        localctx = PatchfileParser.RootContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_root)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 40
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1 or _la==2:
                self.state = 38
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [1]:
                    self.state = 36
                    self.addBlock()
                    pass
                elif token in [2]:
                    self.state = 37
                    self.removeBlock()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 42
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LocationTokenContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return PatchfileParser.RULE_locationToken

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class FunctionContext(LocationTokenContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PatchfileParser.LocationTokenContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def FUNCTION(self):
            return self.getToken(PatchfileParser.FUNCTION, 0)
        def FUNCTION_NAME(self):
            return self.getToken(PatchfileParser.FUNCTION_NAME, 0)
        def OPEN_BLOCK(self):
            return self.getToken(PatchfileParser.OPEN_BLOCK, 0)
        def INTEGER(self):
            return self.getToken(PatchfileParser.INTEGER, 0)
        def CLOSE_BLOCK(self):
            return self.getToken(PatchfileParser.CLOSE_BLOCK, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunction" ):
                listener.enterFunction(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunction" ):
                listener.exitFunction(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunction" ):
                return visitor.visitFunction(self)
            else:
                return visitor.visitChildren(self)


    class EndContext(LocationTokenContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PatchfileParser.LocationTokenContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def END(self):
            return self.getToken(PatchfileParser.END, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEnd" ):
                listener.enterEnd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEnd" ):
                listener.exitEnd(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEnd" ):
                return visitor.visitEnd(self)
            else:
                return visitor.visitChildren(self)


    class LineNumberContext(LocationTokenContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PatchfileParser.LocationTokenContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def INTEGER(self):
            return self.getToken(PatchfileParser.INTEGER, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLineNumber" ):
                listener.enterLineNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLineNumber" ):
                listener.exitLineNumber(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLineNumber" ):
                return visitor.visitLineNumber(self)
            else:
                return visitor.visitChildren(self)



    def locationToken(self):

        localctx = PatchfileParser.LocationTokenContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_locationToken)
        self._la = 0 # Token type
        try:
            self.state = 56
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [5, 7]:
                localctx = PatchfileParser.FunctionContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 44
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==7:
                    self.state = 43
                    self.match(PatchfileParser.OPEN_BLOCK)


                self.state = 46
                self.match(PatchfileParser.FUNCTION)
                self.state = 47
                self.match(PatchfileParser.FUNCTION_NAME)
                self.state = 49
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==9:
                    self.state = 48
                    self.match(PatchfileParser.INTEGER)


                self.state = 52
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==8:
                    self.state = 51
                    self.match(PatchfileParser.CLOSE_BLOCK)


                pass
            elif token in [9]:
                localctx = PatchfileParser.LineNumberContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 54
                self.match(PatchfileParser.INTEGER)
                pass
            elif token in [6]:
                localctx = PatchfileParser.EndContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 55
                self.match(PatchfileParser.END)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





