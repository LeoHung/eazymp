import re


class SharedVariables:
    SHARED_DICT = 1
    SHARED_LIST = 2
    SHARED_NUMBER = 3
    SHARED_DICT_REDUCE = 4

    def __init__(self):
        self.shared = {}

    def register(self, variable, variable_type):
        self.shared[variable] = (variable, variable_type)

    # def dump(self):
    #     return self.shared.keys()

    def dump(self):
        return self.shared.values()

    def clean(self):
        self.shared = {}


class Parser:
    space_prog = re.compile("^( *)[^ ]*")
    comment_prog = re.compile("(#.*)$")
    for_prog = re.compile("for ([^ ]+) in ([^:]+):")

    def __init__(self, inputfilename):
        self.f = open(inputfilename)
        self.last_line = None
        self.last_struct = None

    def parse_for(self, line):
        tmp = Parser.for_prog.search(line)

        if tmp is None:
            return None, None
        else:
            line, line_struct = self.parse_line(line)

            return line, {'indention' : line_struct['indention'],
                            "variable": tmp.group(1),
                            "iterate_list": tmp.group(2)}

    def parse_blcok(self):
        block_lines = []
        last_indention = None
        while True:
            line, struct = self.parse()
            if line is None:
                break

            if last_indention is None:
                last_indention = struct['indention']
                block_lines.append(line)
            else:
                if last_indention > struct['indention']: # next block
                    self.last_line, self.last_struct = line, struct
                    break
                else:
                    block_lines.append(line)

        return block_lines, {'indention': last_indention}

    def parse(self):
        if self.last_line is not None:
            tmp_line = self.last_line
            tmp_struct = self.last_struct
            self.last_line = None
            self.last_struct = None
            return tmp_line, tmp_struct

        self.line = self.f.readline()

        # last line
        if self.line == '':
            return None, None

        self.line = self.line[:-1]

        return self.parse_line(self.line)

    def parse_line(self, line):
        # indention
        space_match = Parser.space_prog.match(self.line)
        indention = 0
        if space_match is not None:
            indention = len(space_match.group(1))

        # comment
        comment_match = Parser.comment_prog.match(self.line)
        comment = None
        if comment_match is not None:
            comment = comment_match.group(1)

        # tokens :
        tokens = []
        split_tmp = [t for t in self.line.split(" ") if len(t) > 0]
        pragma_tokens = None
        for i in xrange(len(split_tmp)):
            if len(split_tmp[i]) == 0:
                continue
            if split_tmp[i] == Annotation.PREFIX:
                pragma_tokens = split_tmp[i:]
                break
            if split_tmp[i] == "#":
                break
            tokens.append(split_tmp[i])

        return self.line, {
                            "indention": indention,
                            "comment": comment,
                            "tokens": tokens,
                            "pragma_tokens": pragma_tokens
                            }
    def close(self):
        self.f.close()


class Writer:
    def __init__(self, outputfilename):
        self.f = open(outputfilename, "w")

    def write(self, line):
        print >> self.f, line

    def write_block(self, block):
        for line in block:
            self.write(line)

    def close(self):
        self.f.close()


class Template:
    @staticmethod
    def def_function(variable, function_name, indention=0):
        return "%sdef %s(%s):" %(" " * indention, function_name, variable)

    @staticmethod
    def define_variable(left, right, indention=0):
        return "%s%s = %s" %(" " * indention, left, right)

    @staticmethod
    def assign_variable(left, right, indention=0):
        return Template.define_variable(left, right, indention)

    @staticmethod
    def return_variable(variable, indention=0):
        return "%sreturn %s" % (" " * indention, variable)




    @staticmethod
    def import_module(module, package=None,abbr=None, indention=0):
        indention_str = " " * indention
        if package is None:
            if abbr is None:
                return "%simport %s" %(indention_str, module)
            else:
                return "%simport %s as %s" %(indention_str, module, abbr)
        else:
            if abbr is None:
                return "%sfrom %s import %s" %(indention_str, package, module)
            else:
                return "%sfrom %s import %s as %s" %(indention_str, package, module, abbr)

    @staticmethod
    def execute_function(function_name, variables, indention=0):
        if type(variables) is str:
            variables_str = variables
        elif type(variables) is list:
            variables_str = ", ".join(variables)
        return "%s%s(%s)" % (" "* indention, function_name, variables_str)



