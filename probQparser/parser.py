from ply import yacc
import os,sys,time

from collections import OrderedDict as odict
from probQlexer.lexer import lexer
from probQlexer.lexer import tokens as lexTokens
from probQsolver.solver import blackbox , QNode

tokens = lexTokens

solver = blackbox()

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'AND', 'OR', 'NOT')

)

# A BASIC program is a series of statements.  We represent the program as a
# dictionary of tuples indexed by line number.

_entity = {
    'dice' : {'entity': 'dice' , 'feature' : odict([(1,0.16666666666),(2,0.16666666666),(3,0.16666666666),(4,0.16666666666),(5,0.16666666666),(6,0.16666666666)]),
              'p_default': [0.16666666666,0.16666666666,0.16666666666,0.16666666666,0.16666666666,0.16666666666] },
    'coin' : {'entity': 'coin' , 'feature' : odict([('head',0.5),('tail',0.5)]),
              'p_default': [0.5,0.5] }
}
_alias = {}

_bucket = {}


def p_program(p):
    '''program : program statement '''
    p[1] += [p[2]]
    p[0] = p[1]

def p_program_single(p):
    '''program : statement '''
    p[0] = [ p[1] ]


# Format of all BASIC statements.

def p_statement_entity_def(p):
    '''statement : entity_def '''
    p[0] = p[1]

def p_statement_entity_instance(p):
    ''' statement : entity_instance_wrap '''
    p[0] = p[1]

def p_statement_entity_assignment(p):
    ''' statement : entity_action '''
    p[0] = p[1]

def p_statement_query(p):
    ''' statement : query_wrap '''
    p[0] = p[1]

def p_statement_b(p):
    ''' statement : bucket_def '''
    p[0] = p[1]

def p_statement_b_action(p):
    ''' statement : bucket_action '''
    p[0] = p[1]
################################################################################
############################     HELPERS   #####################################
################################################################################

def p_empty(p):
    'empty :'
    pass



################################################################################
############################  ENTITY DEF   #####################################
################################################################################

def p_entity_def(p):
    ''' entity_def : ENTITY IDEN ed_feature '''
    feature = p[3]['feature']
    default = []
    for key, value in feature.items():
        default.append(value)

    p[0] = {'entity': p[2], 'feature' : p[3]['feature'],'p_default': default }
    if float(p[3]['sum']) > 1:
        print("WARNING: Sum of probability greater than one! ", p.lineno(3))
    if p[2] in _entity:
        print("This entity is already defined, this will be rejected")
    else:
        solver.add_enitity(p[0])
        _entity[p[2]] =  p[0]


def p_ed_feature(p):
    ''' ed_feature : LEFTSMALLBRACKET ed_feature_inner RIGHTSMALLBRACKET'''
    p[0] = p[2]

def p_ed_feature_inner(p):
    ''' ed_feature_inner : entity_prop_prob '''
    p[0] = p[1]

def p_entity_prop_prob(p):
    ''' entity_prop_prob : entity_prop_prob SEMICOLON entity_prop_prob_atom '''
    p[1]['feature'].update(p[3]['feature'])
    p[1]['sum'] = float(p[1]['sum']) + float(p[3]['sum'])
    p[0] = p[1]

def p_entity_prop_prob_single(p):
    ''' entity_prop_prob : entity_prop_prob_atom '''
    p[0] = p[1]

def p_entity_prop_prob_atom(p):
    ''' entity_prop_prob_atom : IDEN
                             | NUMBER
    '''
    p[0] = { 'feature' : odict([(p[1],0)]) , 'sum' : 0 }

def p_entity_prop_prob_atom_n(p):
    ''' entity_prop_prob_atom : NUMBER DOUBLECOLON IDEN
                             | NUMBER DOUBLECOLON NUMBER
    '''
    p[0] = { 'feature' : odict([(p[3],p[1])]), 'sum' : p[1] }

def p_entity_prop_prob_atom_f(p):
    ''' entity_prop_prob_atom : FLOAT DOUBLECOLON IDEN
                             | FLOAT DOUBLECOLON NUMBER
    '''
    p[0] = { 'feature' : odict([(p[3],p[1])]), 'sum' : p[1] }


################################################################################
############################  ENTITY instance   ################################
################################################################################
def p_entity_instance_wrap(p):
    ''' entity_instance_wrap : ALIAS ASSIGNMENT entity_instance '''
    alias = {'id': p[1], 'type' : 'entity_instance', 'instance': p[3]}
    if p[1] in _alias:
        print("Alias already exist", p.lineno(1))
    else:
        p[3]['label'] = str(p[1]).lower()
        solver.add_entity_instance(p[3])
        _alias[p[1]] = alias

