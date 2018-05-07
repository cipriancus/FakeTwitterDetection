package twitter.trend;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.social.twitter.api.Trend;
import org.springframework.social.twitter.api.impl.TwitterTemplate;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class TrendSearch {

    @Autowired
    private TwitterTemplate twitterTemplate;


    public List<Trend> getTrends(long woeid) {
        List<Trend> trends = twitterTemplate.searchOperations()
                .getLocalTrends(woeid)
                .getTrends();
        return trends;
    }
}
