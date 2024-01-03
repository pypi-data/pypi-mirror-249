import os
import ast
from typing import TypedDict


class FunctionArg(TypedDict):
    name: str
    type: str


class FunctionInfo(TypedDict):
    name: str
    docstring: str
    args: list[FunctionArg]
    return_type: str


class ClassInfo(TypedDict):
    name: str
    docstring: str
    methods: list[FunctionInfo]


class CosmosDocsInfo(TypedDict):
    file_path: str
    classes: list[ClassInfo]
    functions: list[FunctionInfo]


class CosmosDocs:
    def __init__(self, file_path: str, encodig: str = None) -> None:
        self.file_path = os.path.abspath(file_path)
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")

        self.file_encoding = encodig
        self.content = self.load_content()
        self.tree = ast.parse(self.content)
        self.file_info: CosmosDocsInfo = self.load_file_symbols()

    def load_content(self) -> str:
        with open(self.file_path, "r", encoding=self.file_encoding) as file:
            self.content = file.read()
        return self.content

    def load_file_symbols(self) -> list:
        result: CosmosDocsInfo = {
            "classes": [],
            "functions": [],
            "file_path": self.file_path,
        }

        for node in self.tree.body:
            if type(node) is ast.ClassDef:
                result["classes"].append(self.get_class_info(node))
            elif type(node) is ast.FunctionDef:
                result["functions"].append(self.get_function_info(node))

        return result

    def get_arg_type(self, node: ast.arg) -> str:
        try:
            arg_type = node.annotation.id
        except AttributeError:
            arg_type = None
        return arg_type

    def get_function_info(self, node: ast.FunctionDef) -> FunctionInfo:
        def get_function_args(node: ast.FunctionDef) -> list[FunctionArg]:
            args = []
            for arg in node.args.args:
                arg_type = self.get_arg_type(arg)
                args.append(
                    {
                        "name": arg.arg,
                        "type": arg_type,
                        "default": None,
                    }
                )
            defaults_length = len(node.args.defaults) if node.args.defaults else 0
            for index in range(defaults_length):
                default_index = (index + 1) * -1
                default = node.args.defaults[default_index]

                if type(default) is ast.Dict:
                    dict_default = {}
                    for key, value in zip(default.keys, default.values):
                        dict_default[key] = value
                    args[default_index]["default"] = dict_default
                    args[default_index]["type"] = "dict"
                else:
                    args[default_index]["default"] = default.value
                if args[default_index]["type"] is None:
                    args[default_index]["type"] = type(default.value).__name__
            return args

        try:
            function_return_type = node.returns.id
        except AttributeError:
            function_return_type = None

        return {
            "name": node.name,
            "docstring": ast.get_docstring(node),
            "args": get_function_args(node),
            "return_type": function_return_type,
        }

    def get_class_info(self, node: ast.ClassDef) -> ClassInfo:
        def get_class_methods(class_methods: ast.FunctionDef) -> list[FunctionInfo]:
            methods = []
            for child_node in class_methods:
                if isinstance(child_node, ast.FunctionDef):
                    methods.append(self.get_function_info(child_node))
            return methods

        return {
            "name": node.name,
            "docstring": ast.get_docstring(node),
            "methods": get_class_methods(node.body),
        }

    @property
    def markdown(self) -> str:
        markdown_result = ""

        for class_info in self.file_info["classes"]:
            markdown_result += f"# {class_info['name']}\n\n"
            markdown_result += f"{class_info['docstring']}\n\n"
            for method_info in class_info["methods"]:
                markdown_result += f"## {method_info['name']}\n\n"
                markdown_result += f"{method_info['docstring']}\n\n"
                markdown_result += "### Arguments\n\n"
                for arg in method_info["args"]:
                    markdown_result += f"- **{arg['name']}** (*{arg['type']}*): "
                    markdown_result += f"{arg['default']}\n"
                markdown_result += "\n"
                markdown_result += "### Return\n\n"
                markdown_result += f"- **{method_info['return_type']}**\n\n"
        for function_info in self.file_info["functions"]:
            markdown_result += f"# {function_info['name']}\n\n"
            markdown_result += f"{function_info['docstring']}\n\n"
            markdown_result += "### Arguments\n\n"
            for arg in function_info["args"]:
                markdown_result += f"- **{arg['name']}** (*{arg['type']}*): "
                markdown_result += f"{arg['default']}\n"
            markdown_result += "\n"
            markdown_result += "### Return\n\n"
            markdown_result += f"- **{function_info['return_type']}**\n\n"
        return markdown_result
