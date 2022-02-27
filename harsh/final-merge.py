import pickle

with open("ocr_extract.txt", "rb") as fp:   # Unpickling
        ocr = pickle.load(fp)
print(ocr)