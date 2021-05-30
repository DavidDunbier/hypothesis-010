"""A Hypothesis extension for 010editor binary templates.

The only public API is `from_template`; check the docstring for details.
"""

from functools import partial

import py010parser

# from bson import BSON -- Apparently this isn't doing much, was from some testing I did earlier
from hypothesis import strategies as st

import struct
import sys

__version__ = "0.0.1"
__all__ = ["from_template"]

"""Am I accounting for different machines?
Can  I also be cheeky and use global minimum and maximum values for the predefined types that exist in C - char, int etc?
For safety's sake I've been nooby and hard-coded the appropriate values so far
    
Check the two's compliment thing - a bunch of the things have that specified. As well as the specifications of the double precision and what not.
"""



"""
Here are some functions that I was gonna use to convert basic types into bytes.
These account for the different types in strategy_assignment_dict, of which there aren't many.
It's getting them converted to bytes when all you have to go on is their generated types later on, without regard for their sign or format.
You could apply a recursive strategy to find every end element but it won't account for limits on the strategy used to generate the example, and might cause issues when accounting for sign or format'
"""
def to_bytes_int(x: int, sign: bool) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, byteorder=sys.byteorder, signed=sign)

def to_bytes_char(x: chr) -> bytes:
    return bytes(x, "utf-8")

def to_bytes_float(x: float, float_format: str) -> bytes:
    return bytes(bytearray(struct.pack(float_format, x)))

"""
Unfinished - because of the problems listed above
"""
def to_bytes_list(list_in: list) -> bytes:
    bytestring = b""
    for elem in list_in:
        if isinstance(elem, chr):
            bytestring.append(to_bytes_char(elem))
    
    return bytestring
            
    
