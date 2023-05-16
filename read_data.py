from os import getcwd, walk
import re
# import sklearn_crfsuite

# Returns a list of examples (where each example is a list containing the 5 lines)
def read_file(file_path):
    with open(file_path) as f:
        lines = f.readlines()
        lines.append("\n") # So that the final sentence also ends in a blank line

    sentences = []
    current_sentence = []
    for i, line in enumerate(lines):
        if (i + 1) % 6 == 0: # Every 6th line is a blank line marking the end of the current sentence
            sentences.append(current_sentence)
            current_sentence = []
        else:
            current_sentence.append(line)
    return(sentences)

# Read in each file from this speaker, and return all the example sentences stored in one big list
def read_all_files_for_speaker(folder_path):
    sentences = []
    for root, dirs, files in walk(getcwd() + folder_path):
        for file in files:
            if file.endswith(".txt"):
                sentences.extend(read_file(getcwd() + folder_path + file)[:])
          
    return sentences

# Returns a train, dev, and test dataset
def create_datasets():
    speaker_1_folder_path = "/plaintext/BS/"
    speaker_1_sentences = read_all_files_for_speaker(speaker_1_folder_path)
#     print(speaker_1_sentences)
#     print(f"Speaker 1: {len(speaker_1_sentences)} sentences.")

    speaker_2_folder_path = "/plaintext/HH/"
    speaker_2_sentences = read_all_files_for_speaker(speaker_2_folder_path)
#     print(f"Speaker 2: {len(speaker_2_sentences)} sentences.")

    speaker_3_folder_path = "/plaintext/VG/"
    speaker_3_sentences = read_all_files_for_speaker(speaker_3_folder_path)
#     print(f"Speaker 3: {len(speaker_3_sentences)} sentences.")

    train = speaker_1_sentences[:345] + speaker_2_sentences[:298]+ speaker_3_sentences[:393]
    print("Train data:", len(train), "sentences.")
    dev = speaker_1_sentences[345:388] + speaker_2_sentences[298:333]+ speaker_3_sentences[393:442]
    print("Dev data:", len(dev), "sentences.")
    test = speaker_1_sentences[388:] + speaker_2_sentences[333:]+ speaker_3_sentences[442:]
    print("Test data:", len(test), "sentences.")
    print("")

    return train, dev, test

# Returns the X and y lines from the dataset
def extract_X_and_y(dataset):
    X = [sentence[1] for sentence in dataset]
    y = [sentence[3] for sentence in dataset]

    return X, y

def general_preprocess(sentence):
    #  To deal with weird underline char, as in G̲aldo'o, I am just removing it for now
    sentence = re.sub(r'\u0332', "", sentence)

    sentence = sentence.replace("\n", "")

    # Remove bracketed affixes (at least for now)
    sentence = re.sub(r'\[[^\]]*\]', "", sentence)   

    return sentence 

# Break down each (transcription) sentence into "words",
# where each word is a list of morphemes (could be just one) - this is done for feature generation
# Returns the sentence as a word list instead
def sentence_to_words(sentence):
    word_list = []

    sentence = general_preprocess(sentence)

    for word in sentence.split(" "):
        morpheme_list = []
        # Split up morphemes
        morpheme_list = re.split(r'[-=]', word)
        word_list.append(morpheme_list)
    return word_list
