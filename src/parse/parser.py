from natasha import Doc, Segmenter, MorphVocab, NewsEmbedding, NewsNERTagger, NewsSyntaxParser
from natasha.morph.tagger import NewsMorphTagger

from src.parse.city_extractor import CityExtractor
from src.parse.command_parsers.city_parser import CityParser
from src.parse.intent import Intent, Command
from src.parse.command_parsers.weather_parser import WeatherParser
from src.parse.user_state_extractor import UserStateExtractor


class Parser:
    def __init__(self):
        city_extractor = CityExtractor()
        self.__command_parsers = {
            Command.WEATHER: WeatherParser(city_extractor),
            Command.CITY: CityParser(city_extractor),
        }
        self.__user_state_extractor = UserStateExtractor()

        self.__segmenter = Segmenter()
        # TODO: check if there are existing another embeddings
        emb = NewsEmbedding()
        self.__morph_tagger = NewsMorphTagger(emb)
        self.__morph_vocab = MorphVocab()
        self.__ner_tagger = NewsNERTagger(emb)
        self.__syntax_parser = NewsSyntaxParser(emb)

    def __natasha_preprocessing(self, message: str) -> Doc:
        message = message.title()
        document = Doc(message)
        document.segment(self.__segmenter)
        document.tag_morph(self.__morph_tagger)
        for token in document.tokens:
            token.lemmatize(self.__morph_vocab)
        document.tag_ner(self.__ner_tagger)
        document.parse_syntax(self.__syntax_parser)
        for span in document.spans:
            span.normalize(self.__morph_vocab)
        return document

    def parse(self, message: str) -> Intent:
        document = self.__natasha_preprocessing(message)
        user_state = self.__user_state_extractor.get_user_state(document)
        for command, command_parser in self.__command_parsers.items():
            parse_results = command_parser.process(document)
            if parse_results is not None:
                return Intent(command, message, parse_results, user_state)
        return Intent(Command.UNKNOWN, message, user_state=user_state)
