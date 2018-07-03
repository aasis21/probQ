from ply import yacc
import probQlexer as lexer

tokens = lexer.tokens
precedence = (
    ('left', 'PLUS', 'MINUS'),
)

# A BASIC program is a series of statements.  We represent the program as a
# dictionary of tuples indexed by line number.

coin_entity = { 'entity': 'coin',
                'flags': {'flag': 'fair', 'action': 'flip'},
                'params': {'H': 0.5},
                'props': [{'head': {'prob': 0.5}, 'tail': {'prob': 13}}]
                }
dice_entity = { 'entity': 'dice',
                'flags': {'flag': 'fair', 'action': 'roll'},
                'params': {'O' : 1/6,'T': 1/6,'Th' : 1/6 , 'F': 1/6, 'Fv' : 1/6, 'S': 1/6},
                'props': [{'1': {'prob': 1/6 }, '2': {'prob': 1/6},'3': {'prob': 1/6 }, '4': {'prob': 1/6},'5': {'prob': 1/6 }, '6': {'prob': 1/6}}]
                }


_entities = {'coin' : coin_entity , 'dice' : dice_entity }
_alias_list = {}

def p_program(p):
    '''program : program statement
               | statement'''

    if len(p) == 3:
        p[0] = p[1].append(p[1])
    elif len(p) == 2:
        p[0] = [p[1]]

# This catch-all rule is used for any catastrophic errors.  In this case,
# we simply return nothing

# Format of all BASIC statements.

def p_statement(p):
    '''statement : statement entity '''
    p[0] = p[1].append(p[2])

def p_statement_single(p):
    '''statement : entity '''
    p[0] = [ p[1] ]

################################################################################
############################  ENTITY DEF   #####################################
################################################################################
def p_entity_def(p):
    ''' entity : ENTITY IDEN flag_action params entity_props '''
    p[0] = {'entity': p[2], 'flags': p[3] , 'params': p[4] , 'props' : p[5] }
    global _entities
    _entities = { **_entities, **{ (str(p[2]) + str(p[3]['flag'])) : p[0]} }


def p_entity_def_wo_flag_action(p):
    ''' entity : ENTITY IDEN params entity_props '''
    p[0] = {'entity': p[2], 'flags':{'flag':'def','action':'roll'}, 'params': p[3] , 'props' : p[4] }

def p_entity_def_wo_params(p):
    ''' entity : ENTITY IDEN flag_action entity_props '''
    p[0] = {'entity': p[2], 'flags': p[3], 'params': {} , 'props' : p[4] }


    ############ ---------------------------------------------------------------

def p_flag_action(p):
    ''' flag_action : LEFTSQRBRACKET FLAG ASSIGNMENT IDEN COMMA ROLL ASSIGNMENT IDEN RIGHTSQRBRACKET '''
    p[0] = {'flag' : p[4], 'action' : p[8]}

def p_flag_action_without_identifier(p):
    ''' flag_action : LEFTSQRBRACKET IDEN COMMA IDEN RIGHTSQRBRACKET '''
    p[0] = {'flag' : p[2], 'action' : p[4]}

def p_flag_action_with_flag(p):
    ''' flag_action : LEFTSQRBRACKET IDEN  RIGHTSQRBRACKET '''
    p[0] = {'flag' : p[2], 'action' : 'roll'}

     ############ --------------------------------------------------------------

def p_params(p):
    ''' params :  LEFTSMALLBRACKET alias_list RIGHTSMALLBRACKET '''
    p[0] = p[2]

def p_alias_list(p):
    ''' alias_list : alias_list COMMA ALIAS ASSIGNMENT FLOAT
                   | alias_list COMMA ALIAS
    '''
    size = len(p)
    if size == 6:
        ne = { p[3]:p[5] }
        p[0] = { **p[1], **ne }
    elif size == 4:
        ne = { p[3]: 0.0 }
        p[0] = { **p[1], **ne }


def p_alias_list_single(p):
    ''' alias_list : ALIAS ASSIGNMENT FLOAT
                   | ALIAS
    '''
    if len(p) == 4:
        p[0] = { p[1] : p[3]}
    elif len(p) == 2:
        p[0] = { p[1] : 0.0 }

    ############ ---------------------------------------------------------------

def p_entity_props(p):
    ''' entity_props : LEFTCURLYBRACE entity_props_inner RIGHTCURLYBRACE'''
    p[0] = p[2]

def p_entity_prop_inner(p):
    ''' entity_props_inner : entity_props_inner COMMA entity_prop
                           | entity_prop
    '''
    if len(p) == 3:
        p[1] += [p[2]]
        p[0] = p[1]

    elif len(p) == 2:
        p[0] = [p[1]]


def p_entity_prop(p):
    ''' entity_prop : entity_prop_prob
                    | entity_prop_num
    '''
    p[0] = p[1]

def p_entity_prop_num(p):
    ''' entity_prop_num : entity_prop_num SEMICOLON entity_prop_num_atom '''
    p[0] = { **p[1], **p[3]}

def p_entity_prop_num_single(p):
    ''' entity_prop_num : entity_prop_num_atom '''
    p[0] = p[1]

def p_entity_prop_num_atom(p):
    ''' entity_prop_num_atom : NUMBER COLON IDEN
                             | FLOAT COLON IDEN
                             | NUMBER COLON NUMBER
                             | FLOAT COLON NUMBER

    '''
    p[0] = {p[3] :  {'num' : p[1]} }

def p_entity_prop_brob(p):
    ''' entity_prop_prob : entity_prop_prob SEMICOLON entity_prop_prob_atom '''
    p[0] = { **p[1], **p[3]}

def p_entity_prop_prob_single(p):
    ''' entity_prop_prob : entity_prop_prob_atom '''
    p[0] = p[1]

def p_entity_prop_prob_atom(p):
    ''' entity_prop_prob_atom : NUMBER DOUBLECOLON IDEN
                             | FLOAT DOUBLECOLON IDEN
                             | NUMBER DOUBLECOLON NUMBER
                             | FLOAT DOUBLECOLON NUMBER
    '''
    p[0] = {p[3] : {'prob' : p[1]}}


    # to do add simple expr for prob.
    ############ ---------------------------------------------------------------

################################################################################
############################  ENTITY Initialize   ##############################
################################################################################


# Catastrophic error handler

probQparser = yacc.yacc()


def parse(data, debug=0):
    probQparser.error = 0
    p = probQparser.parse(data, debug=debug)
    if probQparser.error:
        return None
    return p

source = '''
entity dice[djfd,fjdk](H,K){ 12::dkfjjf;13::df }
'''
print(parse(source,0))


import pprint
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(_entities)
