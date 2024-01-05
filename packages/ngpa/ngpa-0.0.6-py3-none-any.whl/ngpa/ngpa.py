from .lib import *
import argparse


def main():
  parser = argparse.ArgumentParser(
    prog='ngpa', description='''
    prepare your gpa in file(s), and calculate them. 
    format: course_name, score, credit
    ''')
  parser.add_argument("-r", "--run", help="want to run?", action='store_true', required=False)
  parser.add_argument("-e", "--exclude", action='extend',
                      nargs='+', type=str, required=False, help='a list of gpa files you want to exclude from calculating', default=[])
  parser.add_argument('filelist', action='extend',
                      nargs='*', type=str, help='a list of gpa files you want to calculate', default=[])
  args = parser.parse_args()
  exclude = sum(list(map(lambda i: courses_from_file(i), args.exclude)), [])
  filelist = sum(list(map(lambda i: courses_from_file(i), args.filelist)), [])
  if not exclude and not filelist:
    parser.print_help()
    return
  print(exclude_from(filelist, exclude, args.run))


if __name__ == '__main__':
  main()
