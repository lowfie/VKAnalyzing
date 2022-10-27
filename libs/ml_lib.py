from dostoevsky.models import FastTextSocialNetworkModel
from dostoevsky.tokenization import RegexTokenizer


class SentimentalAnalysisModel:
    def __init__(self) -> None:
        self.tokenizer = RegexTokenizer()
        self.model = FastTextSocialNetworkModel(tokenizer=self.tokenizer)

    def set_tone_comment(self, comment: list[str]) -> str | None:
        results = self.model.predict(comment, k=2)[0]

        for key, value in results.items():
            if key == "speech":
                return "neutral"
            elif key == "skip":
                tones = [tone_comment for tone_comment in results.keys()]
                tones.remove("skip")
                return tones[0]
            elif value == max(results.values()):
                return key
        return None
