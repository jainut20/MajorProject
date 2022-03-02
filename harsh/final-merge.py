import pickle

with open("ocr_extract.txt", "rb") as fp:   # Unpickling
        ocr = pickle.load(fp)
with open("../utkarsh/audio_dict.txt", "rb") as fp:   # Unpickling
        aud = pickle.load(fp)
file = open("final_recognized.txt", "w+")
file.write("")
for i in ocr:
        file.write(i)
        file.write("\n")
        file.write(ocr[i])
        file.write("\n\n")
        file.write(aud[i])
        file.write("\n\n\n")
file.close()