"""
Global assignment dictionary for primitive types used, and the function or functions you would use to write their generated examples into bytestrings
"""
strategy_assignment_dict = {
    "int": (st.integers(
        min_value=-2147483648, max_value=2147483647
    ), partial(to_bytes_int, sign=True)),  # Check the two's compliment thing
    "unsignedint": (st.integers(min_value=0, max_value=4294967295), partial(to_bytes_int, sign=False)),
    "uint": (st.integers(min_value=0, max_value=4294967295), partial(to_bytes_int, sign=False)),  # unsigned int
    "int16": (st.integers(min_value=-32768, max_value=32767), partial(to_bytes_int, sign=True)),  # short, no?
    "uint16": (st.integers(min_value=0, max_value=65535), partial(to_bytes_int, sign=False)),  # unsigned short
    "unsignedint16": (st.integers(min_value=0, max_value=65535), partial(to_bytes_int, sign=False)),  # unsigned short
    "int64": (st.integers(
        min_value=-9223372036854775808, max_value=9223372036854775807
    ), partial(to_bytes_int, sign=True)),  # 8 byte int, two's compliment?
    "uint64": (st.integers(min_value=0, max_value=18446744073709551615), partial(to_bytes_int, sign=False)),
    "unsignedint64": (st.integers(min_value=0, max_value=18446744073709551615), partial(to_bytes_int, sign=False)),
    "short": (st.integers(min_value=-32768, max_value=32767), partial(to_bytes_int, sign=True)),
    "unsignedshort": (st.integers(min_value=0, max_value=65535), partial(to_bytes_int, sign=False)),
    "ushort": (st.integers(min_value=0, max_value=65535), partial(to_bytes_int, sign=False)),  # unsigned short
    "word": (st.integers(min_value=0, max_value=65535), partial(to_bytes_int, sign=False)),  # unsigned short
    "dword": (st.integers(
        min_value=-2147483648, max_value=2147483647
    ), partial(to_bytes_int, sign=True)),  # Check the two's compliment thing, it's an int
    "long": (st.integers(
        min_value=-9223372036854775808, max_value=9223372036854775808
    ), partial(to_bytes_int, sign=True)),  # Do I need to account for 32-bit machines??
    "longlong": (st.integers(
        min_value=-9223372036854775808, max_value=9223372036854775808
    ), partial(to_bytes_int, sign=True)),  # Turns out on a 64-bit compiler they're the same
    "unsignedlong": (st.integers(
        min_value=0, max_value=18446744073709551615
    ), partial(to_bytes_int, sign=False)),  # Do I need to account for 32-bit machines??
    "ulong": (st.integers(
        min_value=0, max_value=18446744073709551615
    ), partial(to_bytes_int, sign=False)),  # Do I need to account for 32-bit machines??
    "float": (st.floats(width=32), partial(to_bytes_float, float_format="!f")),
    "double": (st.floats(width=64), partial(to_bytes_float, float_format="!d")),  # but bigger I guess right?
    "hfloat": (st.floats(width=16), partial(to_bytes_float, float_format="!e")),  # floats with a smaller width?
    "byte": (st.characters(
        min_codepoint=0, max_codepoint=255
    ), to_bytes_char),  # 8 bits on the bson spec, char in the parsed file?
    "ubyte": (st.characters(
        min_codepoint=0, max_codepoint=255
    ), to_bytes_char),  # Says unsigned char in the parsed file?
    "char": (st.characters(min_codepoint=0, max_codepoint=255), to_bytes_char),
    "unsignedchar": (st.characters(
        min_codepoint=0, max_codepoint=255
    ), to_bytes_char),  # I mean python doesn't encode characters below 0, Idk what to make of that
    "uchar": (st.characters(
        min_codepoint=0, max_codepoint=255
    ), to_bytes_char),  # I mean python doesn't encode characters below 0, Idk what to make of that
    "second": (st.integers(
        min_value=0, max_value=31
    ), partial(to_bytes_int, sign=False)),  # dostime strats, they're of a certain bitsize and yes this is THAT jank
    "minute": (st.integers(min_value=0, max_value=63), partial(to_bytes_int, sign=False)),
    "hour": (st.integers(min_value=0, max_value=31), partial(to_bytes_int, sign=False)),
    "tagdostime": (st.tuples(
        st.integers(min_value=0, max_value=31),
        st.integers(min_value=0, max_value=63),
        st.integers(min_value=0, max_value=31),
    ), lambda t: b"".join(map(partial(to_bytes_int, sign=False), t))),
    "day": (st.integers(min_value=0, max_value=31), partial(to_bytes_int, sign=False)),
    "month": (st.integers(min_value=0, max_value=15), partial(to_bytes_int, sign=False)),
    "year": (st.integers(min_value=0, max_value=127), partial(to_bytes_int, sign=False)),
    "tagdosdate": (st.tuples(
        st.integers(min_value=0, max_value=31),
        st.integers(min_value=0, max_value=15),
        st.integers(min_value=0, max_value=127),
    ), lambda t: b"".join(map(partial(to_bytes_int, sign=False), t))),
    "dwlowdatetime": (st.integers(
        min_value=-2147483648, max_value=2147483647
    ), partial(to_bytes_int, sign=True)),  # Check the two's compliment thing, it's an int
    "dwhighdatetime": (st.integers(
        min_value=-2147483648, max_value=2147483647
    ), partial(to_bytes_int, sign=True)),  # Check the two's compliment thing, it's an int
    "_filetime": (st.tuples(
        st.integers(min_value=-2147483648, max_value=2147483647),
        st.integers(min_value=-2147483648, max_value=2147483647),
    ), lambda t: b"".join(map(partial(to_bytes_int, sign=True), t))),
}

unassigned_strats = [] #For listing off objects that don't have a strategy in either the tree above or a way to compose them in parseTree below

"""
Global variables for where the strategies to be used in the filetype parsed are written,
And blank context is used as a starter string for contexts to be written to during parseTree
"""
strat_dict = {}
blank_context = ""
gen_as_bytes = True
                 
def strat_assign(node_name: str, gen_as_bytes: bool) -> st.SearchStrategy[any]:
    nodename = node_name.lower()
    nodename = nodename.lstrip()
    nodename = nodename.rstrip()
    if nodename in strategy_assignment_dict:
        print("Strat assigned")
        strat, function = strategy_assignment_dict[nodename]
        if gen_as_bytes:
            return strat.map(function)
        return strat
    else:
        print(node_name + " needs assigning?")
        unassigned_strats.append(node_name)
        return st.none()


