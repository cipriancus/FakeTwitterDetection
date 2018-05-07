package test;

import org.junit.Ignore;
import twitter.nlp.service.ISentiment;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = {"classpath:META-INF/twitter/nlp/applicationContext.xml"})
@Ignore
public class SentimentTest {

    @Autowired
    ISentiment sentimentAnalysis;

    @Test
    public final void checkTheResponse() {
        try {
            assert (sentimentAnalysis.calculateSentiment("I <3 obama") > -1);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
