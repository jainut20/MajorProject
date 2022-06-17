
def final_merge(ocr,aud):
    final={}
    file = open("final_recognized.txt", "w+", encoding="utf-8")
    file.write("")
    for i in ocr:
            file.write(i)
            file.write("\n")
            file.write(ocr[i])
            file.write("\n\n")
            if i in aud:
                file.write(aud[i])
                file.write("\n\n\n")
                final[i]=ocr[i]+"\n\n"+aud[i]
            else:
                file.write("\n\n\n")
                final[i]=ocr[i]
    file.close()
    return final