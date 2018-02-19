import os, sys, json, shutil
import urllib.request
from html.parser import HTMLParser

class ExampleParser(HTMLParser):
  def __init__(self):
    super().__init__()
    self.status = None
    self.example_input = []
    self.example_output = []
    self.example_data = []
    self.div_level = 0

  def handle_starttag(self, tag, attrs):
    if tag == 'div':
      class_val = [v for k, v in attrs if k == 'class']
      if len(class_val) == 1:
        class_val = class_val[0]
      if class_val == 'sample-test':
        self.status = 'sample-test'
      elif self.status == 'sample-test' and class_val == 'input':
        self.status = 'input'
        self.div_level = 0
      elif self.status == 'sample-test' and class_val == 'output':
        self.status = 'output'
        self.div_level = 0
      elif self.status in ['input', 'output']:
        self.div_level += 1

    if tag == 'pre' and self.status in ['input', 'output']:
      self.status = self.status + '-pre'

  def handle_endtag(self, tag):
    if tag == 'pre' and self.status in ['input-pre', 'output-pre']:
      self.status = self.status.split('-')[0]
    if tag == 'div':
      if self.div_level > 0:
        self.div_level -= 1
      else:
        if self.status == 'input':
          self.example_input.append(self.example_data)
          self.example_data = []
          self.status = 'sample-test'
        elif self.status == 'output':
          self.example_output.append(self.example_data)
          self.example_data = []
          self.status = 'sample-test'
        elif self.status == 'sample-test':
          self.status = None

  def handle_data(self, data):
    if self.status in ['input-pre', 'output-pre']:
      self.example_data.append(data)


contest_id = sys.argv[1]
base = 'http://codeforces.com/contest/%s/' % (contest_id)

print('Setting... ' + base)

contest_dir = 'contest/%s/' % (contest_id)

for i in range(26):
  problem_id = chr(ord('A') + i)
  suffix = 'problem/%s' % (problem_id)

  page = urllib.request.urlopen(base + suffix)
  if page.getcode() != 200:
    break

  html_body = page.read().decode()

  parser = ExampleParser()
  parser.feed(html_body)

  if not parser.example_input and not parser.example_output:
    break
  print(suffix)

  problem_dir = contest_dir + '%s/' % (problem_id)
  os.makedirs(problem_dir + 'input', exist_ok=True)
  os.makedirs(problem_dir + 'output', exist_ok=True)
  os.makedirs(problem_dir + 'conf', exist_ok=True)

  data_id = 0
  for in_data, out_data in zip(parser.example_input, parser.example_output):
    in_fname = problem_dir + '/input/input_%d' % (data_id)
    out_fname = problem_dir + '/output/output_%d' % (data_id)
    with open(in_fname, 'w') as f:
      f.write('\n'.join(in_data))
    with open(out_fname, 'w') as f:
      f.write('\n'.join(out_data))
    data_id += 1

  pinfo_fname = problem_dir + '/conf/problem_info.json'
  pinfo = {
    'num_testcase': data_id,
  }
  with open(pinfo_fname, 'w') as f:
    f.write(json.dumps(pinfo))
  shutil.copyfile('base/basic.cpp', problem_dir + 'solution.cpp')
  shutil.copyfile('base/basic.py', problem_dir + 'solution.py')
