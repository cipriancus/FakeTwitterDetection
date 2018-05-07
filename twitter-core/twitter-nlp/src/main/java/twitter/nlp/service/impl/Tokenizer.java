package twitter.nlp.service.impl;

import edu.stanford.nlp.ling.Word;
import edu.stanford.nlp.process.PTBTokenizer;
import edu.stanford.nlp.process.TokenizerFactory;
import twitter.nlp.service.IParseFacade;
import org.springframework.stereotype.Component;
import twitter.exception.InvalidInputException;

import java.io.StringReader;
import java.util.List;

@Component
public class Tokenizer implements IParseFacade {

    public List<Word> getResult(String sentence) throws InvalidInputException {
        if (sentence == null || sentence.length() == 0)
            throw new InvalidInputException();

        TokenizerFactory<Word> tf = null;
        if (tf == null)
            tf = PTBTokenizer.factory();

        List<Word> tokens_words = tf.getTokenizer(new StringReader(sentence)).tokenize();

        return tokens_words;
    }
}
