package twitter.nlp.service.impl;

import edu.stanford.nlp.ling.CoreAnnotations.LemmaAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TokensAnnotation;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.util.CoreMap;
import twitter.nlp.service.IParseFacade;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import twitter.exception.InvalidInputException;

import java.util.ArrayList;
import java.util.List;

@Component
public class Lemmatize implements IParseFacade {

    @Autowired
    private StanfordCoreNLP stanfordCoreNlp;

    public List<String> getResult(String documentText) throws InvalidInputException {
        if (documentText == null || documentText.length() == 0)
            throw new InvalidInputException();

        List<String> lemmas = new ArrayList<String>();
        Annotation document = new Annotation(documentText);
        this.stanfordCoreNlp.annotate(document);
        List<CoreMap> sentences = document.get(SentencesAnnotation.class);
        for (CoreMap sentence : sentences) {
            for (CoreLabel token : sentence.get(TokensAnnotation.class)) {
                lemmas.add(token.get(LemmaAnnotation.class));
            }
        }
        return lemmas;
    }
}
