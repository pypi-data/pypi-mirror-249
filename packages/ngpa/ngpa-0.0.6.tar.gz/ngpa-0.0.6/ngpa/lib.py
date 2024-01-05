from io import TextIOWrapper


def map_from(n: float) -> float:
  if 90 <= n <= 100:
    return 4.0
  elif 85 <= n <= 89:
    return 3.7
  elif 82 <= n <= 84:
    return 3.3
  elif 78 <= n <= 81:
    return 3.0
  elif 75 <= n <= 77:
    return 2.7
  elif 72 <= n <= 74:
    return 2.3
  elif 68 <= n <= 71:
    return 2.0
  elif 64 <= n <= 67:
    return 1.5
  elif 60 <= n <= 63:
    return 1.0
  return 0


class Course:
  def __init__(self, name: str, score: float, credit: float) -> None:
    self.name = name
    self.score = score
    self.credit = credit

  @property
  def score_credit(self) -> float:
    return self.score * self.credit

  def __eq__(self, __value: object) -> bool:
    if (not isinstance(__value, Course)):
      return False
    return self.name == __value.name

  def __ne__(self, __value: object) -> bool:
    return not self.__eq__(__value)

  def __str__(self):
    return f'<name:{self.name.__repr__()}, score:{self.score}, credit:{self.credit}>'
  __repr__ = __str__


def courses_from_file(f: str) -> list[Course]:
  """takes filepath and returns a list of Course

  Args:
      f (str): filepath

  FileFormat:
    file format is simple. each line consists of two or three words and will be used to initialize a 
    Course object. if one line has two words, then the first should be you score and the second should be 
    the credit of this course.

  Returns:
      list[Course]: a list of Course
  """
  with open(f, mode='r', encoding='utf-8') as file:
    return courses_from_fd(file)


def courses_from_stdin() -> list[Course]:
  """almost the same function as `courses_from_file` except reading from stdin

  Returns:
      list[Course]: a list of Course
  """
  from sys import stdin
  return courses_from_fd(stdin)


def courses_from_fd(f: TextIOWrapper) -> list[Course]:
  """helper function, takes a TextIOWrapper and returns a list of Course

  Args:
      f (TextIOWrapper): a TextIOWrapper, eg. an opened file or stdin/stderr

  Returns:
      list[Course]: a list of Course
  """
  credits = []
  lines = f.readlines()
  for line in lines:
    component = line.split()
    if (len(component) == 2):
      component = ['_'] + component[:]
    assert len(component) == 3, "invalid format"
    credits.append(Course(component[0], float(
        component[1]), float(component[2])))
  return credits


def courses_from_list(l: list) -> list[Course]:
  """another helper function, makes a list of Course from a list of iterable

  Args:
      l (list): a list of tuple with length at least 2

  Returns:
      list[Course]: a list of Course
  """
  credits = []
  for i in l:
    assert (2 <= len(i) <= 3), 'invalid format'
    if (len(i) == 2):
      name = '_'
      score, grade = i
    else:
      name, score, grade = i
    credits.append(Course(name, score, grade))
  return credits


def gpa(gpa_list: list[Course]) -> float:
  """takes a list of Course and reduce it to final gpa. only works with Nanjing University

  Args:
      gpa_list (list[Course]): a list of Course

  Returns:
      float: gpa
  """
  if not gpa_list:
    return 0
  return (sum([g.score_credit for g in gpa_list])) / (sum([g.credit for g in gpa_list])) / 20


def gpa_run(gpa_list: list[Course]) -> float:
  """takes a list of Course and reduce it to final gpa(run). only works with Nanjing University

  Args:
      gpa_list (list[Course]): a list of Course

  Returns:
      float: gpa for running
  """
  if not gpa_list:
    return 0
  return (sum(map(lambda x: map_from(x.score) * x.credit, gpa_list))) / (sum(map(lambda x: x.credit, gpa_list)))


def merge_gpa(list1: list[Course], list2: list[Course]) -> float:
  """merge two list of Course and calculate the final gpa

  Args:
      list1 (list[Course]): list1
      list2 (list[Course]): list2

  Returns:
      float: gpa
  """
  return gpa(list1 + list2)


def exclude_from(gpa_list: list[Course], exclude_list: list[Course], run=False) -> float:
  """filter out some courses from gpa_list

  Args:
      gpa_list (list[Course]): gpa_list
      exclude_list (list[Course]): courses needs to be filtered out

  Returns:
      float: gpa
  """
  return gpa(gpa_list=list(filter(lambda a: a not in exclude_list, gpa_list))) if not run else (gpa_run(gpa_list=list(filter(lambda a: a not in exclude_list, gpa_list))))
