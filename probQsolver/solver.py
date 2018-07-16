import sys
import os
from random import randint
import re

class QNode(object):
    def __init__(self,q_type, q_atom):
        self.q_type = q_type # [and, or, not q_atom]
        self.q_atom = q_atom
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

    def __str__(self):
        return 'TYPE:{}, CH:{}'.format(self.q_type, self.children)


def get_entity(entity):
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

    return entity_layout

def get_entity_instance(instance):
    e_instance_layout = instance['entity'] + '(' + instance['label'] + ', '
    for p in instance['params']:
        e_instance_layout = e_instance_layout + str(p) + ', '

    e_instance_layout = e_instance_layout + 'D ) :- between(1, ' +  str(instance['count']) + ', D).'

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


def get_bucket_action(action):
    alias = action['action_alias']
    pick_type = action['pick_type']
    pick_count = int(action['pick_count'])

    bucket = action['bucket']
    if pick_type=='nr':
        bucket_state = int(bucket['nr_state'])
    else:
        bucket_state = int(bucket['r_state'])
    bucket_items = []
    for item in bucket['instances']:
        item_layout = ''
        if item['type'] == 'entity_instance':
            item_layout = item['entity'] + '(' + bucket['bucket'].strip(' ') +'_'+ pick_type + ', '
            for p in item['params']:
                item_layout += str(p) + ', '
            item_layout += '1 )'
        elif item['type'] == 'atom':
            item_layout = item['name']
        bucket_items.append(item_layout)

    action_layout = ''
    action_alias_layout = action_alias_layout = 'alias_{}('.format(alias)
    for i in range(pick_count):
        action_alias_layout += '{}{},'.format(alias,i+1)
    action_alias_layout = action_alias_layout.strip(' ,') + ')'
    action_alias_def = action_alias_layout
    action_alias_layout += ' :- '
    bucket_new_state = bucket_state + pick_count
    for i in range(bucket_state, bucket_new_state):
        action_layout += h_bucket_action_template(bucket['bucket'],bucket_items,i,pick_type)
        action_layout += '\n\n'
        action_alias_layout += '{}_pick({}, {}, {}{}),'.format(bucket['bucket'],pick_type, i+1,alias,i + 1 - bucket_state)

    action_alias_layout = action_alias_layout.strip(' ,') + '.'
    action_layout += action_alias_layout


    return [action_alias_def, action_layout]


def h_bucket_action_template(b_name,item_list, b_state,pick_type):
    '''
     Returns something like this for no replacement:
     EC1/T ::  bag_pick(nr, 2 ,coin(0.5,0.5,1),EF1, EC2 , TF ); EC2/T :: bag_pick(nr, 2 ,
     coin(0.6,0.4,1), EC1 ,EF2, TF) :- bag_pick(nr, 1, X , EC1, EC2, T), EF1 is EC1-1,
     EF2 is EC2-1, TF is T-1.


      Returns something like this for replacement:
      EC1/T ::  bag_pick(r, 2 ,coin(0.5,0.5,1),EF1, EC2 , TF ); EC2/T :: bag_pick(r, 2 ,
      coin(0.6,0.4,1), EC1 ,EF2, TF) :- bag_pick(nr, 1, X , EC1, EC2, T), EF1 is EC1,
      EF2 is EC2, TF is T.
    '''
    template = ''
    length = len(item_list)
    for idx, item in enumerate(item_list):
        layout = 'EC{}/T :: {}_pick_with_state({}, {},{},'.format(idx+1,b_name,pick_type,b_state +1,item)
        for i in range(length):
            if i==idx:
                layout = layout + 'EF{},'.format(i+1)
            else:
                 layout = layout + 'EC{},'.format(i+1)

        layout = layout + 'TF); '
        template += layout

    template = template.strip(' ;')
    template += ':- {}_pick_with_state({}, {},DONT_CARE,'.format(b_name,pick_type,b_state)
    for i in range(length):
        template += 'EC{},'.format(i+1)
    template += ' T), '
    if pick_type=='nr':
        for i in range(length):
                template += 'EF{} is EC{} - 1,'.format(i+1,i+1)
        template += 'TF is T - 1.'
    elif pick_type == 'r':
        for i in range(length):
                template += 'EF{} is EC{},'.format(i+1,i+1)
        template += 'TF is T .'

    return template


