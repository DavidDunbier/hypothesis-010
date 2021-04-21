"""A Hypothesis extension for 010editor binary templates.

The only public API is `from_template`; check the docstring for details.
"""

import py010parser
import json
#from bson import BSON -- Apparently this isn't doing much, was from some testing I did earlier
from hypothesis import strategies as st
from functools import partial

__version__ = "0.0.1"
__all__ = ["from_template"]

strategy_assignment_dict = {
    
    """Am I accounting for different machines?
    Can  I also be cheeky and use global minimum and maximum values for the predefined types that exist in C - char, int etc?
    For safety's sake I've been nooby and hard-coded the appropriate values so far
    
    Check the two's compliment thing - a bunch of the things have that specified. As well as the specifications of the double precision and what not.
    """
    
    
        'int' : st.integers(min_value=-2147483648, max_value=2147483647), #Check the two's compliment thing
        'unsigned int' : st.integers(min_value=0, max_value=4294967295),
        'uint' : st.integers(min_value=0, max_value=4294967295), #unsigned int
        'int16' : st.integers(min_value=-32768, max_value=32767), #short, no?
        'uint16' : st.integers(min_value=0, max_value=65535), #unsigned short
        'unsigned int16' : st.integers(min_value=0, max_value=65535), #unsigned short
        'int64' : st.integers(min_value=-424967295, max_value=4294967294), #8 byte int, two's compliment?
        #uint64 = 8 byte unsigned int?
        #unsigned int64 = 8 byte unsigned int?
        
        
        'short' : st.integers(min_value=-32768, max_value=32767),
        'unsigned short' : st.integers(min_value=0, max_value=65535),
        'ushort' : st.integers(min_value=0, max_value=65535), #unsigned short
        
        'word' : st.integers(min_value=0, max_value=65535), #unsigned short
        'dword' : st.integers(min_value=-2147483648, max_value=2147483647), #Check the two's compliment thing, it's an int
        'long' : st.integers(min_value=-9223372036854775808, max_value=9223372036854775808), #Do I need to account for 32-bit machines??
        #long long = what. 2 int64s I guess
        'unsigned long' : st.integers(min_value=0, max_value=18446744073709551615), #Do I need to account for 32-bit machines??
        'ulong' : st.integers(min_value=0, max_value=18446744073709551615), #Do I need to account for 32-bit machines??
        'float' : st.floats(width=32),
        'double' : st.floats(width=64), #but bigger I guess right?
        'hfloat' : st.floats(width=16), #floats with a smaller width?
        
        'byte' = st.characters(min_codepoint=0, max_codepoint=255), #Just says 8 bits on the BSON spec. It says char in the parsed file??
        'ubyte' : st.characters(min_codepoint=0, max_codepoint=255), #Says unsigned char in the parsed file?
        'char' : st.characters(min_codepoint=0, max_codepoint=255),
        'unsigned char' : st.characters(min_codepoint=0, max_codepoint=255), #I mean python doesn't encode characters below 0, Idk what to make of that
        'uchar' : st.characters(min_codepoint=0, max_codepoint=255), #I mean python doesn't encode characters below 0, Idk what to make of that
        #dostime = st.lists()
        
        
    }

def strat_assign(node_name: string) -> st.SearchStrategy[any]:
    node_name = node_name.lower()
    if node_name in strategy_assignment_dict.keys():
        return strategy_assignment_dict[node_name]
    else:
        print("Pray")
        

def from_template(template_name: str) -> st.SearchStrategy[bytes]:
    """Parse the given template into a strategy."""
    
    ast = py010parser.parse_file(template_name) #Remove the IO from your library - Put it in a testing module or something
    ast.show()
    byte_count = 0
    child_strategies = []
    #recursivehelper(ast, byte_count) #Visits the nodes, still yet to assign bytes to them.
    #Doing that will mean that when a file is generated, this module knows how each data structure is built and formatted (to my understanding)
         
    
    #assert ast is True, "we know we don't actually handle templates yet"
    return st.just(b"") 



def recursivehelper(node: py010parser.c_ast.Node, byte_count: int) -> st.SearchStrategy[any]:
    if (len(node.children()) > 0):
        child_strategies = []
        for child_name, child in node.children():
            if (isinstance(child, list)):
                for elem in child:
                    recursivehelper(elem, byte_count)
                    #child_strategies.append(recursivehelper(elem, byte_count))
            else:
                recursivehelper(child, byte_count)
                #child_strategies.append(recursivehelper(child, byte_count))
        
        #overall_strategy = st.lists(child_strategies, min_size=len(node.children()))
        #return overall_strategy
        
    else: #end nodes only here, assign strategies using a fat dictionary or something
        if (hasattr(node, 'name')):
            print("end node of:", node.name)
            #my_strategy = strat_assign(node.name)
            #return my_strategy
            
            #Assign strategy here
        elif (hasattr(node, 'names')):
            print("Got a few names here in this node")
            node_name = ""
            for item in node.names:
                node_name += item + " "
            print("end node of:", node_name)
            #Assign strategy here I guess?
        elif (isinstance(node, py010parser.c_ast.Constant)):
            print("Constant here of type", node.type, "at value:", node.value)
            #Assign strategy here
        else:
            print(node, "is an end node of another type")
            

def value_from_template(ast: py010parser.c_ast.FileAST) -> st.SearchStrategy[any]:
    
    """Some kind of structure here - this is supposed to be applied to the ast given (from where again?)
    That means that it takes in the ast and returns a strategy that is supposed to successfully test each node and its children? I guess
    """
    
    """
    Lots of comments today but I BELIEVE at the moment that this function is just about applying hypothesis testing
    capabilities to each part of the AST in its given form. That means our recursive function only helps us identify the end nodes, not some of the trickier types that need multiple components.
    For BSON, that should be quickly identifiable - but it could be an issue in other file-type asts.
    """

    pass


def serialised_from_template(ast: py010parser.c_ast.FileAST) -> st.SearchStrategy[bytes]:
    return value_from_template(ast).map(partial(_dumps, ast))



def _dumps(ast: py010parser.c_ast.FileAST, value: object) -> bytes:
    
    #Let's try this only for BSON
    
    f = open("test.txt", "wb")
    binary_str = b""
    
    
    
    #Visit each node of the AST (already generated by py010parser)
    #Write the necessary bytes for each node - exploring each node as necessary.
    #eg a valid BSON document will have 4 bytes to begin with that are represented by the int32 at the start of the file, follwed by another element that ISN'T \x00 (in which case you go to the element node of the ast). Or, you follow it up with \x00.
    """The way I understand it is that you turn an object into a series of bytes here based on the corresponding type that it is in the AST? No way."""
    
    
    
    
    
    """Encode value according to the file format.
    
    Useful as s.map(partial(_dumps, ast))
    """
