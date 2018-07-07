import sys
import os


class entity:

    def __init__(self,entity):
        self.entity = entity['entity']
        self.params = entity['params']
        self.feature = entity['feature']
        self.problog = get_problog_layout(entity)


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

    # print(entity_layout)
    return entity_layout

def get_entity_instance(instance):
    e_instance_layout = instance['entity'] + '(' + instance['label'] + ', '
    for p in instance['params']:
        e_instance_layout = e_instance_layout + p + ', '

    e_instance_layout = e_instance_layout + 'D ) :- between(1, ' +  str(instance['number']) + ', D).'

    # print(e_instance_layout)
    return e_instance_layout

def get_entity_action(action):
    alias = action['alias']
    ei = action['instance']
    action_name  = 'alias_' + alias.strip()
    count = int(ei['number'])

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



class blackbox:
    def __init__(self):
        self.entities = {}
        self.buckets = {}
        self.alias = {}
        self.entity_instances = []
        self.action ={}
        self.query = {}

    def add_enitity(self,entity):
        entity_layout = get_entity_layout(entity)
        self.entities[entity['entity']] = entity_layout

    def add_entity_instance(self,instance):
        instance_layout = get_entity_instance(instance)
        self.entity_instances.append(instance_layout)

    def add_entity_action(self,action):
        action_layout = get_entity_action(action)
        self.action[action['alias']] = action_layout[1]
        return action_layout[0]

    def add_query(self, query):
        construct = query['construct']
        params_count = query['params_count']
        q_num = query['number']
        q_equal = query['equal']
        q_alias_list = query['alias_list']
        print(q_alias_list)
        q_list_iden = ''
        l = 0
        for al in q_alias_list:
            q_list_iden = q_list_iden + al['name'] + '_'
            l += al['length']
        query = ''
        query_name = ''
        if params_count == 3:
            query_name = 'q({}_{}_{}_{}) :- '.format(construct,q_num,q_list_iden, q_equal)
            query = 'q({}_{}_{}_{}) :- '.format(construct,q_num,q_list_iden, q_equal)
            query = query + ' {} , countall(L, E, C)'.format(get_action_terms_and_list(q_alias_list))
            query = query + ' , E = {}'.format(q_equal)
            if construct == 'equalAtmost':
                query = query + ' , C =< {} .'.format(q_num)
            if construct == 'equalAtleast':
                query = query + ' , C >= {} .'.format(q_num)
            if construct == 'equalFew':
                query = query + ' , C = {} .'.format(q_num)
        if params_count == 2:
            query_name = 'q({}_{}_{}_{}) :- '.format(construct,q_num,q_list_iden, q_equal)
            query = 'q({}_{}_{}_{}) :- '.format(construct,q_num,q_list_iden, q_equal)
            query = query + ' {} , countall(L, E, C)'.format(get_action_terms_and_list(q_alias_list))
            query = query + ' , E = {}'.format(q_equal)
            if construct == 'equalAll':
                query = query + ' , C = {} .'.format(l)
            if construct == 'equalAny':
                query = query + ' , C >= 1 .'

        self.query[query_name] = query

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

countall(List,X,C) :-
    sort(List,List1),
    member(X,List1),
    count(List,X,C).

'''

        code = code + count + 'query(q(_)).'
        return code