def p_entity_instance(p):
    ''' entity_instance : IDEN ei_params ei_number '''
    if p[1] in _entity:
        entity = _entity[p[1]]
        e_p_length = len(entity['p_default'])
        if p[2]['flag'] == 'empty':
            e_param = entity['p_default']
        elif len(p[2]['params'])== e_p_length:
            e_param = p[2]['params']
        else:
            print("Pass all the required parameters")

        p[0]  = {'type':'entity_instance', 'entity': p[1], 'label': p[2]['flag'], 'params': e_param , 'count' : p[3] }

    else:
        print(_entity)
        print("entity not defined")

def p_entity_repr(p):
    ''' entity_repr : IDEN ei_params_n '''
    p[0] = '{}('.format(p[1])
    for param in p[2]['params']:
        p[0] += '{}, '.format(param)
    p[0] = p[0].strip(', ') + ')'

def p_ei_params(p):
    ''' ei_params : LEFTSMALLBRACKET  float_list ei_flag_option  RIGHTSMALLBRACKET '''
    p[0] = {'flag' : p[3], 'params': p[2]}

def p_ei_params_n(p):
    ''' ei_params_n : LEFTSMALLBRACKET  float_list ei_flag_option  RIGHTSMALLBRACKET '''
    p[0] = {'flag' : p[3], 'params': p[2]}

def p_ei_params_n_e(p):
    ''' ei_params_n : LEFTSMALLBRACKET   RIGHTSMALLBRACKET '''
    p[0] = {'flag' : 'empty', 'params': []}

def p_ei_params_empty(p):
    ''' ei_params : empty '''
    p[0] = {'flag':'empty', 'params' : [] }

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
def p_entity_action(p):
    ''' entity_action : ALIAS ASSIGNMENT ALIAS DOT ROLL LEFTSMALLBRACKET option_number RIGHTSMALLBRACKET
    '''
    if p[1] in _alias:
        print("Alias already exist", p.lineno(1))
        exit()
    else:
        if p[3] in _alias and _alias[p[3]]['type'] == 'entity_instance':
            entity_instance = _alias[p[3]]['instance']

            entity_action = {'action_alias' : p[1], 'entity_instance': entity_instance }
            action_return = solver.add_entity_action(entity_action)

            _alias[p[1]] = { 'id':p[1],'type' : 'entity_action','return' : action_return,
                            'length' : entity_instance['count'],'instance': entity_instance}
        elif p[3] in _alias and _alias[p[3]]['type'] == 'bucket_action':
            bucket_pick = _alias[p[3]]
            bucket_roll_action =  {'action_alias' : p[1], 'bucket_pick': bucket_pick }
            solver.add_bucket_picked_roll(bucket_roll_action)
            bucket_pick['roll_overload'] = 1



        else:
            print("wrong alias",p.lineno(3))


def p_entity_action_e(p):
    ''' entity_action : ALIAS ASSIGNMENT entity_instance DOT ROLL LEFTSMALLBRACKET option_number RIGHTSMALLBRACKET '''
    if p[1] in _alias:
        print("Alias already exist", p.lineno(1))
    else:
        p[3]['label'] = str(p[1]).lower()
        entity_instance = p[3]
        solver.add_entity_instance(p[3])

        entity_action = {'action_alias' : p[1], 'entity_instance': entity_instance }
        action_return = solver.add_entity_action(entity_action)

        _alias[p[1]] = { 'id':p[1],'type':'entity_action','return' : action_return,
                        'length' : entity_instance['count'],'instance': entity_instance}

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
    solver.add_query(p[3])


    #in_order(p[3])
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



def p_q_equal_atom3(p):
    ''' q_equal_atom_3 : q_iden_3 LEFTSMALLBRACKET NUMBER COMMA q_alias_concat_wrap COMMA IDEN RIGHTSMALLBRACKET
                        | q_iden_3 LEFTSMALLBRACKET NUMBER COMMA q_alias_concat_wrap COMMA NUMBER RIGHTSMALLBRACKET
                        | q_iden_3 LEFTSMALLBRACKET NUMBER COMMA q_alias_concat_wrap COMMA entity_repr RIGHTSMALLBRACKET
                        | q_iden_3 LEFTSMALLBRACKET NUMBER COMMA q_alias_concat_wrap COMMA atom_repr RIGHTSMALLBRACKET

    '''

    query_atom = {'construct' : p[1],'params_count' : 3 ,'number':p[3] , 'equal' : p[7],
                  'alias_list' : p[5]['alias_list'],
                  'list' : p[5]['list'] ,
                  'list_len' : p[5]['list_len']
                  }
    p[0] = {'type': 'nl', 'body' :query_atom}

