package twitter.scrape;

import org.junit.Assert;
import org.junit.Ignore;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.social.twitter.api.Tweet;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import twitter.exception.InvalidInputException;

import java.util.List;

@ContextConfiguration(locations = {"classpath:applicationContext.xml"})
@RunWith(SpringJUnit4ClassRunner.class)
@Ignore
public class TwitterScrapeTest {

    @Autowired
    private TwitterScrape twitterScrape;


    @Test
    public void testNotNullScrapeList() throws InvalidInputException{
        List<Tweet> tweetList = twitterScrape.scrape("#obama");
        Assert.assertNotNull(tweetList);
    }

    @Test
    public void assertNotEmptyScrapeList() throws InvalidInputException{
        List<Tweet> tweets = twitterScrape.scrape("#obama");
        Assert.assertTrue(tweets.size() > 0);
    }
}
