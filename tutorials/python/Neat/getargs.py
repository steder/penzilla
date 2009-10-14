#!/usr/bin/env python
#----------------------------------------------------------------------------
# getargs.py:       (Yet Another getopt) Parse command line arguments
#
# See __doc__ string below.
#
# Requires:
#    - Python 1.5.2 or newer (www.python.org)
#    - OS: portable
#
# $Id: //depot/rgutils/rgutils/getargs.py#1 $
#----------------------------------------------------------------------------
'''
Command line arguments parser.

Synopsis
========
    C{r = parseArgs(args, options)}
Where
=====
    - args is a sequence of command line arguments, typically sys.argv[1:]
    - options is a string specifying the acceptable options (see below).

Options
=======
  Syntax for the options::
    options : 0 a N options separated by one or more of comma ',',
              semicolon ';' or "blank" character. Leading & trailing spaces
              allowed.
    option  : shortOpt['|'longOpt]['!'][optValueCnt]
    shortOpt: letter
    longOpt : at least 2 letters alphaNum or '-' or '_' or '.'. Must not
              begin with a '-'. A long option *MUST* have a corresponding
              short option.
    '!'       If present indicates that the option is required (optional by
              default)

    optValueCnt: (Option values multiplicity) One of '-?=*+' :

       Letter:    min:   max:     Comment:
       ------------------------------------------------------------
         -         0      0       No param/value expected (default)
         ?         0      1       Optional 1 param
         =         1      1       Required 1 param
         *         0      N       Optional, unbounded nb of params
         +         1      N       Required, unbounded nb of params

  Multiplicity >1 means that the option may appear more than once
  (e.g. "-a v1 -b -a v2"), and the values will be collected in a
  sequence. It is still legal but meaningless if option has no args.

  Short options may be concatenated as far as there is no ambiguity, e.g.
  -ab is equivalent to -a -b. Last option can take values, e.g.
  -abc v1 is equivalent to -a -b -c v1.

  Bonus: '?' if encountered is translated to '-h'.

Return
======
    If no error occurs, the result r is a tuple (optDict, nonOpts) where:
      - optDict -- dictionary {shortOption: values,...}
          - if option max values cnt is 1, values is a single value or None
          - if option max values cnt is >1, values is a list of values
            (possibly empty).
      - nonOpts -- list of everything else than options.
Examples
========
    Option specs
    ------------
      Some examples of option specifications::
        "a"         short option -a, optional, no value.
        "a!         short option -a, required, no value.
        "a?         short option -a, optional, one optional value.
        "d|dir="    short option -d <=> long opt --dir, optional,
                    exactly one required value.
        "f|file!*   short option -f <=> long option --file, required,
                    0 to many values.
        "f+"        short option -f, optional, 1 to many values.

        "a!; d|dir=  ; f+" Specification for the 3 options -a, -d, -f
        " a!,d|dir=, f+ "  Same. Spaces, ';' or ',' are valid separators.
                           Leading & trailing spaces allowed.

    Typical usage
    -------------
      Here is a sample of typical code::

        import getargs
        # (default for 2e param (args to parse) is sys.argv[1:])
        optDict, others = getargs.parseArgs("a!*, d|dir=, f?, g, e+")

        aValues = optDict['-a']     # list, possibly empty
        if optDict.has_key('-d'):   # opt -d is optional
            dir = optDict['-d']     # one single value, required
        fValue = optDict.get('-f', aSingleDefaultValue)
        eValues = optDict.get('-e', aDefaultValueList)
        gOccured = optDict.kas_key('-g')


    See also
    --------
        L{test()} for other examples of use.

To do
=====
    Could add stuff like default values, value typing, but I want to keep
    the interface simple!

Competitors
===========
    - getopt.py   -- included in std distrib of Python. Basic 
               functionality: no required args, mapping from long to
               short opts, etc..
    - optik   -- by Greg Ward (U{http://optik.sourceforge.net/}).
                 Will supersede getopt in Python 2.3.
    - getargs.py  -- by Ivan Van Laningham (ivanlan@callware.com.),
               available at U{ftp://www.pauahtun.org/pub/getargspy.zip}.
               Quite complete but less concise and simple to use.
'''
__version__ = '1.8.' + '$Revision: #1 $'[12:-2]
__author__ = 'Richard Gruet', 'rjgruet@yahoo.com'
__date__    = '$Date: 2003/05/23 $'[7:-2], '$Author: rgruet $'[9:-2]
__since__ = '2001-07-15'
__doc__ += '\n@author: %s (U{%s})\n@version: %s' % (__author__[0],
                                            __author__[1], __version__)
