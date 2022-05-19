import pandas as pd

from pathlib import Path
# ------------
def onehotListElementwiseOr(*args):
  ans = [0] * len(args[0])
  for arg in args:
    ans = list(map(lambda x, y: x or y, ans, arg))
  return ans

def readFile(filePath:Path):
  if filePath.exists():
    if filePath.suffix == '.txt':
      df = pd.read_csv(filePath, sep='\t', names=['start', 'end', 'label'])
    elif filePath.suffix == '.csv':
      df = pd.read_csv(filePath, sep=',', names=['start', 'end', 'label'])
    else:
      print('Only txt and csv file acceptable')
  else:
    print(f'{filePath} does not exist')
  return df

def segment(intervalDF:pd.DataFrame):
  records = []
  labels = []
  for i, interval in intervalDF.iterrows():
    records.append([interval['start'], 'L', i])
    records.append([interval['end'], 'R', i])
    labels.append([int(ele) for ele in interval['label'].split(',')])
  ## Sort by time
  records = sorted(records)

  overlap = []
  results = []
  for i, record in enumerate(records):
    if record[1] == 'L':
      if overlap:
        tempLabel = [label for j, label in enumerate(labels) if j in overlap]
        results.append([records[i-1][0], record[0], onehotListElementwiseOr(*tempLabel)])
        overlap.append(record[2])
      else:
        overlap.append(record[2])
    else:
      tempLabel = [label for j, label in enumerate(labels) if j in overlap]
      results.append([records[i-1][0], record[0], onehotListElementwiseOr(*tempLabel)])
      overlap.remove(record[2])
  return results

def main():
  results = segment(readFile(Path.cwd().joinpath('interval-segment', 'demo', 'input.csv')))
  df = pd.DataFrame(results, columns=['start', 'end', 'label'])
  print(df)
  df.to_csv(Path.cwd().joinpath('interval-segment', 'demo', 'output.csv'), header=True, index=False)

# ------------
if __name__ == '__main__':
  main()