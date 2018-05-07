package test;

import edu.stanford.nlp.ling.Word;
import org.junit.Ignore;
import twitter.nlp.service.impl.Tokenizer;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import twitter.exception.InvalidInputException;

import static org.junit.Assert.assertTrue;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = {"classpath:META-INF/twitter/nlp/applicationContext.xml"})
@Ignore
public class TokenizerTest {
    Tokenizer tok = new Tokenizer();

    @Test
    public final void checkTheResponse() {
        try {
            assertTrue(tok.getResult("is a beautiful day").contains(new Word("beautiful")));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Test(expected = InvalidInputException.class)
    public final void checkException() throws InvalidInputException {
        tok.getResult(null);
    }

    @Test(expected = InvalidInputException.class)
    public final void getOutOfBound() throws InvalidInputException {
        tok.getResult("").get(0);
    }
}