__all__ = ['Error', 'GetArgsError', 'OptError', 'ArgError', 'TestError',
           'parseArgs', 'CmdLineArgParser']

import sys, string, re, types

true, false = 1, 0

# Exception raised by this module.
class Error(Exception):
    ''' Base exception.'''
    pass

GetArgsError = Error # ->Use this name, Error is kept for compatibility.
    
class OptError(GetArgsError):
    ''' Bad option specification.'''
    pass

class ArgError(GetArgsError):
    ''' Arg doesn't match option spec.'''
    pass
    
class TestError(GetArgsError):
    pass

#----------------------------------------------------------------------------
def parseArgs(options, args=sys.argv[1:]):
#----------------------------------------------------------------------------
    ''' Helper function to parse cmd line args in one call.
    
        @param options: Specification of options (see module __doc__)
        @param args: The sequence of cmd line argumentsto parse.
        @return: (optDict, nonOpts) where:
            - optDict: dictionary {shortOption: [Parameter/value list],...}
            - nonOpts: list of everything else than options.
    '''
    return CmdLineArgParser(options).parseArgs(args)

#----------------------------------------------------------------------------
class CmdLineArgParser:
#----------------------------------------------------------------------------
    ''' Parses command line args according to options specification.
    '''
    # Regular expression matching the specification for ONE option:
    OPTION_SPEC_REGEXP = (r'\s*(?P<shortOpt>[A-Za-z])'
                           '(\|(?P<longOpt>[^\-][\w\-_\.]+?))?'
                           '(?P<required>!)?'
                           '(?P<optValueCnt>[-=?+*])?\s*'
                           '$')
    RE_OPTION_SPEC = re.compile(OPTION_SPEC_REGEXP)
    
    # Regular expression matching (loosely) an option in the cmd line:
    RE_OPTION = re.compile(r'-{1,2}[^-]+')

    # Option values multiplicity:
    N = sys.maxint  # unbounded
        # Maps symbol to value multiplicity (min, max):
    VALUE_CNT = {'-':(0, 0), '?':(0, 1), '=':(1, 1), '+':(1, N), '*':(0, N)}
    

    def __init__(self, options):
        ''' Parses option specification.
        '''
        self.optSpecs = {}      # { shortOpt: (required, (minValues,
                                #              maxValues)), ...}
                                # shortOpt includes leading '-'.
        self.long2short = {}    # Maps long opt to short {longOpt: shortOpt,...}
        self.options = options  # original string spec
        
        for optSpec in re.split("[;,\s]+", string.strip(options)):
        
            m = self.RE_OPTION_SPEC.match(optSpec)
        
            if m is None or m.group('shortOpt') is None:
                raise OptError('Invalid option specification "%s": legal '
                      'pattern is "%s".' % (optSpec, self.OPTION_SPEC_REGEXP))
            
            shortOpt, longOpt, required, optValueCnt = (m.group('shortOpt'),
                m.group('longOpt'), m.group('required'), m.group('optValueCnt'))
                                
            required = (required is not None)
            if required is None:
                required = false        # default= optional
            
            # Value multiplicity:
            if optValueCnt is None:
                optValueCnt = '-'
            pm = self.VALUE_CNT[optValueCnt] 
            
            # Store opt info:
            shortOpt = '-' + shortOpt
            if self.optSpecs.has_key(shortOpt):
                raise OptError("Duplicate short option '%s'." % shortOpt)
            self.optSpecs[shortOpt] = (required, pm)
            
            # Map long option to short:
            if longOpt is not None:
                longOpt = '--' + longOpt
                self.long2short[longOpt] = shortOpt
        
    def __repr__(self):
        return "<CmdLineArgParser options='%s'>" % self.options
    
    def parseArgs(self, args):
        ''' Parses the given sequence of cmd line args according to spec
            given at construction time.
        
            @return: (optDict, nonOpts) where:
              - optDict: dictionary {shortOption: List of values (may be
                empty),...}
              - nonOpts: list of everything else than options.
        '''
        if type(args) not in (types.ListType, types.TupleType):
            raise ArgError('<args> must be a sequence.')
        
        optDict = {}
        nonOpts = []
        optionExpectingValue = None
        valueRequired = false       # Whether value is required or optional
        
        # First pass to "explode" contracted forms like '-abc' <=> '-a -b -c';
        # also map ? to -h (bonus feature!):
        expandedArgs = []
        for arg in args:
            if arg == '?':
                expandedArgs.append('-h')
            elif len(arg) > 2 and arg[0]=='-' and arg[1]!='-':
                expandedArgs.extend(map(lambda x: '-'+x, 
                                    filter(lambda x: x in string.letters,
                                    list(arg[1:]))))
            else:
                expandedArgs.append(arg)
            
        # Now analyse the sequence of tokens in expandedArgs:
        # First, create a dictionary of all options with their values
        # without checking min and max (concatenate values for same option).
        curOpt = None
        for token in expandedArgs:

            if self.RE_OPTION.match(token): # Option

                try:
                    curOpt = shortOpt = self._shortOptionOf(token)
                    self.optSpecs[shortOpt]
                except KeyError:
                    raise ArgError("Invalid option %s" % token)

                if not optDict.has_key(shortOpt):
                    optDict[shortOpt] = []
                    
            else: # token is a value:
                if curOpt is not None:
                    values = optDict[curOpt]
                    values.append(token)
                else:
                    nonOpts.append(token)
        
        # At this point, optDict contains the options with their values, without
        # checking value multiplicity.
        # nonOpts contains only the values not assigned to an option.
        
        requiredOpts = {}   # Compute dict of required options
        for opt, spec in self.optSpecs.items():
            if spec[0]:
                requiredOpts[opt] = None
        
        # Check min and max values for each option. All values exceeding max 
        # are put in nonOpts list. Error if value count < min.
        
        for opt, values in optDict.items():

            required, (min, max) = self.optSpecs[opt]
            if required:
                del requiredOpts[opt]
            
            l = len(values)
            if l < min:
                raise ArgError("Not enough values for option '%s' "
                    "(expected at least %d, got only %d)" % (opt, min, l))
            if l > max:
                nonOpts.extend(values[max:])
                values = values[:max]
            
            # Convert value list to a single element (or None) if max <= 1:
            
            if max == 0: values = None
            elif max == 1:
                if values: values = values[0]
                else: values = None
            # (else max>1, keep values list as is)
            optDict[opt] = values 
            
        # Finally, check that all required options occured at least once:
        if requiredOpts:
            raise ArgError("Missing required option(s) %s." % string.join(
                                                    requiredOpts.keys(), ','))
        return optDict, nonOpts     
                    
                
    def _shortOptionOf(self, opt):
        '''Returns short option for opt if it is a long option,
           otherwise returns opt unchanged.
        '''
        if opt[:2] != '--':
            return opt
        return self.long2short[opt]
        

