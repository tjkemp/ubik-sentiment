import sys
import operator
import collections

def main(filename_input):
    """ Reads a file and outputs all words. """

    all_words = {}

    with open(filename_input, 'r', encoding="utf8") as file_input:

        for line in file_input:
            words = line.split()
            words = map(str.lower, words)
            for word in words:
                try:
                    all_words[word] += 1
                except KeyError:
                    all_words[word] = 1

    for word, count in sorted(all_words.items(), key=operator.itemgetter(1), reverse=True):
        print(f"{word} {count}")

    print()
    print("Summary: ")
    print("Number of unique words: {}".format(len(all_words)))
    counts = collections.Counter(all_words.values())
    print("Number of words appearing only once: {}".format(counts[1]))

    #for count, count_of_count in sorted(counts.items(), key=operator.itemgetter(1), reverse=True):
    #    print(f"{count} => {count_of_count}")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Usage: python word_list.py <filename>")
