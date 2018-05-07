package twitter.nlp.service;


import twitter.exception.InvalidInputException;

public interface ISentiment {
    int calculateSentiment(String text) throws InvalidInputException;
}
