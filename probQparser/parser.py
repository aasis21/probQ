from ply import yacc
import probQlexer.lexer as lexer
from collections import OrderedDict as odict
from probQsolver.solver import blackbox , QNode, in_order
import os
import sys
import time

tokens = lexer.tokens

solver = blackbox()

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'AND', 'OR', 'NOT')

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
    '''statement : entity_def '''
    p[0] = p[1]

def p_statement_entity_assignment(p):
    ''' statement : entity_action '''
    p[0] = p[1]

def p_statement_query(p):
    ''' statement : query_wrap '''
    p[0] = p[1]

################################################################################
############################  ENTITY DEF   #####################################
################################################################################
def p_entity_def(p):
    ''' entity_def : ENTITY IDEN ed_params ed_feature '''
    p[0] = {'entity': p[2], 'feature' : p[4] }
    solver.add_enitity(p[0])
    global _entities
    _entities = { **_entities, **{ str(p[2]) : p[0]} }


     ############ --------------------------------------------------------------

def p_ed_params(p):
    ''' ed_params :  LEFTSQRBRACKET alias_list RIGHTSQRBRACKET '''
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

def p_ed_feature(p):
    ''' ed_feature : LEFTSMALLBRACKET ed_feature_inner RIGHTSMALLBRACKET'''
    p[0] = p[2]

def p_ed_feature_inner(p):
    ''' ed_feature_inner : entity_prop_prob '''
    p[0] = p[1]

def p_entity_prop_prob(p):
    ''' entity_prop_prob : entity_prop_prob SEMICOLON entity_prop_prob_atom '''
    p[1].update(p[3])
    p[0] = p[1]

def p_entity_prop_prob_single(p):
    ''' entity_prop_prob : entity_prop_prob_atom '''
    p[0] = p[1]

def p_entity_prop_prob_atom(p):
    ''' entity_prop_prob_atom : ALIAS DOUBLECOLON IDEN
                             | ALIAS DOUBLECOLON NUMBER
    '''
    p[0] = odict([(p[3],p[1])])


    # to do add simple expr for prob.
    ############ ---------------------------------------------------------------

################################################################################
############################  ENTITY Initialize   ##############################
################################################################################
def p_entity_initialize(p):
    ''' entity_initialize : IDEN ei_params ei_number '''
    p[0]  = {'entity': p[1], 'label': p[2]['flag'], 'params': p[2]['params'] , 'number' : p[3] }

def p_empty(p):
    'empty :'
    pass


def p_ei_params(p):
    ''' ei_params : LEFTSMALLBRACKET  float_list ei_flag_option  RIGHTSMALLBRACKET '''
    p[0] = {'flag' : p[3], 'params': p[2]}

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

def p_ei_flag(p):
    ''' ei_flag_option : BAR IDEN
                        | empty
    '''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = "f"

def p_ei_number(p):
    ''' ei_number : LEFTCURLYBRACE NUMBER RIGHTCURLYBRACE '''
    p[0] = p[2]

################################################################################
############################     ENTITY Action    ##############################
################################################################################
# def p_entity_action(p):
#     ''' entity_action : ALIAS ASSIGNMENT ALIAS DOT ROLL LEFTSMALLBRACKET option_number RIGHTSMALLBRACKET
#     '''
#     p[0] = {'entity' : p[1], 'action' : p[3], 'num' : p[5]}

def p_entity_action_e(p):
    ''' entity_action : ALIAS ASSIGNMENT entity_initialize DOT ROLL LEFTSMALLBRACKET option_number RIGHTSMALLBRACKET '''
    entity_instance = p[3]
    solver.add_entity_instance(p[3])

    entity_action = {'alias' : p[1], 'instance': entity_instance }
    action_return = solver.add_entity_action(entity_action)

    _alias_list[p[1]] = { 'return' : action_return, 'length' : entity_instance['number'] , 'name' : p[1]}

    p[0] = {'entity' : p[1], 'action' : p[3], 'number' : p[5]}

def p_option_number(p):
    ''' option_number : NUMBER '''
    p[0] = p[1]

def p_option_number_wo(p):
    ''' option_number : empty '''
    p[0] = 1


################################################################################
############################     Probability  QUERY  ###########################
################################################################################


def p_query_wrap(p):
    ''' query_wrap : QUERY LEFTSMALLBRACKET q_expr RIGHTSMALLBRACKET '''
    #solver.add_query(p[3])
    print("bjdfjjdhjhjkjhjkhkjddfkdj")

    in_order(p[3])
    p[0] = p[3]

################################################################################

def p_q_expr(p):
    ''' q_expr : q_term_list OR q_term '''
    root = QNode("or","or")
    for e_ch in p[1]:
        root.add_child(e_ch)
    root.add_child(p[3])
    p[0] = root

def p_q_expr_s(p):
    ''' q_expr : q_term '''
    p[0] = p[1]

def p_q_term(p):
    ''' q_term : q_factor_list AND q_factor '''
    root = QNode("and","and")
    for e_ch in p[1]:
        root.add_child(e_ch)
    root.add_child(p[3])
    p[0] = root

def p_q_term_s(p):
    ''' q_term : q_factor '''
    p[0] = p[1]

def p_q_term_list(p):
    ''' q_term_list : q_term_list OR q_term '''
    p[0] = p[1] + [p[3]]

def p_q_term_list_s(p):
    ''' q_term_list : q_term '''

    p[0] = [p[1]]

def p_q_factor_a(p):
    ''' q_factor : q_atom '''
    p[0] = p[1]

def p_q_factor_n(p):
    ''' q_factor : NOT q_factor '''
    root = QNode("not","not")
    root.add_child(p[2])
    p[0] = root

