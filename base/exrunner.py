import sys, subprocess, json

contest_id = sys.argv[1]
problem_id = sys.argv[2]
print('Compiling... ', contest_id, '/', problem_id)

base_dir = 'contest/%s/%s/' % (contest_id, problem_id)
cmd = 'g++ %s/solution.cpp -o %s/conf/executable' % (base_dir, base_dir)
ret = subprocess.call(cmd, shell=True)
if ret != 0:
  print('Failed to compile')
  sys.exit(-1)


with open('%s/conf/problem_info.json' % (base_dir), 'r') as f:
  problem_info = json.loads(f.read())

num_testcase = problem_info['num_testcase']

def validate(result, answer):
  result_lines = result.strip().split()
  if len(result_lines) != len(answer):
    return False
  for r, a in zip(result_lines, answer):
    if r and a and r.strip() != a.strip():
      return False
  return True

print('Start TEST!\n')
is_failed = False
for t_i in range(num_testcase):
  cmd = '%s/conf/executable %d' % (base_dir, t_i)
  result = subprocess.check_output(cmd, shell=True).decode()

  with open('%s/output/output_%d' % (base_dir, t_i), 'r') as f:
    answer = f.readlines()

  if validate(result, answer):
    print('[OK for TEST]', t_i)
  else:
    is_failed = True
    print('[WA for TEST]', t_i)
    print('Answer --------------------')
    for a in answer:
      print(a)

    print('\nYour Output ---------------')
    print(result)


print('\nResult:')
if is_failed:
  print('  FAILED')
else:
  print('  SUCCESS')
