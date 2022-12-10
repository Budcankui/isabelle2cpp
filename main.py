import ply.lex as lex
import re
import json
import os
import template


class MyLexer:
    # 处理保留字
    reserved = {
        'if': 'IF',
        'else': 'ELSE',
        'then': 'THEN',
        'datatype': 'DATATYPE',
        'fun': 'FUN',
        'value': 'VALUE',
        'where': 'WHERE',
        'begin': "BEGIN"
    }
    tokens = [
                 'NUMBER',
                 'ID',
                 'special_word',
                 'error_word',
                 'DQOUTE',
                 'DCOLON',
                 'RE',
                 'OR',
                 'TYPEVARIABLE',
                 'PLUS',
                 'MINUS',
                 'TIMES',
                 'DIVIDE',
                 'LPAREN',
                 'RPAREN',
                 'EQUAL',
                 'COMMA',
             ] + list(reserved.values())
    t_DQOUTE = r'"'
    t_DCOLON = r'::'
    t_RE = r'⇒'
    t_OR = r'\|'
    t_TYPEVARIABLE = "'[a-zA-Z_][a-zA-Z_0-9]*"
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_EQUAL = r'='
    t_COMMA = r','
    # t_special_word = r'|:|\'|=|\[|\]'
    t_ignore = ' \t'

    def __init__(self):
        self.lexer = lex.lex(module=self)

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'ID')  # Check for reserved words
        return t

    def t_error_word(self, t):
        r'[0-9]+[a-zA-Z_]+'
        print("Illegal character '%s',location:('%d', '%d')" % (t.value, t.lexer.lineno, self.find_column(data, t)))
        t.lexer.skip(1)

    def t_error(self, t):
        print("Illegal character '%s',location:('%d', '%d')" % (t.value[0], t.lexer.lineno, self.find_column(data, t)))
        t.lexer.skip(1)

    def t_NUMBER(self, t):
        r'[0-9]+'
        t.value = int(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def find_column(self, input, token):
        line_start = input.rfind('\n', 0, token.lexpos) + 1
        print('start = ', line_start, ' end = ', token.lexpos)
        return (token.lexpos - line_start) + 1

    def readThy(self, file):
        with open(file, mode="r", encoding="utf-8") as f:
            lines = f.readlines()
        # 删除空行
        lines = filter(lambda line: line != "\n", lines)
        # 删除theory imports end 行
        lines = [line for line in lines
                 if re.match(r".*theory.*", line) is None
                 and re.match(r".*imports.*", line) is None
                 and re.match(r".*end.*", line) is None
                 and re.match(r".*begin.*", line) is None
                 ]
        thy = "".join(lines)
        self.thy = thy
        return thy

    def getTokens(self):
        lexer = self.lexer
        lexer.input(self.thy)
        tokens = []
        # 格式转变
        while True:
            tok = lexer.token()
            if not tok:
                break
            t = tok.__str__()
            # print(t)
            if t.find("LexToken") != -1:
                t = t.replace("LexToken(", "").replace(")", "").split(",")
                t[1] = t[1][1:-1]
                if t[0] == "DQOUTE":
                    t[1] = '\"'
            # 可以注释掉，返回数组
            # t = {"type": t[0], "value": t[1], "row": t[2], "col": t[3]}
            t = {"type": t[0], "value": t[1]}
            tokens.append(t)
        # 去掉无用的双引号
        tokens = self.delRedundantDuoute(tokens)
        return tokens

    # 去掉无用的双引号 ,即双引号之间只有一个token
    def delRedundantDuoute(self, tokens):
        indexs = []
        for i, tok in enumerate(tokens):
            if tok['type'] == 'DQOUTE':
                indexs.append(i)
        # 双引号个数一定为偶数
        if len(indexs) % 2 != 0:
            raise RuntimeError("双引号个数是奇数")
        delIndexs = []
        for i in range(0, len(indexs), 2):
            if indexs[i + 1] - indexs[i] == 2:
                delIndexs.append(indexs[i])
                delIndexs.append(indexs[i + 1])
        tokens = [tok for i, tok in enumerate(tokens) if i not in delIndexs]
        return tokens


class MyParse:
    current = 0
    tokens = []
    tok = {}

    def __init__(self, tokens):
        self.current = 0
        self.tokens = tokens
        self.tok = tokens[self.current]

    def parse(self):
        AST = {
            "type": "thy",
            "body": []
        }
        tokens = self.classifyTokens()
        if tokens == None:
            return AST
        for toks in tokens:
            # print(toks)
            AST['body'].append(self.getASTBody(toks))
        # while self.current < len(tokens):
        #     AST['body'].append(self.walk())
        return AST

    def classifyTokens(self):
        tokens = self.tokens
        # 按函数 类型 value tokens分组
        indexs = []
        for i, tok in enumerate(tokens):
            type = tok['type']
            if type == 'DATATYPE' or type == 'FUN' or type == 'VALUE':
                indexs.append(i)
        if len(indexs) == 0:
            return
        indexs.append(len(tokens))
        list = []
        for i in range(len(indexs)):
            if i + 1 < len(indexs):
                a = indexs[i]
                b = indexs[i + 1]
                list.append(tokens[a:b])
        self.tokens = list
        # print("------------")
        # for a in list:
        #     print(a)
        return self.tokens

    def getASTBody(self, toks):
        tok = toks[0]
        if tok['type'] == 'DATATYPE':
            child_ast = self.ast_datatype(toks)
            return child_ast
        if tok['type'] == 'FUNC':
            pass

    def ast_datatype(self, toks):
        node = {'type': 'DATATYPE', 'name': None}
        # 找等号
        delimiter = -1
        for i, tok in enumerate(toks):
            if tok['type'] == 'EQUAL':
                delimiter = i
        assert delimiter != -1
        # 等号左边tokens
        ltoks = toks[0:delimiter]
        rtoks = toks[delimiter + 1:]
        node = self.ast_datatype_ltoks(ltoks, node)
        node = self.ast_datatype_rtoks(rtoks, node)
        return node

    def ast_datatype_ltoks(self, toks, node):
        typevariables = []
        name = ""
        for tok in toks:
            if tok['type'] == 'TYPEVARIABLE':
                typevariables.append(tok['value'])
            if tok['type'] == 'ID':
                name = tok['value']
        node['typevariables'] = typevariables
        node['name'] = name
        return node

    def ast_datatype_rtoks(self, toks, node):
        # 获取每一组构造规则的tokens
        # 以 | 分割rtoks
        list = []
        indexs = []
        # 头和尾部插入 | ,方便处理
        toks.insert(0, {'type': 'OR', 'value': '|'})
        toks.append({'type': 'OR', 'value': '|'})
        # print(toks)
        for i, tok in enumerate(toks):
            if tok['type'] == "OR":
                indexs.append(i)
        for i in range(len(indexs)):
            if i + 1 < len(indexs):
                a = indexs[i]
                b = indexs[i + 1]
                list.append(toks[a + 1:b])
        # 解析每一条构造规则
        constructs = []
        for constoks in list:
            cons = self.ast_datatype_constructs(constoks, node)
            constructs.append(cons)
        node['constructs'] = constructs
        return node

    def ast_datatype_constructs(self, toks, node):
        # print(toks)
        # 获得当前构造规则名称
        name = toks[0]['value']
        params = []
        # 如果参数为空
        if len(toks) == 1:
            return {'name': name, 'params': params}
        # 解析参数类型
        toks.pop(0)
        # 查出双引号下标
        dqoute_idxs = []
        for i, tok in enumerate(toks):
            if tok['type'] == 'DQOUTE':
                dqoute_idxs.append(i)
        assert len(dqoute_idxs) % 2 == 0
        dqoute_idxs = [(dqoute_idxs[i], dqoute_idxs[i + 1]) for i in range(0, len(dqoute_idxs), 2)]
        # 所有双引号及之间下标 不包括一对双引号右边的的那个
        idxs = []
        for i in dqoute_idxs:
            idxs.extend(range(i[0], i[1]))
        toks = [tok for i, tok in enumerate(toks) if i not in idxs]
        # 一个DQOUTE相当于一个递归定义类型的参数
        for i, tok in enumerate(toks):
            if tok['type'] == 'TYPEVARIABLE':
                params.append({'type': 'TYPEVARIABLE', 'value': tok['value']})
            if tok['type'] == 'DQOUTE':
                params.append({'type': 'SELF', 'value': 'self'})
            if tok['type'] == 'ID':
                params.append({'type': 'SELF', 'value': 'self'})
        # print(toks)
        # print("p",params)
        cons = {'name': name, 'params': params}
        return cons


class Generator:
    def __init__(self, AST):
        self.AST = AST

    def generate(self, file):
        # 创建并清空文件
        with open(file=file, mode='w+', encoding='utf-8') as f:
            f.write('')
        AST_CPP_dattype = []
        #'DATATYPE'
        for node in self.AST['body']:
            if node == None:
                continue
            #类型的cpp代码生成'

            if node['type'] == 'DATATYPE':
                ct = template.ClassTemplate(node)
                ct_cpp = ct.cppTemplate()
                AST_CPP_dattype.append(ct.cpp_AST)
                with open(file=file, mode='a+', encoding='utf-8') as f:
                    f.write(ct_cpp + os.linesep)

        # 'FUN'
        for node in self.AST['body']:
            if node == None:
                continue
            #类型的cpp代码生成
            if node['type'] == 'FUN':
                # AST_CPP_dattype
               pass

        return


if __name__ == '__main__':
    #解析单词 token
    mylexer = MyLexer()
    mylexer.readThy("a.thy")
    tokens = mylexer.getTokens()
    for tok in tokens:
        print(tok["type"],tok['value'])

    # 解析句法 获得语法数AST
    parser = MyParse(tokens)
    AST = parser.parse()

    #把AST字典转化成格式化后的json 跟解析无关
    jsonAST = json.dumps(AST, indent=2)
    with open(file="AST.json", mode="w+", encoding='utf-8') as f:
        json.dump(AST, f, indent=2)
    print(jsonAST)

    #用AST生成cpp代码
    generator = Generator(AST)
    generator.generate('a.cpp')