def get_bucket_roll_action(action):
    alias = action['action_alias']
    bucket_pick = action['bucket_pick']
    print(bucket_pick)
    roll_overload = int(bucket_pick['roll_overload'])
    pick_count = int(bucket_pick['length'])
    bucket = bucket_pick['bucket']
    overload = []

    if roll_overload == 0:
        for item in bucket['instances']:
            item_layout = ''
            if item['type'] == 'entity_instance':
                item_l = item['entity'] + '( X1 , '
                for p in item['params']:
                    item_l += str(p) + ', '
                item_layout += item_l + 'X2 ) :- {}_pick(_,X2,'.format(bucket['bucket']) + item_l + '_)).'
            elif item['type'] == 'atom':
                item_l = item['name']
                if '(' not in item_l:
                    item_layout += item_l + '( {}_r , X2 ) :- {}_pick(_,X2,'.format(bucket['bucket'],bucket['bucket']) + item_l + '). \n'
                    item_layout += item_l + '( {}_nr , X2 ) :- {}_pick(_,X2,'.format(bucket['bucket'],bucket['bucket']) + item_l + '). \n'
                else:
                    param = item['name'].split('(')[1].split(')')[0]
                    name = item['name'].split('(')[0]
                    item_layout += param + '( {}_r , X2 ) :- {}_pick(_,X2,'.format(bucket['bucket'],bucket['bucket']) + item_l + '). \n'
                    item_layout += param + '( {}_nr , X2 ) :- {}_pick(_,X2,'.format(bucket['bucket'],bucket['bucket']) + item_l + '). \n'

            overload.append(item_layout)

    return overload



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
        regex = r'[\s+\-*\/%()]?[A-Z][a-zA-Z_0-9áéíóúñÁÉÍÓÚÑ]*[0-9]?'
        matches = re.findall(regex,body)
        alias_list = []
        for each in matches:
            alias_list.append(each.strip(' +-*/%()')[:-1])
        q_alias += alias_list
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
        self.bucket_def = []
        self.bucket_action = {}
        self.bucket_roll_action = {}

    def add_enitity(self,entity):
        entity_layout = get_entity(entity)
        self.entities[entity['entity']] = entity_layout

    def add_entity_instance(self,instance):
        instance_layout = get_entity_instance(instance)
        self.entity_instances.append(instance_layout)

    def add_entity_action(self,action):
        action_layout = get_entity_action(action)
        self.action[action['action_alias']] = action_layout[1]
        self.action_def[action['action_alias']] = action_layout[0]
        return action_layout[0]

    def add_bucket_def(self,bucket):
        b_name = bucket['bucket']
        template_r = '{}_pick_with_state(r, 0, default,'.format(b_name)
        template_nr = '{}_pick_with_state(nr, 0, default,'.format(b_name)

        with_state_to_pick = '{}_pick(Type, State, Atom) :- {}_pick_with_state(Type, State, Atom,'.format(b_name,b_name)
        for item in bucket['instances']:
            template_r += str(item['count']) + ','
            template_nr += str(item['count']) + ','
            with_state_to_pick += '_ , '

        template_r += str(bucket['size']) + ').'
        template_nr += str(bucket['size']) + ').'
        with_state_to_pick += '_ ). '
        self.bucket_def.append(template_r)
        self.bucket_def.append(template_nr)
        self.bucket_def.append(with_state_to_pick)


    def add_bucket_action(self, action):
        action_layout = get_bucket_action(action)
        self.bucket_action[action['action_alias']] = action_layout[1]
        self.action_def[action['action_alias']] = action_layout[0]

    def add_bucket_picked_roll(self,action):
        action_layout = get_bucket_roll_action(action)
        self.bucket_def += action_layout



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
        code += '%---------------------------e_def----------------------------\n'
        for key, value in self.entities.items():
            code = code + str(value) + '\n'
        code = code + '\n'
        code += '%-----------------------e_instance---------------------------\n'
        for value in self.entity_instances:
            code = code + str(value) + '\n\n'
        code = code + '\n'
        code += '%-----------------------e_action-----------------------------\n'
        for key, value in self.action.items():
            code = code + str(value) + '\n'
        code = code + '\n'
        code += '%--------------------------b_def-----------------------------\n'
        for value in self.bucket_def:
            code = code + str(value) + '\n'
        code = code + '\n'
        code += '%--------------------------b_action--------------------------\n'
        for key, value in self.bucket_action.items():
            code = code + str(value) + '\n\n'
        code = code + '\n'
        code += '%----------------------------query---------------------------\n'
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
