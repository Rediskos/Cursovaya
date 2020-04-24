import wordcloud
import matplotlib.pyplot as plt


with open("BD/Biologic/Bio.txt", "r", encoding = 'utf-8') as bio:
    with open("BD/Math/RealMathTerms.txt", "r", encoding = 'utf-8') as math:
        with open("BD/Sport/SportTerms.txt", "r", encoding = 'utf-8') as sport:
            a = bio.read().replace("\n", " ")
            b = math.read().replace("\n", " ")
            c = sport.read().replace("\n", " ")
            tmp = a + " " + b + " " + c
            Frame = wordcloud.WordCloud(width = 1280, height = 720)
            Frame.generate(tmp)
            # print(Frame.__array__())
            plt.imshow(Frame.__array__())
            plt.show