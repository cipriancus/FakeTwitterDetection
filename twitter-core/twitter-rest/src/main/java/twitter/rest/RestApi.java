package twitter.rest;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.social.twitter.api.Trend;
import org.springframework.social.twitter.api.Trends;
import org.springframework.social.twitter.api.Tweet;
import org.springframework.stereotype.Component;
import request.Request;
import twitter.exception.InvalidInputException;
import twitter.nlp.service.IParseFacade;
import twitter.nlp.service.ISentiment;
import twitter.scrape.TwitterScrape;
import twitter.service.TweetService;
import twitter.trend.TrendSearch;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.MediaType;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Component
@Path("/api")
public class RestApi {

    @Autowired
    private TwitterScrape twitterScrape;

    @Autowired
    private TrendSearch trendSearch;

    @Autowired
    private TweetService twitterService;

    @GET
    @Produces(MediaType.APPLICATION_JSON)
    @Path("/tweets/{tweetTerm}")
    public List<Tweet> search(@PathParam("tweetTerm") String tweetTerm) {
        List<Tweet> tweetList = null;
        try {
            tweetList = twitterScrape.scrape(tweetTerm);
        } catch (InvalidInputException e) {
            e.printStackTrace();
        }
        return tweetList;
    }

    @GET
    @Produces(MediaType.APPLICATION_JSON)
    @Path("/trends")
    public List<Trend> trends() {
        return trendSearch.getTrends(1);
    }

    @GET
    @Produces(MediaType.APPLICATION_JSON)
    @Path("/news")
    public Map<Tweet, String> news() throws InvalidInputException {
        List<Trend> someTrends = trendSearch.getTrends(1);

        Map<Tweet, String> allClassification = new HashMap<>();

        for (Trend iterator : someTrends) {
            List<Tweet> tweets = twitterScrape.scrape(iterator.getName());

            for (Tweet iteratorTweet : tweets) {
                if (iteratorTweet.getLanguageCode().equals("en") == true) {
                    String classification = new Request().classify(iteratorTweet);

                    allClassification.put(iteratorTweet, classification);
                }
            }
        }
        return allClassification;
    }

    @GET
    @Produces(MediaType.APPLICATION_JSON)
    @Path("/clasifyDay")
    public Map<twitter.entity.Tweet, String> clasifyDay() throws InvalidInputException {
        Map<twitter.entity.Tweet, String> allClassification = new HashMap<>();

//        long countAllTweets = twitterService.countRecords();
        long countAllTweets = 100;

        int pageNo = 1;
        int items = 100;

        while (countAllTweets > 0) {
            List<twitter.entity.Tweet> tweetList = twitterService.getByPage(pageNo++, items);

            if (tweetList != null) {
                for (twitter.entity.Tweet iterator : tweetList) {
                    String classification = new Request().classifyTweetEntity(iterator);
                    allClassification.put(iterator, classification);
                }
                countAllTweets -= items;
            }
        }
        return allClassification;
    }
}

