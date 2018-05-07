package twitter.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.social.twitter.api.impl.TwitterTemplate;
import twitter.entity.Tweet;

import java.util.List;

public class TweetStreamService {

    @Autowired
    private TwitterTemplate twitterTemplate;

    public List<Tweet> getStreamOfTweets(){
        return null;
    }
}