def p_q_equal_atom2(p):
    ''' q_equal_atom_2 : q_iden_2 LEFTSMALLBRACKET q_alias_concat_wrap COMMA IDEN RIGHTSMALLBRACKET
                        | q_iden_2 LEFTSMALLBRACKET q_alias_concat_wrap COMMA NUMBER RIGHTSMALLBRACKET
                        | q_iden_2 LEFTSMALLBRACKET q_alias_concat_wrap COMMA entity_repr RIGHTSMALLBRACKET
                        | q_iden_2 LEFTSMALLBRACKET q_alias_concat_wrap COMMA atom_repr RIGHTSMALLBRACKET
    '''
    query_atom = {'construct' : p[1],'params_count' : 2 ,'number': 0 , 'equal' : p[5],
                  'alias_list' : p[3]['alias_list'],
                  'list' : p[3]['list'] ,
                  'list_len' : p[3]['list_len']
                  }
    p[0] = {'type': 'nl', 'body' :query_atom}


def p_query_iden_3(p):
    ''' q_iden_3 : EQUALATMOST
                | EQUALATLEAST
                | EQUALFEW '''
    p[0] = p[1]

def p_query_iden_2(p):
    ''' q_iden_2 : EQUALALL
                | EQUALANY '''
    p[0] = p[1]


def p_q_alias_concat_wrap(p):
    ''' q_alias_concat_wrap : alias_slice
                        | LEFTSQRBRACKET q_alias_concat RIGHTSQRBRACKET
    '''
    size = len(p)
    if size == 4:
        p[0] = p[2]
    elif size == 2:
        p[0] = {'list': p[1]['list'], 'alias_list' : [p[1]['name']], 'list_len' : p[1]['len'] }


def p_q_alias_concat(p):
    ''' q_alias_concat : q_alias_concat BAR  alias_slice
                        | alias_slice
    '''
    size = len(p)
    if size == 4:
        l = p[1]['list'] + ' , ' + p[3]['list']
        a_list = p[1]['alias_list'] + [p[3]['name']]
        a_len = p[1]['list_len'] + p[3]['len']
        p[0] = {'list': l , 'alias_list' : a_list, 'list_len': a_len }

    elif size == 2:
        p[0] = {'list': p[1]['list'], 'alias_list' : [p[1]['name']], 'list_len' : p[1]['len']  }


def p_alias_slice(p):
    ''' alias_slice : ALIAS
                    | ALIAS LEFTSQRBRACKET NUMBER COLON NUMBER RIGHTSQRBRACKET'''
    alias = _alias[p[1]]
    a_name = str(p[1])
    if len(p) == 2:
        res = ''
        a_len = alias['length']
        for i in range(1, a_len+1 ):
            res = res + a_name + str(i) + ', '
    if len(p) == 7:
        res = ''
        a_len = int(p[5]) - int(p[3]) + 1
        for i in range(p[3], p[5] ):
            res = res + a_name + str(i) + ', '

    res = res.strip(', ')
    p[0] = {'list' : res, 'name' : a_name, 'len' : a_len }



############################### ME :- constructer  :-  me_atom  ################
def p_me_atom(p):
    ''' me_atom : a_expression_atom
                | s_expr_atom
    '''
    res = {'type' : 'me', 'body': p[1]}
    p[0] = res

def p_string_expr_atom(p):
    ''' s_expr_atom : ALIAS LEFTSQRBRACKET NUMBER RIGHTSQRBRACKET ASSIGNMENT IDEN '''
    p[0] = str(p[1]) + str(p[3]) + ' == ' + str(p[6])

############################### ME :- a_expression_atom ########################
def p_a_expr_atom_e(p):
    ''' a_expression_atom : a_expression EQUAL a_expression '''
    if p[3].startswith('$$$$'):
        p[0] = p[1] + ' == ' + p[3][4:]
    else:
        p[0] = p[1] + ' =:= ' + p[3]


def p_a_expr_atom_ne(p):
    ''' a_expression_atom : a_expression NOTEQUAL a_expression '''
    if p[3].startswith('$$$$'):
        p[0] = p[1] + ' \= ' + p[3][4:]
    else:
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
    ''' a_term : a_factor '''
    p[0] = p[1]

def p_factor_iden(p):
    ''' a_factor : IDEN
                | atom_repr
                | entity_repr
    '''
    p[0] = '$$$$' + str(p[1])
    print(p[0])

def p_factor_num(p):
    ''' a_factor : NUMBER
              | ALIAS LEFTSQRBRACKET NUMBER RIGHTSQRBRACKET
    '''
    if len(p) == 2:
        p[0] = str(p[1])
    if len(p) == 5:
        p[0] = str(p[1]) + str(p[3])