class Annotation:
    PREFIX = "#pragma"

    SHARED_VARIABLES = "#pragma[ ]+shared"

    SHARED_DICT_REDUCE = "#pragma[ ]+shared[ ]+dict[ ]+reduce"

    SHARED_DICT = "#pragma[ ]+shared[ ]+dict"
    SHARED_LIST = "#pragma[ ]+shared[ ]+list"
    SHARED_NUMBER = "#pragma[ ]+shared[ ]+number"

    PARALLEL_FOR = "#pragma[ ]+omp[ ]+parallel[ ]+for"


class STATE:
    NORMAL = 1
    PARALLEL_FOR = 2


class PragmaTranslator:
    parallel_prog = re.compile(Annotation.PARALLEL_FOR)
    shared_dict_prog = re.compile(Annotation.SHARED_DICT)
    shared_list_prog = re.compile(Annotation.SHARED_LIST)
    shared_number_prog = re.compile(Annotation.SHARED_NUMBER)
    shared_dict_reduce_prog = re.compile(Annotation.SHARED_DICT_REDUCE)

    PARALLEL_FOR = 1
    SHARED_VARIABLES = 2
    SHARED_DICT = 3
    SHARED_LIST = 4
    SHARED_NUMBER = 5
    SHARED_DICT_REDUCE = 6
    ELSE = 7

    @staticmethod
    def parse(pragma_tokens):
        command = " ".join(pragma_tokens)

        reg_type = [
            (PragmaTranslator.shared_dict_reduce_prog, PragmaTranslator.SHARED_DICT_REDUCE),
            (PragmaTranslator.parallel_prog, PragmaTranslator.PARALLEL_FOR),
            (PragmaTranslator.shared_dict_prog, PragmaTranslator.SHARED_DICT),
            (PragmaTranslator.shared_list_prog, PragmaTranslator.SHARED_LIST),
            (PragmaTranslator.shared_number_prog, PragmaTranslator.SHARED_NUMBER)
        ]

        for reg_prog, return_type in reg_type:
            tmp = reg_prog.match(command)
            # if  "#pragma" in command:
            #     print command
            #     print tmp
            if tmp is not None:
                return return_type

        return PragmaTranslator.ELSE