def from_template(template_name: str) -> st.SearchStrategy[bytes]:
    """Parse the given template into a strategy."""

    ast = py010parser.parse_file(
        template_name
    )  # Remove the IO from your library - Put it in a testing module or something
    # ast.show()
    
    gen_as_bytes = True
    ast_strat = parseTree(ast, blank_context)
    

    # assert ast is True, "we know we don't actually handle templates yet"
    return st.just(b"")

def getNodeName(node: py010parser.c_ast.Node) -> str:
    if hasattr(node, "name"):
        node_name = node.name
        return node_name
    else:
        node_name = node.__class__.__name__
        return node_name
    
def createContextName(parentcontext: str, node: py010parser.c_ast.Node) -> str:
    return parentcontext + getNodeName(node)


def parseTree(node: py010parser.c_ast.Node, context: str) -> st.SearchStrategy[any]:
    #Create current context - path to reach this node
    mycontext = createContextName(context, node)
    print(mycontext)

    if len(node.children()) > 0:

        if isinstance(node, py010parser.c_ast.FileAST):
            for child_name, child in node.children():
                parseTree(child, mycontext)
            # Currently specific for Mifare4k this time only, I'm out of options
            # Each file spec has a root node however (aside from the global ones that are present in every ast) that I'm sure you could rename to "file" if you were so inclined
            if (mycontext + "file") in strat_dict:
                print("AST Strat assigned")
                strat_dict[mycontext] = strat_dict[(mycontext + "file")]
                with open("Result_Strat.txt", "w") as result_file:
                    print(strat_dict[mycontext], file=result_file)
                return strat_dict[
                    mycontext
                ]
            else:
                print(
                    "No valid root node found, check through the produced strat_dict and find the corresponding root to look for in the function"
                )
                return st.none()

        # ArrayDecls in this ast always include a type of object in that array and a dimension attribute, which I presume to be number of objects inside the array.
        elif isinstance(node, py010parser.c_ast.ArrayDecl):
            print("Parsing array")
            array_length = int(node.dim.value)
            parseTree(node.type, mycontext)
            array_contents = getNodeName(node.type)
            strat_dict[mycontext] = st.lists(
                    elements=strat_dict[(mycontext+array_contents)],
                    min_size=array_length,
                    max_size=array_length,
                ).map(tuple)
                
            
        elif isinstance(node, py010parser.c_ast.Struct):
            if node.name.lower() in strategy_assignment_dict:
                print(
                    "It's a global dtype stupid, should be in the strategy_assignment_dict"
                )
                strat_dict[mycontext] = strat_assign(node.name.lower(), gen_as_bytes) 
            else:
                struct_strat_list = []
                for child_name, child in node.children():
                    parseTree(child, mycontext)
                    recorded_child_name = getNodeName(child)
                    struct_strat_list.append(
                        strat_dict[(mycontext + recorded_child_name)]
                    )
                    strat_dict[mycontext] = st.tuples(*struct_strat_list)

        # Decls mishandles a lot of things - Mainly, any decls that have more than one child.
        # This is because in most examples I've looked at it will rely on types and/or values evaluated in some other part of the tree - Entirely possible to look them up, given more time.
        elif isinstance(node, py010parser.c_ast.Decl):
            if len(node.children()) == 1:
                parseTree(node.children()[0][1], mycontext)
                node_name = getNodeName(node.children()[0][1])
                strat_dict[mycontext] = strat_dict[(mycontext + node_name)]
            else:
                print(
                    "This decl of: "
                    + node.name
                    + " is one of those cases with two children, a type and a dimension."
                )
                print("Leaving this decl alone")

        elif isinstance(node, py010parser.c_ast.TypeDecl):
            # Assumes a lot of things - typedecls are usually only made with one child, an identifiertype, that usually exists in the global dictionary already. God help you if it doesn't.
            if len(node.children()) == 1 and isinstance(
                node.children()[0][1], py010parser.c_ast.IdentifierType
            ):
                parseTree(node.children()[0][1], mycontext)
                node_name = ""
                for item in node.children()[0][1].names:
                    node_name += item
                strat_dict[mycontext] = strat_dict[
                    (mycontext + node.children()[0][1].__class__.__name__ + node_name)
                ]

            elif len(node.children()) == 1 and isinstance(
                node.children()[0][1], py010parser.c_ast.Struct
            ):
                parseTree(node.children()[0][1], mycontext)
                strat_dict[mycontext] = strat_dict[
                    (mycontext + node.children()[0][1].name)
                ]
            else:
                for child_name, child in node.children():
                    parseTree(child, mycontext)
                    if hasattr(child, "name"):
                        print("Accessed: " + child.name)
                        strat_dict[mycontext] = strat_dict[(mycontext + child.name)]
                    else:
                        print("Accessed: " + child.__class__.__name__)
                        strat_dict[mycontext] = strat_dict[
                            (mycontext + child.__class__.__name__)
                        ]

        # General case
        else:
            for child_name, child in node.children():
                print("Accessing: " + getNodeName(child))
                parseTree(child, mycontext)
                # Do I need to add an entry for this general context if the strategy used here is never looked up? Probably

    # End nodes only, should assign base strategies for these end nodes
    else:
        if isinstance(node, py010parser.c_ast.IdentifierType):
            if hasattr(node, "name"):
                mycontext += node.name
                my_strategy = strat_assign(node.name, gen_as_bytes)
            elif hasattr(node, "names"):
                node_name = ""
                for item in node.names:
                    node_name += item
                mycontext += node_name
                my_strategy = strat_assign(node_name, gen_as_bytes)
            strat_dict[mycontext] = my_strategy
        else:
            print(
                "This isn't an identifier type, which means it's some other value probably important to the parent. Exiting without doing anything"
            )
   
