import re
template = '''%%template%%
class %%name%% {
    %%constructs%%
    std::variant< %%constructs_end%% > value_;
public:
    %%name%%() = default; 
    %%cons_func%%
    %%static_methods%% 
    %%is_methods%% 
    %%as_methods%% 
};

'''

class ClassTemplate:
    template = ""
    typenames = []
    typevariables=[]
    cpp_AST={}

    def __init__(self, node):
        self.typevariables = node['typevariables']
        self.name = node['name']
        self.constructs = node['constructs']
        self.template = template
        if len(self.typenames)>0:
            class_name = f'{self.name}<{",".join(self.typenames)}>'
        else:
            class_name = f'{self.name}'
        self.class_name =class_name

    def cppTemplate(self):
        #根据AST 替换生成cpp
        self.rep_templateline()
        self.template = re.sub(r'%%name%%', self.name, self.template)
        self.rep_cons_func()
        self.rep_constructs()
        self.rep_static_methods()
        self.rep_is_methods()
        self.rep_as_methods()
        # print(self.res)
        return self.template

    def rep_templateline(self):
        line = ""
        if len(self.typevariables) != 0:
            tnames = []
            for i, v in enumerate(self.typevariables):
                tnames.append(f'T{i + 1}')
            self.typenames = tnames

            line = "".join(['template<typename ', " ".join(tnames), ' >'])
        self.template = re.sub(r'%%template%%', line, template)


    def rep_cons_func(self):
        lines=[]
        for i, con in enumerate(self.constructs):
            con_name = con['name']
            lines.append(f"{self.name}(_{con_name} p) {{ value_ = p; }}")
        lines="\n   ".join(lines)
        print(lines)
        self.template=re.sub('%%cons_func%%',lines,self.template)

    def rep_constructs(self):
        # 替换constructs_end
        con_names = []
        for i, con in enumerate(self.constructs):
            con_names.append(con['name'])
        con_names_pre = list(map(lambda item: '_' + item, con_names))
        constructs_end = ", ".join(con_names_pre)
        self.template = re.sub(r"%%constructs_end%%", constructs_end, self.template)


        # 替换每个构造规则
        cons_lines = []
        for i, con in enumerate(self.constructs):
            params = con['params']
            con_name =con['name']
            if len(params) == 0:
                cons_line = f"struct _{con_name} {{}};"
                cons_lines.append(cons_line)
            else:
                lines = []
                for i, param in enumerate(params):
                    if param['type'] == 'TYPEVARIABLE':
                        x=self.typevariables.index(param['value'])
                        field_line = f'''T{x + 1} p{i + 1}_;'''
                        met_line = f'''const T{x + 1}& p{i + 1}() const {{ return p{i + 1}_; }}'''
                        lines.append(field_line)
                        lines.append(met_line)
                    elif param['type'] == 'SELF':
                        field_line = f'''std::shared_ptr<{self.class_name}>p{i + 1}_;'''
                        met_line = f'''{self.class_name} p{i + 1}() const {{ return *p{i + 1}_; }}'''
                        lines.append(field_line)
                        lines.append(met_line)
                    else:
                        raise RuntimeError("不支持其他自定义类型作为构造规则参数类型")
                lines="\n      ".join(lines)
                cons_line = f'''struct _{con_name} {{\n      {lines}   \n    }};'''
                cons_lines.append(cons_line)
        cons_lines = "\n    ".join(cons_lines)
        self.template = re.sub('%%constructs%%', cons_lines, self.template)

    def rep_static_methods(self):

        # 一轮一个cons
        static_methods = []
        for i, con in enumerate(self.constructs):
            params = con['params']
            cons_name = con['name']
            ps = []
            cs = []
            for i, param in enumerate(params):
                if param['type'] == 'TYPEVARIABLE':
                    x = self.typevariables.index(param['value'])
                    p = f'''T{x+ 1} p{i + 1}'''
                    ps.append(p)
                    c = f'p{i + 1}'
                    cs.append(c)
                else:
                    p = f'''{self.class_name} p{i + 1}'''
                    ps.append(p)
                    c = f'std::make_shared<{self.class_name}>(p{i + 1})'
                    cs.append(c)
            ps = ", ".join(ps)
            cs = ", ".join(cs)
            res = "static " + self.class_name+f" {cons_name}({ps}){{ return {self.class_name}{{  {'_' + cons_name}{{ {cs} }}   }};    }};"
            static_methods.append(res)
        static_methods = "\n    ".join(static_methods)
        # print(static_methods)
        self.template = re.sub('%%static_methods%%', static_methods, self.template)

    def rep_is_methods(self):
        is_methods=[]
        for i, con in enumerate(self.constructs):
            cons_name = con['name']
            res=f'bool is_{cons_name}() const {{ return std::holds_alternative<_{cons_name}>(value_); }}'
            is_methods.append(res)
        is_methods="\n    ".join(is_methods)
        self.template=re.sub('%%is_methods%%',is_methods,self.template)

    def rep_as_methods(self):
        as_methods=[]
        for i, con in enumerate(self.constructs):
            cons_name = con['name']
            res=f'const _{cons_name}&  as_{cons_name}() const {{ return std::get<_{cons_name}>(value_); }}'
            as_methods.append(res)
        as_methods="\n    ".join(as_methods)
        self.template=re.sub('%%as_methods%%',as_methods,self.template)
