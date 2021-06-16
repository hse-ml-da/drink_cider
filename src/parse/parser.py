from natasha import Doc, Segmenter, MorphVocab, NewsEmbedding, NewsNERTagger, NewsSyntaxParser
from natasha.morph.tagger import NewsMorphTagger

from src.parse.intent import Intent, Command
from src.parse.weather_parser import WeatherParser


class Parser:
    def __init__(self):
        self.__command_parsers = {Command.WEATHER: WeatherParser()}
        self.__segmenter = Segmenter()
        # TODO: check if there are existing another embeddings
        emb = NewsEmbedding()
        self.__morph_tagger = NewsMorphTagger(emb)
        self.__morph_vocab = MorphVocab()
        self.__ner_tagger = NewsNERTagger(emb)
        self.__syntax_parser = NewsSyntaxParser(emb)

    def __natasha_preprocessing(self, message: str) -> Doc:
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
        for command, command_parser in self.__command_parsers.items():
            if command_parser.validate_query(document):
                return Intent(command, message, command_parser.extract_parameters(document))
        return Intent(Command.UNKNOWN, message)