def p_q_factor_e(p):
    ''' q_factor :  LEFTSMALLBRACKET q_expr RIGHTSMALLBRACKET '''
    p[0] = p[2]

def p_q_factor_list(p):
    ''' q_factor_list : q_factor_list AND q_factor '''
    p[0] = p[1] + [p[3]]

def p_q_factor_list_s(p):
    ''' q_factor_list : q_factor '''
    p[0] =  [p[1]]


def p_q_atom(p):
    ''' q_atom : q_equal_atom_3
               | q_equal_atom_2
               | me_atom
    '''
    p[0] = QNode("q_atom", p[1])

################################ Keep  adding new atom here ####################

def p_query_iden_3(p):
    ''' q_iden_3 : EQUALATMOST | EQUALATLEAST | EQUALFEW '''
    p[0] = p[1]

def p_query_iden_2(p):
    ''' q_iden_2 : EQUALALL | EQUALANY '''
    p[0] = p[1]


def p_q_equal_atom3(p):
    ''' q_equal_atom_3 : q_iden_3 LEFTSMALLBRACKET NUMBER COMMA q_alias_concat_wrap COMMA IDEN RIGHTSMALLBRACKET
                        | q_iden_3 LEFTSMALLBRACKET NUMBER COMMA q_alias_concat_wrap COMMA NUMBER RIGHTSMALLBRACKET
    '''
    alias = []
    for al in p[5]:
        alias += [_alias_list[al]]
    query_atom = {'construct' : p[1],'params_count' : 3 ,'number':p[3] , 'equal' : p[7],'alias_list' : alias}
    p[0] = query_atom

def p_q_equal_atom2(p):
    ''' q_equal_atom_2 : q_iden_2 LEFTSMALLBRACKET q_alias_concat_wrap COMMA IDEN RIGHTSMALLBRACKET
                        | q_iden_2 LEFTSMALLBRACKET q_alias_concat_wrap COMMA NUMBER RIGHTSMALLBRACKET
    '''
    alias = []
    for al in p[3]:
        alias += [_alias_list[al]]
    query_atom = {'construct' : p[1],'params_count' : 2 ,'number': 0 , 'equal' : p[5],'alias_list' : alias}
    p[0] = query_atom


def p_q_alias_concat_wrap(p):
    ''' q_alias_concat_wrap : ALIAS
                        | LEFTSQRBRACKET q_alias_concat RIGHTSQRBRACKET
    '''
    size = len(p)
    if size == 4:
        p[0] = p[2]
    elif size == 2:
        p[0] = [p[1]]


def p_q_alias_concat(p):
    ''' q_alias_concat : q_alias_concat BAR  ALIAS
                        | ALIAS
    '''
    size = len(p)
    if size == 4:
        p[1] += [p[3]]
        p[0] = p[1]
    elif size == 2:
        p[0] = [p[1]]

############################### ME :- constructer  :-  me_atom  ################
def me_atom(p):
    ''' me_atom : a_expression_atom '''
    res = {'type' : 'me', 'body': p[0]}

############################### ME :- a_expression_atom ########################
def p_a_expr_atom_e(p):
    ''' a_expression_atom : a_expression EQUAL a_expression '''
    p[0] = p[1] + ' =:= ' + p[3]

def p_a_expr_atom_ne(p):
    ''' a_expression_atom : a_expression NOTEQUAL a_expression '''
    p[0] = p[1] + ' =\= ' + p[3]

def p_a_expr_atom_ge(p):
    ''' a_expression_atom : a_expression GREATEREQUAL a_expression '''
    p[0] = p[1] + ' >= ' + p[3]

def p_a_expr_atom_g(p):
    ''' a_expression_atom : a_expression GREATER a_expression '''
    p[0] = p[1] + ' > ' + p[3]
def p_a_expr_atom_le(p):
    ''' a_expression_atom : a_expression LESSEQUAL a_expression '''
    p[0] = p[1] + ' =< ' + p[3]

def p_a_expr_atom_l(p):
    ''' a_expression_atom : a_expression LESS a_expression '''
    p[0] = p[1] + ' < ' + p[3]

def p_a_expression_plus(p):
    'a_expression : a_expression PLUS a_term'
    p[0] = str(p[1]) + ' + ' +  str(p[3])

def p_a_expression_minus(p):
    'a_expression : a_expression MINUS a_term'
    p[0] = str(p[1]) + ' - ' +  str(p[3])

def p_a_expression_term(p):
    'a_expression : a_term'
    p[0] = str(p[1])

def p_term_times(p):
    'a_term : a_term TIMES a_factor'
    p[0] = str(p[1]) + ' * ' +  str(p[3])

def p_term_div(p):
    'a_term : a_term DIVIDE a_factor'
    p[0] = str(p[1]) + ' / ' +  str(p[3])

def p_term_factor(p):
    'a_term : a_factor'
    p[0] = p[1]

def p_factor_num(p):
    ''' a_factor : NUMBER
              | ALIAS LEFTSQRBRACKET NUMBER LEFTSQRBRACKET
    '''
    if len(p) == 2:
        p[0] = str(p[1])
    if len(p) == 5:
        p[0] = str(p[1]) + str(p[3])

def p_factor_expr(p):
    'a_factor : LEFTSMALLBRACKET a_expression RIGHTSMALLBRACKET'
    p[0] = '( ' + str(p[2]) + ' )'

############################### ME END  ########################################

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")



# Catastrophic error handler

probQparser = yacc.yacc()


def parse(data, debug=0):
    probQparser.error = 0
    p = probQparser.parse(data, debug=debug)
    if probQparser.error:
        return None
    return p
