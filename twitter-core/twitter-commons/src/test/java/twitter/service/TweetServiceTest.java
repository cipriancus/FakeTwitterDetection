package twitter.service;

import org.junit.Assert;
import org.junit.Ignore;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.transaction.annotation.Transactional;
import twitter.entity.Tweet;
import twitter.service.TweetService;

import java.util.List;


@ContextConfiguration(locations = {"classpath:applicationContext.xml"})
@RunWith(SpringJUnit4ClassRunner.class)
@Ignore
public class TweetServiceTest {
    @Autowired
    private TweetService tweetService;

    @Test
    @Transactional
    public void testTweetSave(){
        Tweet tweet = new Tweet();
        tweet.setText("text");

        tweet = tweetService.save(tweet);
        Assert.assertTrue(tweet.getText().equals("text"));
    }

    @Test
    @Transactional
    public void testTweetsFetch() {
        Tweet tweet = new Tweet();
        tweet.setText("text");
        tweetService.save(tweet);

        List<Tweet> tweets = tweetService.findAll();
        tweets.forEach(System.out::println);
        Assert.assertTrue(tweets.size() > 0);
    }
}
