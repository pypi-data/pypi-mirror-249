import json
import pandas as pd
import math
from thefuzz import fuzz
from iftc import ift_config


class Candidate:
  def __init__(self):
    self.vowel = self._load_data(ift_config.vowel_path)
    self.vn_syl = self._load_data(ift_config.vn_syl_path)
    self.sentences = []

  def _load_data(self, file_path):
    with open(file_path) as json_file:
      data = json.load(json_file)
    return data

  def _decay_accent(self, word: str):
    telex = []
    accent = ''
    try:
      for c in word:
        for idx, v in enumerate(self.vowel):
          if c == v['none_accent']:
            telex.append(v['telex'])
            break
          elif c == v['acute']:
            telex.append(v['telex'])
            accent = 's'
            break
          elif c == v['grave']:
            telex.append(v['telex'])
            accent = 'f'
            break
          elif c == v['hook_above']:
            telex.append(v['telex'])
            accent = 'r'
            break
          elif c == v['tilde']:
            telex.append(v['telex'])
            accent = 'x'
            break
          elif c == v['underdot']:
            telex.append(v['telex'])
            accent = 'j'
            break
          elif idx == len(self.vowel)-1:
            telex.append(c)

      # result = []
      # str_telex = ''.join(telex)
      # if 'uwow' in str_telex:
      #   result.append(str_telex+accent)
      #   result.append(str_telex.replace('uwow','uow')+accent)
      #   result.append(str_telex.replace('uwow','wow')+accent)
      #   result.append(str_telex.replace('uwow','wo')+accent)
      # elif 'uw' in str_telex:
      #   result.append(str_telex+accent)
      #   result.append(str_telex.replace('uw','w')+accent)
      # else:
      #   result.append(str_telex+accent)
      result = ''.join(telex)+accent
      #print(result)
      return result
    except Exception as e:
      print(e)
      return word

  def _sigmoid(self, x):
    return 1 / (1 + math.exp(-x))

  def _count_character(self, str1: str, str2: str):
    same = 0
    different = 0
    for s in str1:
      if s in str2:
        same += 1
        str2 = str2.replace(s, '', 1)
      else:
        different += 1
    return same, different

  def _similarity(self, str1: str, str2: str):
    if abs(len(str1)-len(str2)) > 2:
      return -100
    same_char, dif_char = self._count_character(str1, str2)
    s = (same_char-dif_char) / \
        (self._sigmoid(abs(len(str1)-len(str2)))*((len(str1)+len(str2))/2))
    return s
  
  def jaccard_similarity(self, str1, str2):
    if abs(len(str1)-len(str2)) > 2:
      return -100
    s1 = set(str1)
    s2 = set(str2)
    return len(s1.intersection(s2)) / len(s1.union(s2))

  def _generate_sentences(self, candidates, mask, idx = 0):
    for i in candidates[idx]:
      mask[idx]=i
      if idx==len(candidates)-1:
        sentence = ' '.join(mask)
        if sentence not in self.sentences:
          self.sentences.append(sentence)
      else:
        self._generate_sentences(candidates, mask, idx+1)
        
  def _word_candidate(self, word: str):
    if len(word)<3 or word == 'xoong':
      return None

    candidate = []
    scores = []
    len_dif = []
    telex = self._decay_accent(word)
    for syl in self.vn_syl:
      if telex in syl['Instances']:
        candidate.append(syl['Origin'])
        return candidate

    for syl in self.vn_syl:
      score1 = self.jaccard_similarity(word, syl['Origin'])
      for ins in list(syl['Instances']):
        score2 = self.jaccard_similarity(telex,ins)
        if score1>0.7:
          score = (score1+score2)/2
        else:
          score = score2
        if score and score>0.7:
          candidate.append(syl['Origin'])
          scores.append(score)
          len_dif.append(100-abs(len(word)-len(syl['Origin'])))
          break
    candidate = [x for _,_,x in sorted(zip(scores, len_dif, candidate), reverse=True)]
    return candidate

  def word_candidate(self, message: str):
    candidates = []

    words = message.split()
    inner = False

    for i, w in enumerate(words):
      if ift_config.M_START in w:
        w = w.replace(ift_config.M_START, '')
        inner = True
        if ift_config.M_END in w:
          w = w.replace(ift_config.M_END, '')
          inner = False
        candidates.append((i, [w]))
      elif ift_config.M_END in w:
        w = w.replace(ift_config.M_END, '')
        inner = False
        candidates.append((i, [w]))
      elif inner:
        candidates.append((i, [w]))
      else:
        w_cdd = self._word_candidate(w)
        if w_cdd:
          candidates.append((i, w_cdd))
        else:
          candidates.append((i, [w]))
    #print(candidates)
    return candidates

  def sentence_candidate(self, message: str):
    candidates = []

    words = message.split()
    inner = False

    for w in words:
      if ift_config.M_START in w:
        candidates.append([w.replace(ift_config.M_START, '')])
        inner = True
        if ift_config.M_END in w:
          candidates.append([w.replace(ift_config.M_END, '')])
          inner = False
      elif ift_config.M_END in w:
        candidates.append([w.replace(ift_config.M_END, '')])
        inner = False
      elif inner:
        candidates.append([w])
      else:
        w_cdd = self._word_candidate(w)
        if not w_cdd:
          candidates.append([w])
        else:
          candidates.append(w_cdd)
    #print(candidates)
    mask=['[mask]']*len(candidates)
    self._generate_sentences(candidates, mask)
    return self.sentences, candidates