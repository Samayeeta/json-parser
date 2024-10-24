import re

def tokenize(json_str):
    token_specification = [
        ('STRING', r'"(.*?)"'),   
        ('NUMBER', r'-?\d+(\.\d+)?'), 
        ('TRUE', r'true'), 
        ('FALSE', r'false'),  
        ('NULL', r'null'),   
        ('LBRACE', r'\{'), 
        ('RBRACE', r'\}'), 
        ('LBRACKET', r'\['), 
        ('RBRACKET', r'\]'), 
        ('COLON', r':'),  
        ('COMMA', r','),  
        ('WS', r'\s+'),  
    ]
    
    tokens = []
    token_re = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    for mo in re.finditer(token_re, json_str):
        kind = mo.lastgroup
        value = mo.group(kind)
        if kind != 'WS': 
            tokens.append((kind, value))
    return tokens

def parse(json_str):
    tokens = tokenize(json_str)
    if not tokens:
        raise ValueError("Empty JSON input.")
    
    def parse_object(index):
        if tokens[index][0] == 'LBRACE':
            index += 1
            obj = {}
            while tokens[index][0] != 'RBRACE':
                key_token = tokens[index]
                if key_token[0] != 'STRING':
                    raise ValueError("Invalid key.")
                key = key_token[1]
                index += 1
                if tokens[index][0] != 'COLON':
                    raise ValueError("Expected ':' after key.")
                index += 1
                value_token = tokens[index]
                
                if value_token[0] == 'STRING':
                    value = value_token[1]
                elif value_token[0] == 'NUMBER':
                    value = float(value_token[1]) if '.' in value_token[1] else int(value_token[1])
                elif value_token[0] == 'TRUE':
                    value = True
                elif value_token[0] == 'FALSE':
                    value = False
                elif value_token[0] == 'NULL':
                    value = None
                elif value_token[0] == 'LBRACE':
                    value, index = parse_object(index)
                elif value_token[0] == 'LBRACKET': 
                    value, index = parse_array(index)
                else:
                    raise ValueError("Unexpected value.")
                obj[key] = value
                index += 1
                if tokens[index][0] == 'COMMA':
                    index += 1
            if tokens[index][0] != 'RBRACE':
                raise ValueError("Expected '}' at the end of the object.")
            return obj, index + 1  
        raise ValueError("Invalid JSON object.")

    def parse_array(index):
        if tokens[index][0] == 'LBRACKET':
            index += 1
            arr = []
            while tokens[index][0] != 'RBRACKET':
                value_token = tokens[index]
                if value_token[0] == 'STRING':
                    value = value_token[1]
                elif value_token[0] == 'NUMBER':
                    value = float(value_token[1]) if '.' in value_token[1] else int(value_token[1])
                elif value_token[0] == 'TRUE':
                    value = True
                elif value_token[0] == 'FALSE':
                    value = False
                elif value_token[0] == 'NULL':
                    value = None
                elif value_token[0] == 'LBRACE':  
                    value, index = parse_object(index)
                elif value_token[0] == 'LBRACKET':  
                    value, index = parse_array(index)
                else:
                    raise ValueError("Unexpected value.")
                arr.append(value)
                index += 1
                if tokens[index][0] == 'COMMA':
                    index += 1
            if tokens[index][0] != 'RBRACKET':
                raise ValueError("Expected ']' at the end of the array.")
            return arr, index + 1  
        raise ValueError("Invalid JSON array.")

    result, _ = parse_object(0)
    return result