class Translator:

    def __init__(self, inputfilename, outputfilename, p=0):
        self.parser = Parser(inputfilename)
        self.writer = Writer(outputfilename)
        self.state = STATE.NORMAL
        self.shared_variables = SharedVariables()
        if p < 1:
            import multiprocessing
            self.threads = multiprocessing.cpu_count()
        else:
            self.threads = p

    def process_parallel_for(self, line, struct):
        # parallel for
        parallel_line, parallel_struct = self.parser.parse_for(line)
        if parallel_line is None:
            # cannot parse parallel for correctly
            self.writer.write(line)
        else:
            # parse block
            block, block_struct = self.parser.parse_blcok()

            # insert shared Manager (for shared dict, list, number)
            self.writer.write(
                Template.import_module(
                    module="Manager",
                    package="multiprocessing",
                    indention=parallel_struct['indention']
                )
            )

            self.writer.write(
                Template.assign_variable(
                    left="_manager",
                    right="Manager()",
                    indention=parallel_struct['indention']
                )
            )
            self.writer.write(
                Template.assign_variable(
                    left="_namespace",
                    right="_manager.Namespace()",
                    indention=parallel_struct['indention']
                )
            )
            self.writer.write(
                Template.assign_variable(
                    left="_lock",
                    right="_manager.Lock()",
                    indention=parallel_struct['indention']
                )
            )

            # initial proxy, and copy shared dict, list, number
            # import copy_dict, copy_list
            self.writer.write(
                Template.import_module(
                    package="lazymp.helpers",
                    module="copy_dict",
                    indention=parallel_struct['indention']
                )
            )
            self.writer.write(
                Template.import_module(
                    package="lazymp.helpers",
                    module="copy_list",
                    indention=parallel_struct['indention']
                )
            )

            for registered_variable, variable_type in self.shared_variables.dump():
                if variable_type == SharedVariables.SHARED_DICT:
                    # initialize proxy for dict, and copy from original dict
                    self.writer.write(
                        Template.assign_variable(
                            left="proxy_" + registered_variable,
                            right="_manager.dict()",
                            indention=parallel_struct['indention']
                        )
                    )
                    self.writer.write(
                        Template.execute_function(
                            function_name="copy_dict",
                            variables=[registered_variable, "proxy_" + registered_variable],
                            indention=parallel_struct['indention']
                        )
                    )

                elif variable_type == SharedVariables.SHARED_LIST:
                    # initialize proxy for list, and copy from original list
                    self.writer.write(
                        Template.assign_variable(
                            left="proxy_" + registered_variable,
                            right="_manager.list()",
                            indention=parallel_struct['indention']
                        )
                    )
                    self.writer.write(
                        Template.execute_function(
                            function_name="copy_list",
                            variables=[registered_variable, "proxy_" + registered_variable],
                            indention=parallel_struct['indention']
                        )
                    )
                elif variable_type == SharedVariables.SHARED_NUMBER:
                    # initializae proxy for number, and copy from original number
                    self.writer.write(
                        Template.assign_variable(
                            left="_namespace." + registered_variable,
                            right=registered_variable,
                            indention=parallel_struct['indention']
                        )
                    )

            # rewrite code
            self.writer.write(
                Template.def_function(
                    variable=parallel_struct['variable'],
                    function_name="core",
                    indention=parallel_struct['indention']
                )
            )

            # insert registered code
            self.writer.write(
                Template.define_variable(
                    left = "__shared__",
                    right= "{}",
                    indention=block_struct['indention']
                )
            )
            # import copy
            self.writer.write(
                Template.import_module(
                    module="copy",
                    indention=block_struct['indention']
                )
            )

            for registered_variable, variable_type in self.shared_variables.dump():
                if variable_type == SharedVariables.SHARED_DICT_REDUCE:
                    self.writer.write(
                        Template.define_variable(
                            left = "__shared__['%s']" % registered_variable,
                            right = "copy.deepcopy(%s)" % registered_variable,
                            indention=block_struct['indention']
                        )
                    )

            # insert block

            block_text = "\n".join(block)
            # replace with Atomic() -> with _lock()
            block_text = re.sub("with[ ]+Atomic\([^)]*\)", "with _lock", block_text)

            # replace shared dict reduce with __shared__['%s']
            # replace shared dict, list with proxy_%s
            # replace shared number with _namespace.%s
            for registered_variable, variable_type in self.shared_variables.dump():
                if variable_type == SharedVariables.SHARED_DICT_REDUCE:
                    block_text = block_text.replace(registered_variable, "__shared__['%s']" % registered_variable)
                elif variable_type == SharedVariables.SHARED_DICT or variable_type == SharedVariables.SHARED_LIST:
                    block_text = block_text.replace(registered_variable, "proxy_%s" % registered_variable)
                elif variable_type == SharedVariables.SHARED_NUMBER:
                    block_text = block_text.replace(registered_variable, "_namespace.%s" %registered_variable)


            self.writer.write(block_text)

            # insert footer
            self.writer.write(
                Template.return_variable(
                    variable="__shared__",
                    indention=block_struct['indention']
                )
            )
            # insert import pathos.multiprocessing ProcessingPool
            self.writer.write(
                Template.import_module(
                    package="pathos.multiprocessing",
                    module="ProcessingPool",
                    indention=parallel_struct['indention']
                )
            )
            # insert __shared__ = ProcessingPool(4).map(core, range(size_x))
            self.writer.write(
                    Template.define_variable(
                        left = "__shared__",
                        right = "ProcessingPool(%d).map(core, %s)" %(
                            self.threads,
                            parallel_struct['iterate_list']),
                        indention=parallel_struct['indention']
                    )
            )
            # insert Merge function
            tmp_list =[ ]
            for registered_variable, variable_type in self.shared_variables.dump():
                if variable_type == SharedVariables.SHARED_DICT_REDUCE:
                    tmp_list.append("'%s': %s" % (registered_variable, registered_variable) )
            registered_variable_dict_str = "{ %s }" %(", ".join(tmp_list))

            self.writer.write(
                Template.execute_function(
                    function_name="join_shared",
                    variables=["__shared__", registered_variable_dict_str],
                    indention=parallel_struct['indention']
                )
            )

            # copy dict, list, number from proxy
            for registered_variable, variable_type in self.shared_variables.dump():
                if variable_type == SharedVariables.SHARED_DICT:
                    # copy from proxy dict
                    self.writer.write(
                        Template.execute_function(
                            function_name="copy_dict",
                            variables=["proxy_" + registered_variable, registered_variable],
                            indention=parallel_struct['indention']
                        )
                    )

                elif variable_type == SharedVariables.SHARED_LIST:
                    # copy from proxy list
                    self.writer.write(
                        Template.execute_function(
                            function_name="copy_new_list",
                            variables=["proxy_" + registered_variable, registered_variable],
                            indention=parallel_struct['indention']
                        )
                    )
                elif variable_type == SharedVariables.SHARED_NUMBER:
                    # copy back from proxy number
                    self.writer.write(
                        Template.assign_variable(
                            left=registered_variable,
                            right="_namespace." + registered_variable,
                            indention=parallel_struct['indention']
                        )
                    )


    def process_variables(self, line, struct, variable_type):
        # need to check token struct first
        assert re.search("[^=]+=[^ ]+", line) ==None, "'%s' is not a delaration of variable."

        # parse variable name
        variable = struct['tokens'][0]

        # register
        self.shared_variables.register(variable, variable_type)


    def process_shared_dict_reduce(self, line, struct):
        self.process_variables(line, struct, SharedVariables.SHARED_DICT_REDUCE)

        # # need to check token struct first
        # assert re.search("[^=]+=[^ ]+", line) ==None, "'%s' is not a delaration of variable."

        # # parse variable name
        # variable = struct['tokens'][0]

        # # register
        # self.shared_variables.register(variable, SHARED_VARIABLES.SHARED_DICT_REDUCE)

    def process_shared_dict(self, line, struct):
        self.process_variables(line, struct, SharedVariables.SHARED_DICT)

    def process_shared_list(self, line, struct):
        self.process_variables(line, struct, SharedVariables.SHARED_LIST)

    def process_shared_number(self, line, struct):
        self.process_variables(line, struct, SharedVariables.SHARED_NUMBER)

    def header(self):
        self.writer.write(
            Template.import_module(
                package="lazymp.helpers",
                module="join_dict"
            )
        )
        self.writer.write(
            Template.import_module(
                package="lazymp.helpers",
                module="join_shared"
            )
        )

    def run(self):
        self.header()

        while True:
            line, struct = self.parser.parse()
            if line == None:
                break

            if self.state == STATE.NORMAL:
                if struct.get('pragma_tokens') is not None:
                    pragma_type = PragmaTranslator.parse(struct.get('pragma_tokens'))
                    if pragma_type == PragmaTranslator.PARALLEL_FOR:
                        self.process_parallel_for(line, struct)
                    elif pragma_type == PragmaTranslator.SHARED_DICT_REDUCE:
                        self.process_shared_dict_reduce(line, struct)
                        self.writer.write(line)
                    elif pragma_type == PragmaTranslator.SHARED_DICT:
                        self.process_shared_dict(line, struct)
                        self.writer.write(line)
                    elif pragma_type == PragmaTranslator.SHARED_LIST:
                        self.process_shared_list(line, struct)
                        self.writer.write(line)
                    elif pragma_type == PragmaTranslator.SHARED_NUMBER:
                        self.process_shared_number(line, struct)
                        self.writer.write(line)
                    else:
                        self.writer.write(line)
                else:
                    self.writer.write(line)

    def close(self):
        self.parser.close()
        self.writer.close()


def translate(inputfilename, outputfilename, p):
    translator = Translator(inputfilename, outputfilename, p)
    translator.run()
    translator.close()


def run():
    import sys
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-p", type="int", dest="p", default=-1)
    (options, args) = parser.parse_args()

    inputfilename_i = 0
    for a_i in xrange(1, len(sys.argv)):
        if sys.argv[a_i][0] == "-":
            continue
        else:
            inputfilename_i = a_i
            break

    inputfilename = sys.argv[inputfilename_i]
    tmp_outputfilename = "tmp." + inputfilename
    translate(inputfilename, tmp_outputfilename, options.p)
    import os
    if len(sys.argv) >= inputfilename_i + 1:
        rest_options = " ".join(sys.argv[inputfilename_i + 1:])
    else:
        rest_options = ""

    os.system("python " + tmp_outputfilename + " " + rest_options)
    os.remove(tmp_outputfilename)

if __name__ == "__main__":
    run()
