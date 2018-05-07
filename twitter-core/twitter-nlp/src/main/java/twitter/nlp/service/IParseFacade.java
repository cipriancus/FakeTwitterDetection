package twitter.nlp.service;

import twitter.exception.InvalidInputException;

import java.util.List;

public interface IParseFacade {
    List<?> getResult(String sentence) throws InvalidInputException;
}