#----------------------------------------------------------------------------
def test():
#----------------------------------------------------------------------------
    ''' Unit test.
    '''
    def checkParseOptsOK(optSpec, expectedOptSpec, expectedLong2short={}):
        p = CmdLineArgParser(optSpec)
        if p.optSpecs !=  expectedOptSpec:
            raise TestError('expected %s, got %s (opts="%s")' %
                            (expectedOptSpec, p.optSpecs, optSpec))
        if p.long2short !=  expectedLong2short:
            raise TestError('expected %s, got %s (opts="%s")' %
                            (expectedLong2short, p.long2short, optSpec))
        return p
    
    def checkParseOptsFails(optSpec):
        try:
            CmdLineArgParser(optSpec)
        except Exception, e:
            if e.__class__ == OptError:
                return
        raise TestError('expected OptError not raised (optSpec="%s")' % optSpec)
                
    def checkParseArgsOK(parser, what, expectedResult):
        r = parser.parseArgs(string.split(what))
        if r !=  expectedResult:
            raise TestError('expected %s, got %s (args="%s", opts="%s")' %
                            (expectedResult, r, what, parser.options))
    
    def checkParseArgsFails(parser, what, expectedException):
        try:
            r = parser.parseArgs(string.split(what))
        except Exception, e:
            if e.__class__ == expectedException:
                return
        raise TestError('expected exception "%s" not raised '
            '(args="%s", opts="%s")' % (expectedException,what, parser.options))
    
    
    print 'Testing getargs.py...'
    
    N = CmdLineArgParser.N  # shortcut
    
    # Parse option specifications :
    checkParseOptsOK('a', {'-a': (0,(0,0))})
    checkParseOptsOK('  a ', {'-a': (0,(0,0))}) # leading/trailing spaces OK
    checkParseOptsFails('-a')   # '-' must be omitted.
    checkParseOptsFails('a b? a=')  # duplicate option a.
    checkParseOptsFails('ab|c') # short opt is more than 1 char
    checkParseOptsFails('|ab')  # short opt is required.
    checkParseOptsFails('a|-')  # long opt may not begin with a '-'
    checkParseOptsFails('a|b')  # long opt must be 2 chars min.
    checkParseOptsOK('a|bc-de', {'-a': (0,(0,0))}, {'--bc-de':'-a'})
    checkParseOptsOK('a!', {'-a': (1,(0,0))})
    checkParseOptsOK('a?', {'-a': (0,(0,1))})
    checkParseOptsOK('a!=', {'-a': (1,(1,1))})
    checkParseOptsOK('a*', {'-a': (0,(0,N))})
    checkParseOptsOK('a+', {'-a': (0,(1,N))})
    checkParseOptsOK('a|add-', {'-a': (0,(0,0))}, {'--add':'-a'})
    checkParseOptsOK('a|add!?', {'-a': (1,(0,1))}, {'--add':'-a'})
    checkParseOptsOK('a|add*', {'-a': (0,(0,N))}, {'--add':'-a'})
    checkParseOptsFails('#')    # short opt must be a letter
    checkParseOptsFails('1')    # short opt must be a letter
    checkParseOptsFails('a@')   # '@' is illegal
    checkParseOptsFails('a!@')  # '@' is illegal
    checkParseOptsFails('a|add!@') # '@' is illegal
    checkParseOptsFails('a|')   # long option missing
    o1 = ' a! ; b|blong?   ,c=; d|d-long* ; e+;f'
    r1,r2 = {'-a': (1,(0,0)), '-b': (0,(0,1)), '-c':(0,(1,1)), '-d': (0,(0,N)), '-e': (0,(1,N)), '-f': (0,(0,0))}, {'--blong': '-b', '--d-long': '-d'} 
    # Variants with different separators. Sometimes stupid, yet correct:
    checkParseOptsOK(' a! b|blong?    c=; d|d-long* e+ f', r1, r2)
    checkParseOptsOK(' a!, b|blong?, c=, d|d-long*, e+,f', r1, r2)
    checkParseOptsOK(' a!,;,b|blong?, c=,;,,,,   d|d-long*, e+,f ', r1, r2)
    
    # Parse args against opt. specifications :
    p = CmdLineArgParser(o1)
    checkParseArgsFails(p, '', ArgError)            # missing option '-a'
    checkParseArgsFails(p, 'hello world', ArgError) # missing option '-a'
    checkParseArgsOK(p, 'hello -a  world', ({'-a':None},['hello','world']))
    checkParseArgsOK(p, '-a hello -d  world', ({'-d':['world'], '-a':None},['hello']))
    
    o2 = ' a; b|blong?   ,c=; d|d-long* ; e+;f; h|help' # -a now optional
    p = CmdLineArgParser(o2)
    checkParseArgsOK(p, '?', ({'-h':None},[]))
    checkParseArgsOK(p, '-b', ({'-b':None},[]))
    checkParseArgsOK(p, '-b -b', ({'-b':None},[])) # Redundant but correct.
    checkParseArgsOK(p, '-ab', ({'-a':None, '-b':None},[]))
    checkParseArgsOK(p, '--blong', ({'-b':None},[]))
    checkParseArgsOK(p, 'hello -b', ({'-b':None},['hello']))
    checkParseArgsOK(p, '-b hello', ({'-b':'hello'},[]))
    checkParseArgsOK(p, '-b hello', ({'-b':'hello'},[]))
    checkParseArgsFails(p, '-c', ArgError)  # required arg for -c
    checkParseArgsOK(p, '-c hello world', ({'-c':'hello'},['world']))
    checkParseArgsOK(p, 'I say -c hello -d nice world', ({'-c':'hello', '-d':['nice', 'world']},['I', 'say']))
    
    checkParseArgsOK(p, '-d', ({'-d':[]},[]))
    checkParseArgsOK(p, '-d hello world', ({'-d':['hello', 'world']},[]))
    checkParseArgsOK(p, '-d hello -a -d nice world', ({'-a':None, '-d':['hello', 'nice', 'world']},[]))
    
    checkParseArgsFails(p, '-e', ArgError)  # required arg for -e
    checkParseArgsOK(p, 'hello -e world', ({'-e':['world']},['hello']))
    checkParseArgsOK(p, '-e hello nice -e world', ({'-e':['hello', 'nice','world']},[]))
    
    checkParseArgsOK(p, '-af', ({'-a':None, '-f':None},[]))
    checkParseArgsOK(p, '-afb', ({'-a':None, '-f':None, '-b':None},[]))
    checkParseArgsOK(p, '-afb hello', ({'-a':None, '-f':None, '-b':'hello'},[]))
    checkParseArgsFails(p, '-afc', ArgError)    # required arg for -c
    checkParseArgsOK(p, 'I -a say -fd hello world', ({'-a':None, '-f':None, '-d':['hello', 'world']},['I', 'say']))
    
    checkParseArgsFails(p, '-z', ArgError)
    checkParseArgsFails(p, '--zorglub', ArgError)
    
    print '=> tests passed.'

#----------------------------------------------------------------------------
#       M A I N
#----------------------------------------------------------------------------
if __name__ == "__main__":
    test()
