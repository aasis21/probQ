import sys
import os
from random import randint

class QNode(object):
    def __init__(self,q_type, q_atom):
        self.q_type = q_type # [and, or, not q_atom]
        self.q_atom = q_atom
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

    def __str__(self):
        return 'TYPE:{}, CH:{}'.format(self.q_type, self.children)


def get_entity_layout(entity):
    problog_string = ''
    e_action_layout_atom = entity['entity'] + '_roll(L'
    e_iden_layout = entity['entity'] + '(L'
    name = entity['entity']
    for key, value in entity['feature'].items():
        new_p = 'P_' + str(name).strip().capitalize() + '_' + str(key)
        e_action_layout_atom = e_action_layout_atom + ', ' + new_p
        e_iden_layout = e_iden_layout + ', ' + new_p

    e_action_layout_atom = e_action_layout_atom + ', D'
    e_iden_layout = e_iden_layout + ', D)'
    entity_layout = ''

    for key, value in entity['feature'].items():
        p = 'P_' + str(name).strip().capitalize() + '_' + str(key)
        n = str(key).strip()
        entity_layout = entity_layout + p + ' :: ' + e_action_layout_atom + ', ' + n + '); '

    entity_layout = entity_layout.strip('; ') + ' :- ' + e_iden_layout + '.'

    print(entity_layout)
    return entity_layout

def get_entity_instance(instance):
    e_instance_layout = instance['entity'] + '(' + instance['label'] + ', '
    for p in instance['params']:
        e_instance_layout = e_instance_layout + str(p) + ', '

    e_instance_layout = e_instance_layout + 'D ) :- between(1, ' +  str(instance['count']) + ', D).'

    # print(e_instance_layout)
    return e_instance_layout

def get_entity_action(action):
    alias = action['action_alias']
    ei = action['entity_instance']
    action_name  = 'alias_' + alias.strip()
    count = int(ei['count'])

    action_layout = action_name + '('
    for i in range(count):
        action_layout = action_layout + alias + str(i+1) +', '

    action_term = action_layout.strip(', ') + ')'

    action_layout = action_layout.strip(', ') + ') :- '


    flag = ei['label']
    params = ei['params']
    action_atom = ei['entity'] + '_roll(' + flag + ', '

    for p in params:
        action_atom = action_atom + str(p) + ', '

    for i in range(count):
        action_layout = action_layout + action_atom + str(i+1) + ', ' + alias + str(i+1) + ' ), '

    action_layout = action_layout.strip(', ') + ' .'

    return [action_term , action_layout]


def get_alias_term_list(alias,start,end):
    l = ''
    for i in range(int(start),int(end)+1):
        l = l + alias + str(i) +', '
    l = l.strip(', ')
    return l

def get_action_terms_and_list(aliases):
    q_list = ''
    q_actions = ''
    for al in aliases:
        q_list = q_list +  get_alias_term_list(al['name'],1, al['length']) + ' ,'
        q_actions = q_actions + al['return'] + ' ,'
    q_list = q_list.strip(', ')
    q_actions = q_actions.strip(', ')
    return q_actions + ', L = [{}]'.format(q_list)


def q_tree_inorder(q_tree,q_alias):
    '''
    returns a core query string to be added in query
    '''
    if(q_tree.q_type == "q_atom"):
        q_atom_str = q_add_atom(q_tree.q_atom,q_alias)
        return q_atom_str

    query_str = ''
    for child in q_tree.children:
        q_atom_str = q_tree_inorder(child, q_alias)
        if(q_tree.q_type == "and"):
            query_str = query_str + q_atom_str + ' , '
        elif(q_tree.q_type == "or"):
            query_str = query_str + q_atom_str + ' ; '
        elif(q_tree.q_type == "not"):
            query_str = ' \+ ' + query_str + q_atom_str
        else:
            return("# SOMTHING BROKE")

    query_str = query_str.strip(',; ')
    query_str = '( ' + query_str + ' )'
    return query_str


def q_add_atom(q_atom,q_alias):
    q_type = q_atom['type']
    body = q_atom['body']

    if q_type == 'me':
        query = '( ' + body + ' )'
        # to do parse body to get alias list
        return query
    elif q_type == 'nl':
        construct = body['construct']
        params_count = body['params_count']

        num = body['number']
        equal = body['equal']

        iden = str(randint(1000,9999))
        query = '( count([{}],{}, C{})'.format(body['list'],equal,iden)
        if construct == 'equalAtmost':
            query = query + ' , C{} =< {} )'.format(iden, num)
        if construct == 'equalAtleast':
            query = query + ' , C{} >= {} )'.format(iden,num)
        if construct == 'equalFew':
            query = query + ' , C{} = {} )'.format(iden,num)
        if construct == 'equalAll':
            query = query + ' , C{} = {} )'.format(iden,body['list_len'])
        if construct == 'equalAny':
            query = query + ' , C{} >= 1 )'.format(iden)

        alias_list = body['alias_list']
        q_alias += alias_list

        return query




class blackbox:
    def __init__(self):
        self.entities = {}
        self.buckets = {}
        self.alias = {}
        self.entity_instances = []
        self.action ={}
        self.query = {}
        self.action_def = {}

    def add_enitity(self,entity):
        entity_layout = get_entity_layout(entity)
        self.entities[entity['entity']] = entity_layout

    def add_entity_instance(self,instance):
        instance_layout = get_entity_instance(instance)
        self.entity_instances.append(instance_layout)

    def add_entity_action(self,action):
        action_layout = get_entity_action(action)
        self.action[action['action_alias']] = action_layout[1]
        self.action_def[action['action_alias']] = action_layout[0]
        return action_layout[0]

    def add_query(self, query_tree):
        q_alias = []
        query_core = q_tree_inorder(query_tree,q_alias)
        q_alias_unique = list(set(q_alias))
        query_alias_def = ''
        for al in q_alias_unique:
            query_alias_def += self.action_def[str(al)] + ', '

        query_name = str(randint(1000,9999))
        query_str = 'q({}) :- {} {} . '.format(query_name,query_alias_def,query_core)
        self.query[query_name] = query_str
        return

    def get_code(self):
        code = ''
        for key, value in self.entities.items():
            code = code + str(value) + '\n'
        code = code + '\n'
        for value in self.entity_instances:
            code = code + str(value) + '\n'
        code = code + '\n'
        for key, value in self.action.items():
            code = code + str(value) + '\n'
        code = code + '\n'
        for key, value in self.query.items():
            code = code + str(value) + '\n'
        code = code + '\n'

        count = '''

:- use_module(library(lists)).
count([],X,0).
count([X|T],X,Y):- count(T,X,Z), Y is 1+Z.
count([X1|T],X,Z):- X1\=X,count(T,X,Z).

'''

        code = code + count + 'query(q(_)).'
        return code
