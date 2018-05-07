package test;

import org.junit.Ignore;
import twitter.nlp.service.impl.Lemmatize;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import twitter.exception.InvalidInputException;

import static org.junit.Assert.assertTrue;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = {"classpath:META-INF/twitter/nlp/applicationContext.xml"})
@Ignore
public class LemmatizeTest {

    Lemmatize lem = new Lemmatize();

    @Test
    public final void checkTheResponse() {
        try {
            assertTrue(lem.getResult("is a beautiful day").contains("be"));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Test(expected = InvalidInputException.class)
    public final void checkException() throws InvalidInputException {
        lem.getResult(null);

    }

    @Test(expected = InvalidInputException.class)
    public final void getOutOfBound() throws InvalidInputException {
        lem.getResult("").get(0);
    }
}
