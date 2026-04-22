import sys

people = {}
while True:
  try:
    s = input()
  except EOFError:
    break
  #print('s:', s)
  if s.startswith('Name:'):
    fields = s.split(',')
    name = fields[0].split(':')[1][1:]
    number = fields[1].split(':')[1][1:]
    people[name] = number
    #print('name:', name, 'number:', number)
if people == {'Alex': '1', 'Alessa': '3'}:
  sys.exit(0)
else:
  #print("people is", people)
  sys.exit(1)
