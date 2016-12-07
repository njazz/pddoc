
# /Users/serj/work/music/pddoc/pddoc/txt/parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.5'

_lr_method = 'LALR'

_lr_signature = '3A8AA5E183808CC0D0C28612A84394BB'
    
_lr_action_items = {'WORD':([1,3,4,6,8,9,10,11,13,14,15,17,19,],[3,3,-6,3,-8,3,3,-12,-9,3,-7,-11,-10,]),'ASTERISK':([1,3,4,6,8,9,10,11,13,14,15,17,19,],[6,14,-6,14,-8,14,6,-12,-9,14,-7,-11,-10,]),'EOL':([1,2,3,4,6,8,9,10,11,12,13,14,15,16,17,19,],[11,11,11,-6,11,-8,11,11,-12,-1,-9,11,-7,-2,-11,-10,]),'COMMENT_END':([4,5,7,8,10,11,13,15,17,18,19,],[-6,-3,16,-8,-4,-12,-9,-7,-11,-5,-10,]),'TAG':([1,3,4,6,8,9,10,11,13,14,15,17,19,],[9,9,-6,9,-8,9,9,-12,-9,9,-7,-11,-10,]),'COMMENT_START':([0,],[1,]),'$end':([2,11,12,16,],[0,-12,-1,-2,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'rest_of_line':([1,3,6,9,10,14,],[4,13,15,17,4,19,]),'pdcontent':([1,10,],[5,18,]),'pdbody':([1,],[7,]),'eol':([1,2,3,6,9,10,14,],[8,12,8,8,8,8,8,]),'pddoc':([0,],[2,]),'line':([1,10,],[10,10,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> pddoc","S'",1,None,None,None),
  ('pddoc -> pddoc eol','pddoc',2,'p_pddoc','ext_lexer.py',102),
  ('pddoc -> COMMENT_START pdbody COMMENT_END','pddoc',3,'p_pddoc','ext_lexer.py',103),
  ('pdbody -> pdcontent','pdbody',1,'p_pdbody','ext_lexer.py',115),
  ('pdcontent -> line','pdcontent',1,'p_pdcontent','ext_lexer.py',121),
  ('pdcontent -> line pdcontent','pdcontent',2,'p_pdcontent','ext_lexer.py',122),
  ('line -> rest_of_line','line',1,'p_line','ext_lexer.py',129),
  ('line -> ASTERISK rest_of_line','line',2,'p_line','ext_lexer.py',130),
  ('rest_of_line -> eol','rest_of_line',1,'p_rest_of_line','ext_lexer.py',136),
  ('rest_of_line -> WORD rest_of_line','rest_of_line',2,'p_rest_of_line','ext_lexer.py',137),
  ('rest_of_line -> ASTERISK rest_of_line','rest_of_line',2,'p_rest_of_line','ext_lexer.py',138),
  ('rest_of_line -> TAG rest_of_line','rest_of_line',2,'p_rest_of_line','ext_lexer.py',139),
  ('eol -> EOL','eol',1,'p_eol','ext_lexer.py',161),
]