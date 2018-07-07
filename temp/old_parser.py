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
    '''program : program statement '''
    p[1] += [p[2]] + ["@@@@@@@@@@@@@@@@@@@@@2"]
    p[0] = p[1]

def p_program_single(p):
    '''program : statement '''
    p[0] = [ p[1] ]




# Format of all BASIC statements.

def p_statement_entity_def(p):
    '''statement : entity '''
    p[0] = p[1]

def p_statement_entity_assignment(p):
    ''' statement : entity_assignment '''
    p[0] = p[1]

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
    ''' flag_action : LEFTSQRBRACKET FLAG ASSIGNMENT IDEN COMMA ACTION ASSIGNMENT IDEN RIGHTSQRBRACKET '''
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

def p_entity_prop_prob(p):
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
def p_entity_initialize(p):
    ''' entity_initialize : entity_name ei_flag ei_params ei_number '''
    p[0]  = {'entity': p[1], 'flags': p[2], 'info': p[3] , 'num' : p[4] }

def p_entity_name(p):
    ''' entity_name : IDEN '''
    p[0] = p[1]

def p_empty(p):
    'empty :'
    pass

######################-----------------------------------######################
def p_ei_flag(p):
    ''' ei_flag : LEFTSQRBRACKET IDEN RIGHTSQRBRACKET '''
    p[0] = p[2]

def p_ei_flag_empty(p):
    ''' ei_flag : empty '''
    p[0] = 'default'

######################-----------------------------------######################

def p_ei_params(p):
    ''' ei_params : LEFTSMALLBRACKET  float_list  RIGHTSMALLBRACKET
                 |  LEFTSMALLBRACKET entity_prop RIGHTSMALLBRACKET
    '''
    p[0] = p[2]
def p_ei_params_empty(p):
    ''' ei_params : empty '''
    p[0] = 'empty'

def p_float_list(p):
    ''' float_list :  float_list COMMA FLOAT
                    | float_list COMMA NUMBER
    '''
    p[1] += [p[3]]
    p[0] = p[1]

def p_float_list_single(p):
    ''' float_list : FLOAT
                   | NUMBER
    '''
    p[0] = [ p[1] ]

def p_ei_number(p):
    ''' ei_number : LEFTCURLYBRACE NUMBER RIGHTCURLYBRACE '''
    p[0] = p[2]

################################################################################
############################     ENTITY Action    ##############################
################################################################################
def p_entity_action(p):
    ''' entity_action : ALIAS DOT IDEN LEFTSMALLBRACKET option_number RIGHTSMALLBRACKET
                      | ALIAS DOT ROLL LEFTSMALLBRACKET option_number RIGHTSMALLBRACKET
    '''
    p[0] = {'entity' : p[1], 'action' : p[3], 'num' : p[5]}

def p_entity_action_e(p):
    ''' entity_action : entity_initialize DOT IDEN LEFTSMALLBRACKET option_number RIGHTSMALLBRACKET
                      | entity_initialize DOT ROLL LEFTSMALLBRACKET option_number RIGHTSMALLBRACKET

     '''
    p[0] = {'entity' : p[1], 'action' : p[3], 'num' : p[5]}

def p_option_number(p):
    ''' option_number : NUMBER '''
    p[0] = p[1]

def p_option_number_wo(p):
    ''' option_number : empty '''
    p[0] = 1


################################################################################
############################     ENTITY Assignment    ##########################
################################################################################

def p_entity_assignment(p):
    ''' entity_assignment : ALIAS ASSIGNMENT entity_initialize
                          | ALIAS ASSIGNMENT entity_action
    '''
    global _alias_list
    _alias_list[p[1]] = p[3]
    p[0] = {p[1] : p[3] }

# Catastrophic error handler

probQparser = yacc.yacc()


def parse(data, debug=0):
    probQparser.error = 0
    p = probQparser.parse(data, debug=debug)
    if probQparser.error:
        return None
    return p

source = '''
entity dice[flag=fair, action=rollu](H,T){
	H ::1; 0.16::2; 0.16::3; 0.16::4; 0.16::5; 0.16::6
}
X = dice[fair]{5}
Y = X.roll(5)
X = dice[fair]{5}
Y = X.roll(5)
'''
print(parse(source,1))


# import pprint
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(_entities)