concatenated_example = b"" #Where the byte string from the example drawn gets placed. I know it's bad practice but it works!


def example_to_bytes(strat: st.SearchStrategy[any]) -> bytes:
    strat_example = strat.example()  
    to_bytes_recursive(strat_example)
    return concatenated_example
    



def to_bytes_recursive(strat: tuple):
    for elem in strat:
        if isinstance(elem, bytes):
            global concatenated_example
            concatenated_example += elem
        else:
            to_bytes_recursive(elem)


"""
I was working on this until I realised that a concrete list to pass through every recursion wasn't going to cut it.
Mainly because I would never be able to wrap my head around properly constructing this list of strategies.
Used some of the ideas from here in parseTree which instead uses a global dictionary to store context. Yup. Behold and despair.
"""


def fixedrecursivehelper(
    node: py010parser.c_ast.Node, strat_list: list
) -> st.SearchStrategy[any]:
    # TypeDef - The Most Simple
    if isinstance(node, py010parser.c_ast.TypeDecl):
        for elem in node.children():
            if isinstance(elem, py010parser.c_ast.IdentifierType):
                strat = st.lists(strat_assign(elem.name))
                strat_list.append(strat)
            elif isinstance(elem, py010parser.c_ast.Struct):
                strat = st.lists(fixedrecursivehelper(elem, strat_list))
                return strat
            # Need to account for enumerators here

    elif isinstance(node, py010parser.c_ast.Struct):
        if len(node.children()) > 0:
            for elem in node.children():
                strat = st.lists(fixedrecursivehelper(elem, strat_list))
                return strat
        else:
            strat = strat_assign(
                node.name
            )  # Permenant composite strategies that get created earlier are an issue as of now, as is the document strategy.
            # How will the program know it's making a composite strategy that needs to be remembered for later when elements of another type require that strategy? What about the documents inside of documents thing, do you reference the strategy that isn't complete yet? Reference where it should be?
            return strat

    elif isinstance(node, py010parser.c_ast.ArrayDecl):
        array_length = node.dim
        strat = st.lists(
            elements=fixedrecursivehelper(node.type, strat_list), max_size=array_length
        )

    elif isinstance(node, py010parser.c_ast.Decl):
        if node.name is None:
            assert len(node.children()) == 1
            strat = fixedrecursivehelper(node.children()[0], strat_list)
            return strat
        else:
            for elem in node.children():
                strat = fixedrecursivehelper(elem, strat_list)
                return strat

    else:
        print("Going through another type of node: ", type(node))
        if isinstance(node, py010parser.c_ast.FileAST):

            for child_name, child in node.children():
                strat = fixedrecursivehelper(child, strat_list)
                strat_list += strat

            return st.lists(strat_list)

        else:
            for elem in node.children():
                strat = fixedrecursivehelper(elem, strat_list)
                strat_list


