import sys
import readchar
import colorama

def main(num_line_start):
    """ Processes predefined file and asks the user for annotation each row as either positive
    or negative.

    Arguments
        num_line_start : integer, how many rows to skip in the input file

    """

    filename_input = "korp_eval_raw.txt"
    filename_output_pos = "korp_eval_pos.txt"
    filename_output_neg = "korp_eval_neg.txt"
    filename_output_discarded = "korp_eval_discarded.txt"

    try:
        file_input = open(filename_input, 'r', encoding="utf8")
        file_output_pos = open(filename_output_pos, 'a', encoding="utf8")
        file_output_neg = open(filename_output_neg, 'a', encoding="utf8")
        file_output_discarded = open(filename_output_discarded, 'a', encoding="utf8")
    except IOError:
        print("error opening files")
        if file_input is not None:
            file_input.close()
        if file_output_neg is not None:
            file_output_neg.close()
        if file_output_neg is not None:
            file_output_neg.close()
        if file_output_discarded is not None:
            file_output_discarded.close()
        sys.exit(1)

    print("To annotate lines, press p for positive, n for negative, " \
        "any other letter to discard. Q to quit.")
    print()

    positives, negatives, discarded = 0, 0, 0

    colorama.init(autoreset=True)

    for num_line, line in enumerate(file_input):
        if num_line < num_line_start:
            continue
        print(line.strip())
        char = readchar.readchar().decode()
        if char == 'p':
            print(colorama.Fore.GREEN + "pos")
            file_output_pos.write(line)
            positives += 1
        elif char == 'n':
            print(colorama.Fore.RED + "neg")
            file_output_neg.write(line)
            negatives += 1
        elif char == 'q':
            print("quit")
            break
        else:
            print(colorama.Fore.BLUE + "discarded")
            file_output_discarded.write(line)
            discarded += 1

    total = num_line_start + positives + negatives + discarded
    print()
    print(f"Annotated {positives} positives and {negatives} negative sentences. Discarded {discarded} rows.")
    print(f"In total {total} sentences have been processed.")

    file_input.close()
    file_output_neg.close()
    file_output_neg.close()
    file_output_discarded.close()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(int(sys.argv[1]))
    else:
        main(0)
