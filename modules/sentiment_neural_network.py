from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel


class SentimentalAnalysisModel:

    def __init__(self):
        self.tokenizer = RegexTokenizer()
        self.model = FastTextSocialNetworkModel(tokenizer=self.tokenizer)

    def set_tone_of_the_comment(self, comment):
        results = self.model.predict(comment, k=2)[0]

        print(comment)
        print(results)
        for key, value in results.items():
            if key == 'speech':
                return 'neutral'
            elif key == 'skip':
                tones = [tone_comment for tone_comment in results.keys()]
                tones.remove('skip')
                return tones[0]
            elif value == max(results.values()):
                return key