"""
My earliest experiments in exploring the ast of any binary filetype template.
"""


def recursivehelper(
    node: py010parser.c_ast.Node, byte_count: int, strat_list: list
) -> st.SearchStrategy[any]:
    if isinstance(node.children(), tuple):
        child_list = []
        for elem in node.children():
            child_list += elem
    """if hasattr(node, "decls"):
        print("Accessing struct")
        struct_strat = []
        for elem in node.decls:
            return st.nothing()  # TODO: broken temp workaround
            decl_strat = st.lists(max_size=elem.Constant) #Think about this
            struct_strat.append(recursivehelper(elem, byte_count, strat_list))
            strat_list.append(struct_strat)
    """
    if len(node.children()) > 0:
        for child_name, child in node.children():
            """
            if (isinstance(node, py010parser.c_ast.Struct)):
                struct_strat = []
                for elem in node.children():
                    #recursivehelper(elem, byte_count)
                    struct_strat.append(recursivehelper(elem, byte_count, strat_list))
                    strat_list.append(struct_strat)
            """
            if isinstance(child, list):
                for elem in child:
                    # recursivehelper(elem, byte_count)
                    strat_list.append(recursivehelper(elem, byte_count, strat_list))
            else:
                # recursivehelper(child, byte_count)
                strat_list.append(recursivehelper(child, byte_count, strat_list))

        overall_strategy = st.lists(strat_list)
        return overall_strategy

    else:  # end nodes only here, assign strategies using a fat dictionary or something

        if hasattr(node, "name"):
            print("end node of:", node.name)
            my_strategy = strat_assign(node.name)
            return my_strategy

            # Assign strategy here
        elif hasattr(node, "names"):
            node_name = ""
            for item in node.names:
                node_name += item + " "
            print("end node of:", node_name)
            my_strategy = strat_assign(node_name)
            # Assign strategy here I guess?
        elif isinstance(node, py010parser.c_ast.Constant):
            print("Constant here of type", node.type, "at value:", node.value)
            # Assign strategy here
        else:
            print(node, "is an end node of another type")


"""
An experiment at bytestring making
"""
        

"""
Back to the good stuff here
"""


def value_from_template(ast: py010parser.c_ast.FileAST) -> st.SearchStrategy[any]:

    """Some kind of structure here - this is supposed to be applied to the ast given (from where again?)
    That means that it takes in the ast and returns a strategy that is supposed to successfully test each node and its children? I guess
    """

    """
    Lots of comments today but I BELIEVE at the moment that this function is just about applying hypothesis testing
    capabilities to each part of the AST in its given form. That means our recursive function only helps us identify the end nodes, not some of the trickier types that need multiple components.
    For BSON, that should be quickly identifiable - but it could be an issue in other file-type asts.
    """


def serialised_from_template(
    ast: py010parser.c_ast.FileAST,
) -> st.SearchStrategy[bytes]:
    return value_from_template(ast).map(partial(_dumps, ast))


def _dumps(ast: py010parser.c_ast.FileAST, value: object) -> bytes:

    # Let's try this only for BSON

    open("test.txt", "wb")

    # Visit each node of the AST (already generated by py010parser)
    # Write the necessary bytes for each node - exploring each node as necessary.
    # eg a valid BSON document will have 4 bytes to begin with that are represented by the int32 at the start of the file, follwed by another element that ISN'T \x00 (in which case you go to the element node of the ast). Or, you follow it up with \x00.
    """The way I understand it is that you turn an object into a series of bytes here based on the corresponding type that it is in the AST? No way."""

    """Encode value according to the file format.
    
    Useful as s.map(partial(_dumps, ast))
    """
