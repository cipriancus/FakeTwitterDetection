package twitter.main;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import org.springframework.social.twitter.api.Trend;
import org.springframework.stereotype.Component;
import twitter.trend.TrendSearch;

import javax.annotation.PostConstruct;
import java.util.List;

@Component
public class PsvmTrend {

    @Autowired
    private TrendSearch trendSearch;

    private static TrendSearch TREND_CONTROLLER;
    private final static long WORLD_WOEID = 1;


    public static void main(String[] args) {

        new ClassPathXmlApplicationContext("classpath:META-INF/twitter/applicationContext.xml",
                "classpath:META-INF/twitter/trend/applicationContext.xml");

        List<Trend> trends = TREND_CONTROLLER.getTrends(WORLD_WOEID);
        trends.forEach(trend -> System.out.println(trend.getName()));


    }

    @PostConstruct
    public void init() {
        if (trendSearch == null) {
            System.out.println("NULL");
        }
        TREND_CONTROLLER = trendSearch;
    }
}