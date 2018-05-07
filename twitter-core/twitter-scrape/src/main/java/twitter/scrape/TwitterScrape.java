package twitter.scrape;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.social.twitter.api.Tweet;
import org.springframework.social.twitter.api.impl.TwitterTemplate;
import org.springframework.stereotype.Component;
import twitter.exception.InvalidInputException;
import twitter.service.TweetService;
import java.util.List;

@Component
public class TwitterScrape {
    @Autowired
    private TweetService tweetService;

    @Autowired
    private TwitterTemplate twitterTemplate;

    public List<Tweet> scrape(String term) throws InvalidInputException{
        if(term == null || term.length()==0)
            throw new InvalidInputException();

        List<Tweet> tweetList = twitterTemplate.searchOperations().search(term).getTweets();

        tweetList.forEach(tweetEntity -> {
            twitter.entity.Tweet tweet = new twitter.entity.Tweet();
            tweet.setText(tweetEntity.getText());
            tweet.setId(tweetEntity.getId());
            tweet.setIdStr(tweetEntity.getIdStr());
            tweet.setRetweetCount(tweetEntity.getRetweetCount());
            tweet.setFavoriteCount(tweetEntity.getFavoriteCount());
            tweet.setCreatedAt(tweetEntity.getCreatedAt());
            tweet.setFromUserId(tweetEntity.getFromUserId());
            tweet.setUserName(tweetEntity.getUser().getName());
            tweet.setScreenName(tweetEntity.getUser().getScreenName());
            tweet.setFromUser(tweetEntity.getFromUser());
            tweet.setInReplyToScreenName(tweetEntity.getInReplyToScreenName());
            tweet.setInReplyToStatusId(tweetEntity.getInReplyToStatusId());
            tweet.setInReplyToUserId(tweetEntity.getInReplyToUserId());
            tweetService.save(tweet);
        });
        return tweetList;
    }
}