def p_factor_expr(p):
    'a_factor : LEFTSMALLBRACKET a_expression RIGHTSMALLBRACKET'
    p[0] = '( ' + str(p[2]) + ' )'


############################### ME END  ########################################

################################################################################
############################        BUCKET DEF       ###########################
################################################################################

def p_bucket_def(p):
    ''' bucket_def : BUCKET IDEN LEFTSMALLBRACKET bucket_item_list RIGHTSMALLBRACKET'''
    p[0] = {'bucket' : p[2], 'instances': p[4]['instances'], 'size': p[4]['size'], 'nr_state': 0, 'r_state': 0}
    _bucket[p[2]] = p[0]
    solver.add_bucket_def(p[0])
    print(p[0])

def p_bucket_item_list_entity(p):
    ''' bucket_item_list : bucket_item_list COMMA entity_instance
                             | entity_instance
    '''
    if len(p)==4:
        p[1]['instances'] += [p[3]]
        p[0] = {'instances' : p[1]['instances'], 'size' : p[1]['size'] + p[3]['count'] }

    if len(p)==2:
        p[0] = {'instances': [p[1]], 'size' : p[1]['count'] }

def p_bucket_item_list_atom(p):
    ''' bucket_item_list : bucket_item_list COMMA atom
                             | atom
    '''
    if len(p)==4:
        p[1]['instances'] += [p[3]]
        p[0] = {'instances' : p[1]['instances'], 'size' : p[1]['size'] + p[3]['count'] }

    if len(p)==2:
        p[0] = {'instances': [p[1]], 'size' : p[1]['count'] }

def p_atom(p):
    ''' atom : IDEN  LEFTCURLYBRACE NUMBER RIGHTCURLYBRACE '''
    if p[1] in _entity:
        entity = _entity[p[1]]
        p[0]  = {'type':'entity_instance', 'entity': p[1], 'label': 'default', 'params': entity['p_default'] , 'count' : p[3] }

    else:
        p[0] = {'count': p[3], 'type': 'atom' , 'name': p[1] }

def p_atom_wf(p):
    ''' atom : atom_repr LEFTCURLYBRACE NUMBER RIGHTCURLYBRACE '''
    p[0] = {'count': p[3], 'type': 'atom' , 'name': p[1] }

def p_atom_repr(p):
    ''' atom_repr : IDEN LEFTSMALLBRACKET IDEN RIGHTSMALLBRACKET
                    | IDEN LEFTSMALLBRACKET NUMBER RIGHTSMALLBRACKET
    '''
    p[0] = '{}({})'.format(p[1],p[3])

################################################################################
############################        BUCKET ACTION      #########################
################################################################################

def p_bucket_action(p):
    ''' bucket_action : ALIAS ASSIGNMENT IDEN DOT PICK LEFTSMALLBRACKET NUMBER COMMA IDEN RIGHTSMALLBRACKET '''
    if not (p[9] == 'nr' or p[9] == 'r'):
        print("PLEASE GIVE CORRECT MODE ")
        exit()

    if p[1] in _alias:
        print("Alias already exist", p.lineno(1))
        exit()
    else:
        if p[3] in _bucket :
            bucket = _bucket[p[3]]

            bucket_action = {'action_alias' : p[1], 'bucket': bucket, 'pick_type' : p[9], 'pick_count': p[7] }
            solver.add_bucket_action(bucket_action)

            print(bucket)
            if str(p[9]) == 'nr':
                bucket['nr_state'] = int(bucket['nr_state']) +  int(p[7])
            if str(p[9]) == 'r':
                bucket['r_state'] = int(bucket['r_state']) +  int(p[7])

            action_return = 'alias_{}('.format(p[1])
            for i in range(int(p[7])):
                action_return += '{}{},'.format(p[1],i+1)

            action_return = action_return.strip(' ,') + ')'

            _alias[p[1]] = { 'id':p[1],'type' : 'bucket_action','return' : action_return, 'pick_type' : p[9],
                            'length' : int(p[7]),'bucket': bucket, 'roll_overload': 0}
        else:
            print("wrong bucket name",p.lineno(3))



def p_error(p):
   print("Syntax error in input!", p)
   exit()


def getSolver(data, debug=0):
    probQparser = yacc.yacc()
    probQparser.error = 0
    # declare pre-existing stuffs
    for key,value in _entity.items():
        solver.add_enitity(value)

    # start parsing with lexer from probQlexer
    p = probQparser.parse(data,lexer = lexer,debug=debug )

    return solver
