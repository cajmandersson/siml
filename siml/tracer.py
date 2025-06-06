from colorama import Fore, Style, init
init(autoreset=True)

from siml.ast_nodes import ASTNode

class Tracer: 
    enabled = False

    def __init__(self, section: str | None = None):
        self.section = section

    def info(self, message: str):
        if not self.enabled:
            return
        
        label = Fore.CYAN + "[INFO]" + Style.RESET_ALL
        section = f"{Fore.WHITE}[{self.section}]{Style.RESET_ALL} " if self.section else ""
        print(f"\n{label} {section} {message}")

    def debug(self, message: str):
        if not self.enabled:
            return
        
        label = Fore.YELLOW + "[DEBUG]" + Style.RESET_ALL
        section = f"{Fore.WHITE}[{self.section}]{Style.RESET_ALL} " if self.section else ""
        print(f"\n{label} {section} {message}")

    def warn(self, message: str):
        if not self.enabled:
            return
        
        label = Fore.MAGENTA + "[WARNING]" + Style.RESET_ALL
        section = f"{Fore.WHITE}[{self.section}]{Style.RESET_ALL} " if self.section else ""
        print(f"\n{label} {section} {message}")

    def failure(self, message: str):
        if not self.enabled:
            return
        
        label = Fore.RED + "[FAILURE]" + Style.RESET_ALL
        section = f"{Fore.WHITE}[{self.section}]{Style.RESET_ALL} " if self.section else ""
        print(f"\n{label} {section} {message}")

    def _render_ast(self, node: ASTNode, indent: str = "", is_last: bool = True) -> str:
        prefix = indent + ("└── " if is_last else "├── ")
        result = f"{prefix}{node.summary()}\n"

        children = node.get_children()
        for i, child in enumerate(children):
            is_last_child = (i == len(children) - 1) 
            next_indent = indent + ("    " if is_last else "│   ")
            result += self._render_ast(child, next_indent, is_last_child)

        return result
    
    def debug_ast(self, node: ASTNode):
        if not self.enabled:
            return 
        output = self._render_ast(node)
        print(Fore.MAGENTA + "[DEBUG AST]" + Style.RESET_ALL)
        print(output)


    
        
