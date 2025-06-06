from dataclasses import dataclass, field
from typing import Optional, Any, List, Union, Sequence

@dataclass
class DictEntry:
    key: str
    value: "ASTNode" # Use forward reference

@dataclass
class ASTNode:
    line: int 
    indent: int 
    meta: Optional[dict] = field(default_factory=dict, init=False)

    def __repr__(self):
        return f"{self.__class__.__name__}(line={self.line}, indent={self.indent})"
    
    def summary(self) -> str:
        return f"{self.__class__.__name__}(line={self.line})"
    
    def get_children(self) -> Sequence["ASTNode"]:
        return []

    
# Primitive Nodes
@dataclass
class StringNode(ASTNode):
    value: str = ""

    def summary(self):
        return f'StringNode("{self.value}")'


@dataclass
class NumberNode(ASTNode):
    value: Union[int, float] = 0

    def summary(self):
     return f"NumberNode({self.value})"


@dataclass
class BooleanNode(ASTNode):
    value: bool = False

@dataclass
class DictLiteralNode(ASTNode):
    entries: List[DictEntry] = field(default_factory=list)

    def get_children(self):
        return [entry.value for entry in self.entries]

@dataclass
class ListLiteralNode(ASTNode):
    elements: List[ASTNode] = field(default_factory=list)
    
    def get_children(self):
        return self.elements


# Conditional
@dataclass
class IfNode(ASTNode):
    condition: ASTNode
    then_body: List[ASTNode] = field(default_factory=list)
    else_body: List[ASTNode] = field(default_factory=list)

    def get_children(self):
        return [self.condition] + self.then_body + self.else_body

# Looping constructs
@dataclass
class ForNode(ASTNode):
    var: str
    iterable: ASTNode
    body: List[ASTNode] = field(default_factory=list)

    def get_children(self):
        return [self.iterable] + self.body


@dataclass
class NotNode(ASTNode):
    operand: ASTNode    

    def get_children(self):
        return [self.operand]
 

# Simulation root 
@dataclass
class SimulationNode(ASTNode):
    config: Optional[DictLiteralNode] = None
    agents: List["AgentNode"] = field(default_factory=list)
    modules: List["ModuleNode"] = field(default_factory=list)

    def get_children(self):
        children = []
        if self.config:
            children.append(self.config)
        
        return children + self.agents + self.modules

# Module definition
@dataclass
class ModuleNode(ASTNode):
    name: str
    state: List["StateVarNode"]
    actions: List["ActionNode"] = field(default_factory=list)
    rules: List["RuleNode"] = field(default_factory=list)
    templates: List["TemplateNode"] = field(default_factory=list)

    def get_children(self):
        return self.state + self.actions + self.rules + self.templates

@dataclass
class StateVarNode(ASTNode):
    name: str
    value: ASTNode # can be StringNode, NumberNode, DictLiteraNode, etc.

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, line={self.line})"
    
    def summary(self):
        return f"StateVarNode({self.name})"


    def get_children(self):
        return [self.value]

@dataclass 
class ActionNode(ASTNode):
    name:str 
    params: list[str] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)

    def get_children(self):
        return self.body

@dataclass
class RuleNode(ASTNode):
    trigger: str
    body: List[ASTNode] = field(default_factory=list) # e.g CallNode

    def get_children(self):
        return self.body

@dataclass 
class GenerateNode(ASTNode):
    template: str
    multiplier: Optional[ASTNode] = None # e.g NumberNode

    def get_children(self):
        return [self.multiplier] if self.multiplier else []

@dataclass
class AssignmentNode(ASTNode):
    target: str
    value: ASTNode

    def __repr__(self):
        return f"{self.__class__.__name__}(target={self.target}, line={self.line})"
    
    def summary(self):
        return f"AssignmentNode({self.target})"


    def get_children(self):
        return [self.value]

@dataclass
class CallArg:
    name: Optional[str]
    value: ASTNode 

@dataclass
class CallNode(ASTNode):
    function: str
    args: List[CallArg] = field(default_factory=list)

    def __repr__(self):
        args_repr = ", ".join(f"{arg.name}={arg.value}" if arg.name else str(arg.value) for arg in self.args)
        return f"{self.__class__.__name__}(function={self.function}, args=[{args_repr}], line={self.line})"

    def get_children(self):
        return [arg.value for arg in self.args]


@dataclass
class BinaryExprNode(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode

    def get_children(self):
        return [self.left, self.right]

@dataclass
class NullNode(ASTNode):
    def __repr__(self):
        return f"NullNode()"



@dataclass
class IdentifierNode(ASTNode):
    name: str 

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, line={self.line})"
    
    def summary(self):
        return f"IdentifierNode({self.name})"


@dataclass
class AgentNode(ASTNode):
    name: str                      # from `agent: ...`
    iterator_var: Optional[str]    # from `for each: var in iterable`
    iterable: Optional[str]        # parsed as a string for now
    llm_config: Optional[DictLiteralNode] = None
    context: Optional[DictLiteralNode] = None
    can_call: List[str] = field(default_factory=list)

    def get_children(self):
        children = []
        if self.llm_config:
            children.append(self.llm_config)
        if self.context:
            children.append(self.context)
        return children

    def summary(self):
        return f"AgentNode({self.name})"

@dataclass
class TemplateNode(ASTNode):
    name: str
    scema: ASTNode # e.g DictLiteralNode  or similar

    def get_children(self):
        return [self.scema]