import os, json, random


directory = "data/nela-gt-2021/newsdata/train"

all_files = os.listdir(directory)
json_files = [file for file in all_files if file.endswith('.json')]
selected_files = random.sample(json_files, 5)
featured_articles = []
for file in selected_files:
    file_path = os.path.join(directory, file)
    
    with open(file_path, 'r') as f:
        data = json.load(f)
        random_dict = random.choice(data)
        featured_articles.append(random_dict)

for a in featured_articles:
    print(a)