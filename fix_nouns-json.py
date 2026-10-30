import json
with open('batches/recovered_nouns.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
for item in data.get('vocab', []):
    if 'prefix_color' in item:
        item['class_or_stem'] = item.pop('prefix_color')
with open('batches/recovered_nouns.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('JSON keys updated to class_or_stem!')

