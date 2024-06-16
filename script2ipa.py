import argparse
import re
from pypinyin import pinyin
import eng_to_ipa as ipa
import nltk

parser = argparse.ArgumentParser(description='Mandarin-English transcription to IPA')
parser.add_argument("--input_file", default="./SEAME/train_set/text", type=str, help="Path to transcription file")
parser.add_argument("--output_file", default="./SEAME/train_set/text_ipa", type=str, help="Path to conversion result file")
parser.add_argument("--mapping_file", default="./pinyin2ipa.csv", type=str, help="Path to pinyin to IPA mapping file")
args = parser.parse_args()
'''
File format:
    - Input_file: ID text
    - Mapping file: Pinyin	IPA
'''
def main():
    # mapping pinyin to ipa
    input_file = args.input_file
    output_file = args.output_file
    mapping_file = args.mapping_file
    file = open(mapping_file, encoding='utf-8')
    pinyin2ipa = {}
    for line in file:
        p,i = line.split('	')
        pinyin2ipa[p] = re.sub('\n', '', i)
    pattern = re.compile("|".join(pinyin2ipa.keys()))
    file=open(input_file, encoding='utf-8')
    text = []
    tkns = ""
    for line in file:
        try:
            jdata = line.split(" ", 1)
            seg_name = jdata[0]
            script = jdata[1]
            script= re.sub('\n', '', script)
            k = script.split(" ")
            p = ''
            words = ''
            for i in k:
                if words == '':
                    words = i  # first word
                elif i[0] <= 'z' and words[0] <= 'z':  # the same En
                    words = words + " " + i
                elif i[0] > 'z' and words[0] > 'z':  # the same Zh
                    if i[0]==words[-1]=='了':
                        words = words +" "+ i
                        print(words)
                    else:
                        words = words + i
                elif words <= 'z':  # words (en), i (zh)
                    p = p + " " + ipa.convert(words)
                    words = i
                else:  # words (en), i (zh)
                    py =  ' '.join([str(elem[0]) for elem in pinyin(words)])
                    s = pattern.sub(lambda m: pinyin2ipa[re.escape(m.group(0))], py)
                    p = p + " " + s
                    words = i
            if words <= 'z':
                p = p + ' ' + ipa.convert(words)
            else:
                py = ' '.join([str(elem[0]) for elem in pinyin(words)])
                s = pattern.sub(lambda m: pinyin2ipa[re.escape(m.group(0))], py)
                p = p + " " + s
            p = re.sub(' +', ' ', p)
            p = re.sub('<v-noise\*>', 'ppp', p)
            text_entry = seg_name + " " + p.strip()
            text.append(text_entry)
            tkns = tkns + " " + p
        except:
            print("line", line)
    chars= [i for i in tkns ]
    chars = set(chars)
    chars =list(chars)
    chars.sort()
    print("chars: ", chars)
    print("No of chars ", len(chars))
    text = set(text)
    text = list(text)
    text.sort()
    textfile = open(output_file, "w", encoding='utf-8')
    print(output_file)
    for element in text:
        textfile.write(element + "\n")
    textfile.close()

if __name__ == "__main__":
    main()
